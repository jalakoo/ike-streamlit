import streamlit as st
from config import *
import requests


def get_labels():

    # Get Node Labels
    nl_url = st.session_state[DB_URI_KEY] + "/nodes/labels/"
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    try:
        nl = requests.post(
            nl_url, headers=headers, data=st.session_state[N4J_CREDS_KEY].json()
        )
        nl.raise_for_status()
        nl_json = nl.json()
        print(f"Node labels found: {nl_json}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error accessing endpoint: {e}")

    # Get Relationship Types
    rt_url = st.session_state[DB_URI_KEY] + "/relationships/types/"
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    try:
        rt = requests.post(
            rt_url, headers=headers, data=st.session_state[N4J_CREDS_KEY].json()
        )
        rt_json = rt.json()
        print(f"Relationship Types found: {rt_json}")
    except Exception as e:
        st.error(f"Error accessing endpoint: {e}")

    st.session_state[NODE_LABELS_KEY] = nl_json
    st.session_state[REL_TYPES_KEY] = rt_json


def get_schema():
    s_url = st.session_state[DB_URI_KEY] + "/schema/"
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    s_payload = st.session_state[N4J_CREDS_KEY].dict()
    s = requests.post(s_url, headers=headers, json=s_payload)
    print(f"body: {s.text}")
    s_json = s.json()
    st.session_state[SCHEMA_KEY] = s_json


def refresh_graph(node_label_filtered, relationship_type_filtered):

    # Get Nodes (Required)
    n_url = st.session_state[DB_URI_KEY] + "/nodes/"
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    payload = {"creds": st.session_state[N4J_CREDS_KEY].dict()}
    payload.update({"labels": node_label_filtered})

    n = requests.post(n_url, headers=headers, json=payload)

    n_json = n.json()

    if not isinstance(n_json, list):
        st.error(
            f"Unexpected response data from Neo4j: {n_json}. Expected a list of Node records."
        )
    else:
        st.session_state[NODES_KEY] = n_json

    # Get Relationships (Optional)
    # NOTE: Putting this into a function call will NOT work. Streamlit will refresh before this would complete
    url = st.session_state[DB_URI_KEY] + "/relationships"

    payload.update(
        {
            "types": relationship_type_filtered,
        }
    )

    print(f"Requesting relationships with payload: {payload}")

    r = requests.post(url, headers=headers, json=payload)
    r_json = r.json()
    if not isinstance(r_json, list):
        msg = f"Unexpected response data from Neo4j: {r_json}. Expected a list of Relationship records."
        print(msg)
        st.error(msg)
        st.session_state[DID_REFRESH_KEY] = False
    else:
        print(f"Got {len(r_json)} relationships")
        if len(r_json) > 0:
            print(f"First relationship: {r_json[0]}")
        st.session_state[RELS_KEY] = r_json
        st.session_state[DID_REFRESH_KEY] = True


def get_relationships(creds: dict, url: str, labels: list[str], types: list[str] = []):
    # url = st.session_state[DB_URI_KEY] + "/relationships"
    headers = {
        "Content-type": "application/json",
        "Accept": "text/plain",
    }

    payload = {
        "credentials": creds,
        "labels": labels,
        "types": types,
    }

    print(f"Requesting relationships with payload: {payload}")

    r = requests.post(url, headers=headers, json=payload)
    r_json = r.json()
    if not isinstance(r_json, list):
        msg = f"Unexpected response data from Neo4j: {r_json}. Expected a list of Relationship records."
        raise Exception(msg)
    else:
        print(f"Got {len(r_json)} relationships")
        if len(r_json) > 0:
            print(f"First relationship: {r_json[0]}")
        return r_json
