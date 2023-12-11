from src.rdframe.state import (
    global_state_shacl_profiles,
    shacl_pyoxi_store,
    cql_pyoxi_store,
    global_state_cqljson_profiles,
)


def get_global_shacl_state():
    return global_state_shacl_profiles


def get_global_cqljson_state():
    return global_state_cqljson_profiles


def get_shacl_pyoxi_store():
    return shacl_pyoxi_store


def get_cql_pyoxi_store():
    return cql_pyoxi_store
