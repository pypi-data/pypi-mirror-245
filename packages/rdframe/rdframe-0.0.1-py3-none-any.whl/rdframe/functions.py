import json
import logging
from pathlib import Path

from pyoxigraph import NamedNode
from rdflib import Graph
from rdflib import Namespace

from src.rdframe.dependencies import (
    get_global_shacl_state,
    get_shacl_pyoxi_store,
    get_global_cqljson_state,
    get_cql_pyoxi_store,
)
from src.rdframe.x_to_sparql.cql2sparql import CQLParser
from src.rdframe.x_to_sparql.shacl2sparql import SHACLParser

RDFRAME = Namespace("https://rdframe.dev/")
ALTREXT = Namespace("http://www.w3.org/ns/dx/conneg/altr-ext#")
SRC_DIR = Path(__file__).parent

log = logging.getLogger(__name__)


async def load_example_shacl_data_to_oxigraph():
    shacl_state = get_global_shacl_state()
    pyoxi_store = get_shacl_pyoxi_store()
    for profile_name in shacl_state:
        example_data_g = shacl_state[profile_name]["example_data"]
        graph_name = NamedNode(str(RDFRAME[profile_name]))
        pyoxi_store.load(
            example_data_g.serialize(format="ntriples", encoding="utf-8"),
            "application/n-triples",
            to_graph=graph_name,
        )


async def load_example_cql_data_to_oxigraph():
    cql_state = get_global_cqljson_state()
    pyoxi_store = get_cql_pyoxi_store()
    for profile_name in cql_state:
        example_data_g = cql_state[profile_name]["example_data"]
        graph_name = NamedNode(str(RDFRAME[profile_name]))
        pyoxi_store.load(
            example_data_g.serialize(format="ntriples", encoding="utf-8"),
            "application/n-triples",
            to_graph=graph_name,
        )


async def populate_initial_shacl_state(state: dict):
    profiles_root = SRC_DIR / "data/shacl-profiles"
    for profile_dir in profiles_root.glob("*"):
        profile_name = profile_dir.stem
        try:
            profile_g = Graph().parse(profile_dir / "profile.ttl")
            example_data_g = Graph().parse(profile_dir / "example_data.ttl")
            endpoint_definition = Graph().parse(profile_dir / "endpoint_definition.ttl")
            runtime_values = json.loads(
                (profile_dir / "runtime_values.json").read_text()
            )
        except FileNotFoundError:
            logging.error(
                """For each profile_graph you must create a subdirectory under profiles, and create both a "
                          "\"profile.ttl\" file and an \"example_data.ttl\" file."""
            )
            raise
        state[profile_name] = {
            "profile": profile_g,
            "example_data": example_data_g,
            "results": Graph(),
            "sparql": None,
            "endpoint_definition": endpoint_definition,
            "runtime_values": runtime_values,
        }
        logging.info(
            f"Loaded {len(profile_g)} triples for profile_graph: {profile_name}"
        )


async def populate_initial_cqljson_state(state: dict):
    """
    Relies on a hardcoded directory structure with:
    1 * cql.json file
    1 * example_data.ttl file
    :param state:
    :return:
    """
    cql_root = SRC_DIR/"data/cql"
    dirs = [d for d in cql_root.glob("*") if d.is_dir()]
    context = json.load((cql_root / "context.json").open())
    for cql_dir in dirs:
        profile_name = cql_dir.stem
        try:
            cql = json.load((cql_dir / "cql.json").open())
            cql_sparql_obj = CQLParser(cql, context)
            cql_sparql_obj.generate_jsonld()
            cql_json_ld = cql_sparql_obj.cql_json
            cql_sparql_obj.parse()
            cql_sparql = cql_sparql_obj.query_str
            example_data_g = Graph().parse(cql_dir / "example_data.ttl")
        except Exception as e:
            logging.error(e)
            logging.error(
                """For each profile_graph you must create a subdirectory under profiles, and create both a "
                          "\"profile.ttl\" file and an \"example_data.ttl\" file."""
            )
            raise
        state[profile_name] = {
            "cql": cql_json_ld,
            "example_data": example_data_g,
            "results": Graph(),
            "sparql": cql_sparql,
        }
        logging.info(f"Loaded CQL json for {cql_dir}")


async def generate_sparql_query_from_shacl(profile_name):
    state = get_global_shacl_state()
    endpoint_definition = state[profile_name]["endpoint_definition"]
    profile = state[profile_name]["profile"]
    runtime_values = state[profile_name]["runtime_values"]
    sparql_parser = SHACLParserV2(runtime_values, endpoint_definition, profile)
    sparql_parser.generate_sparql()
    sparql = sparql_parser.sparql
    return sparql
