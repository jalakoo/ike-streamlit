import streamlit as st
from config import *
import requests


def filters_ui():
    st.subheader("Filters")

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

    # Display Node + Relationship Options
    node_label_filtered = st.multiselect(
        "Node Labels",
        nl_json,
        default=nl_json,
        help="Select the node labels to filter by. Leaving empty will return ALL available Nodes",
    )
    relationship_type_filtered = st.multiselect(
        "Relationship Types",
        rt_json,
        default=rt_json,
        help="Select the relationship types to filter by. Leaving empty will return ALL available Relationships",
    )

    if st.button("Refresh"):

        # Get Nodes (Required)
        url = st.session_state[DB_URI_KEY] + "/nodes/"
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        payload = {"creds": st.session_state[N4J_CREDS_KEY].dict()}
        payload.update({"labels": node_label_filtered})

        n = requests.post(url, headers=headers, json=payload)

        n_json = n.json()

        if not isinstance(n_json, list):
            st.error(
                f"Unexpected response data from Neo4j: {n_json}. Expected a list of Node records."
            )
        else:
            st.session_state["NODES"] = n_json

        # Get Relationships (Optional)
        if relationship_type_filtered is None or len(relationship_type_filtered) == 0:
            st.session_state["EDGES"] = []
        else:
            url = st.session_state[DB_URI_KEY] + "/relationships"
            headers = {
                "Content-type": "application/json",
                "Accept": "text/plain",
            }

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
            else:
                print(f"Got {len(r_json)} relationships")
                if len(r_json) > 0:
                    print(f"First relationship: {r_json[0]}")
                st.session_state["EDGES"] = r_json
