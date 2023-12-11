import json
import logging
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import markdown2
from pyoxigraph import NamedNode
from pyoxigraph import Store
from rdflib import Graph
from rdflib import Namespace
from starlette.requests import Request
from starlette.responses import PlainTextResponse, Response, HTMLResponse
from starlette.staticfiles import StaticFiles

from src.rdframe.x_to_sparql.cql2sparql import CQLParser
from src.rdframe.dependencies import (
    get_global_shacl_state,
    get_shacl_pyoxi_store,
    get_global_cqljson_state,
    get_cql_pyoxi_store,
)
from src.rdframe.functions import (
    load_example_shacl_data_to_oxigraph,
    populate_initial_shacl_state,
    generate_sparql_query_from_shacl,
    populate_initial_cqljson_state,
    load_example_cql_data_to_oxigraph,
)

RDFRAME = Namespace("https://rdframe.dev/")
log = logging.getLogger(__name__)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8081",
    "http://localhost:8005",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

shacl_static_dir = Path(__file__).parent.parent / "rdframe" / "static" / "shacl"
app.mount("/shacl/static", StaticFiles(directory=shacl_static_dir), name="shacl-static")

cql_static_dir = Path(__file__).parent.parent / "rdframe" / "static" / "cql"
app.mount("/cql/static", StaticFiles(directory=cql_static_dir), name="cql-static")


# Route to serve the index.html
@app.get("/shacl/")
async def shacl_home():
    content = (shacl_static_dir / "index.html").read_text()
    return HTMLResponse(content=content)


@app.get("/cql/")
async def cql_home():
    content = (cql_static_dir / "cqljson.html").read_text()
    return HTMLResponse(content=content)


@app.get("/")
async def home():
    markdown_file_path = Path(__file__).parent.parent.parent / "README.md"
    markdown_content = markdown_file_path.read_text()

    converter = markdown2.Markdown(extras=["tables"])  # <-- here
    html_content = converter.convert(markdown_content)

    css_url = "https://unpkg.com/marx-css@4.1.1/css/marx.min.css"
    html_content_with_css = f"""<!DOCTYPE html><head><link rel="stylesheet" 
    href="{css_url}"></head><body>{html_content}</body></html>"""

    return Response(content=html_content_with_css, media_type="text/html")


@app.on_event("startup")
async def app_startup():
    shacl_state = get_global_shacl_state()
    cqljson_state = get_global_cqljson_state()
    await populate_initial_shacl_state(shacl_state)
    await populate_initial_cqljson_state(cqljson_state)
    await load_example_shacl_data_to_oxigraph()
    await load_example_cql_data_to_oxigraph()


@app.get("/shacl-profiles")
async def list_shacl_profiles(state: dict = Depends(get_global_shacl_state)):
    return JSONResponse(sorted(list(state.keys())))


@app.get("/cqljson")
async def list_cql(state: dict = Depends(get_global_cqljson_state)):
    return JSONResponse(sorted(list(state.keys())))


@app.get("/shacl-profiles/{prof_name}/{object}")
async def get_profile_data(
    prof_name: str,
    object: str,
    state: dict = Depends(get_global_shacl_state),
    pyoxi_store=Depends(get_shacl_pyoxi_store),
):
    object_instance = state[prof_name][object]
    if object == "sparql":
        sparql = await generate_sparql_query_from_shacl(prof_name)
        return PlainTextResponse(sparql)
    elif object == "results":
        try:
            sparql = await generate_sparql_query_from_shacl(prof_name)
        except Exception as e:
            logging.error(f"Error generating SPARQL query: {str(e)}")
            sparql = e
        try:
            results = pyoxi_store.query(
                sparql, default_graph=[NamedNode(RDFRAME[prof_name])]
            )
        except Exception as e:
            logging.error(f"Error executing SPARQL query: {str(e)}")
            return PlainTextResponse(e)
        ntriples = " .\n".join([str(r) for r in list(results)]) + " ."
        if ntriples == " .":
            return PlainTextResponse()
        ex_ns = state[prof_name]["example_data"].namespace_manager
        g = Graph(namespace_manager=ex_ns)
        g.parse(data=ntriples, format="ntriples")
        return PlainTextResponse(
            media_type="text/turtle", content=g.serialize(format="longturtle")
        )
    elif isinstance(object_instance, Graph):
        return PlainTextResponse(object_instance.serialize(format="longturtle"))
    elif isinstance(object_instance, dict):
        formatted_json = json.dumps(object_instance, indent=4)
        return Response(content=formatted_json, media_type="application/json")
    else:
        return PlainTextResponse(object_instance)


@app.put("/shacl-update/{prof_name}/{object}")
async def update_graph(
    prof_name: str,
    object: str,
    request: Request,
    pyoxi_store: Store = Depends(get_shacl_pyoxi_store),
    state: dict = Depends(get_global_shacl_state),
):
    data = await request.body()
    data = data.decode("utf-8")
    if object == "runtime_values":
        state[prof_name][object] = json.loads(data)
        return {"message": "Runtime values updated successfully"}
    else:
        g = Graph().parse(data=data, format="turtle")
        state[prof_name][object] = g
        if object == "example_data":
            pyoxi_store.clear_graph(NamedNode(RDFRAME[prof_name]))
            pyoxi_store.load(
                g.serialize(format="ntriples", encoding="utf-8"),
                "application/n-triples",
                to_graph=NamedNode(RDFRAME[prof_name]),
            )
        return {"message": "Graph updated successfully"}


@app.get("/cqljson/{prof_name}/{object}")
async def get_profile_data(
    prof_name: str,
    object: str,
    state: dict = Depends(get_global_cqljson_state),
    pyoxi_store=Depends(get_cql_pyoxi_store),
):
    object_instance = state[prof_name][object]
    if object == "sparql":
        cql_sparql = state[prof_name]["sparql"]
        return PlainTextResponse(cql_sparql)
    elif object == "results":
        try:
            sparql = state[prof_name]["sparql"]
            results = pyoxi_store.query(
                sparql, default_graph=[NamedNode(RDFRAME[prof_name])]
            )
            ntriples = " .\n".join([str(r) for r in list(results)]) + " ."
            if ntriples == " .":
                return PlainTextResponse()
            g = Graph().parse(data=ntriples, format="ntriples")
            g.bind("ex", Namespace("http://example.com/"))
            g.bind("landsat", Namespace("http://example.com/landsat/"))
            return PlainTextResponse(
                media_type="text/turtle", content=g.serialize(format="text/turtle")
            )
        except Exception as e:
            return PlainTextResponse(str(e))
    elif isinstance(object_instance, dict):
        formatted_json = json.dumps(object_instance, indent=4)
        return Response(content=formatted_json, media_type="application/json")
    elif isinstance(object_instance, Graph):
        return PlainTextResponse(object_instance.serialize())
    else:
        return PlainTextResponse(object_instance)


@app.put("/cqljson-update/{prof_name}/{object}")
async def update_graph(
    prof_name: str,
    object: str,
    request: Request,
    state: dict = Depends(get_global_cqljson_state),
    pyoxi_store: Store = Depends(get_cql_pyoxi_store),
):
    # Get raw data from the request
    data = await request.body()
    data = data.decode("utf-8")
    if object == "runtime_values":
        state[prof_name][object] = json.loads(data)
        return {"message": "Runtime values updated successfully"}
    elif object == "cql":
        updated_cql = json.loads(data)
        state[prof_name][object] = updated_cql
        # update the SPARQL query
        cql_sparql_obj = CQLParser(
            cql_json=updated_cql
        ).parse()  # cql in the state is contextual json ld
        cql_sparql = cql_sparql_obj.query_str
        state[prof_name]["sparql"] = cql_sparql
        return {"message": "CQL updated successfully"}
    elif object == "example_data":
        g = Graph().parse(data=data, format="turtle")
        state[prof_name][object] = g
        if object == "example_data":
            pyoxi_store.clear_graph(NamedNode(RDFRAME[prof_name]))
            pyoxi_store.load(
                g.serialize(format="ntriples", encoding="utf-8"),
                "application/n-triples",
                to_graph=NamedNode(RDFRAME[prof_name]),
            )
        return {"message": "Graph updated successfully"}


if __name__ == "__main__":
    uvicorn.run("app:app", port=8005, host="localhost", reload=True)
