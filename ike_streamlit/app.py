import streamlit as st
from st_cytoscape import cytoscape
import json
import requests
from sidebar_ import sidebar

st.set_page_config(layout="wide", page_title="IKE - Interactive Knowledge Explorer")

sidebar()

if "NODES" not in st.session_state:
    st.session_state["NODES"] = []
if "EDGES" not in st.session_state:
    st.session_state["EDGES"] = []


# Get Node Labels
nl_url = "http://localhost:8000/nodes/labels/"
headers = {"Content-type": "application/json", "Accept": "text/plain"}
nl = requests.get(nl_url, headers=headers)
nl_json = nl.json()
print(nl_json)

# Get Relationship Types
rt_url = "http://localhost:8000/relationships/types/"
headers = {"Content-type": "application/json", "Accept": "text/plain"}
rt = requests.get(rt_url, headers=headers)
rt_json = rt.json()
print(rt_json)


c1, c2, c3 = st.columns(3)
with c1:
    st.subheader("Filters")
    node_label_filtered = st.multiselect("Node Labels", nl_json, default=nl_json)
    relationship_type_filtered = st.multiselect(
        "Relationship Types", rt_json, default=rt_json
    )

    elements = []
    if st.button("Update"):

        params = {}

        # Get Nodes
        # if len(node_label_filtered) > 0:
        url = "http://localhost:8000/nodes"
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        params.update({"labels": [node_label_filtered]})
        n = requests.get(url, headers=headers, params=params)
        n_json = n.json()
        st.session_state["NODES"] = n_json

        # Get Relationships
        # if len(relationship_type_filtered) > 0:
        url = "http://localhost:8000/relationships"
        headers = {"Content-type": "application/json", "Accept": "text/plain"}

        params.update(
            {
                "types": [relationship_type_filtered],
            }
        )
        r = requests.get(url, headers=headers, params=params)
        r_json = r.json()
        st.session_state["EDGES"] = r_json

with c2:
    st.subheader("Graph")
    stylesheet = [
        {
            "selector": "node",
            "style": {"label": "data(label)", "width": 20, "height": 20},
        },
        {
            "selector": "edge",
            "style": {
                "width": 3,
                "curve-style": "bezier",
                "target-arrow-shape": "triangle",
            },
        },
    ]

    selected = cytoscape(
        st.session_state["NODES"] + st.session_state["EDGES"],
        stylesheet,
        key="graph",
    )

with c3:
    st.write("Selected Nodes")
    for n_name in selected["nodes"]:
        for element in elements:
            if element["data"]["label"] == n_name:
                with st.expander(f"{n_name}"):
                    st.json(element["data"])

    st.write("Selected Relationships")
    for rel in selected["edges"]:
        for element in elements:
            if element["data"]["label"] == rel:
                with st.expander(f"{rel}"):
                    st.json(element["data"])
