import streamlit as st
from st_cytoscape import cytoscape
from config import *
from sidebar_ui import sidebar_ui
from filters_ui import filters_ui
from data_ import get_schema, refresh_graph

sidebar_ui()

# MAIN UI
c1, c2, c3 = st.columns(3)

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

with c1:
    with st.container(border=True):
        st.subheader("Data Model")
        selected_datamodel = cytoscape(
            st.session_state[SCHEMA_KEY],
            stylesheet,
            key="data-model",
            height="200px",
        )

    with st.container(border=True):
        # st.write("Node Labels")
        selected_nodes = []
        for n_name in selected_datamodel["nodes"]:
            for element in st.session_state[SCHEMA_KEY]:
                if element["data"]["id"] == n_name:
                    label = element["data"]["label"]
                    selected_nodes.append(label)
                    with st.expander(f"{label}"):
                        st.json(element["data"])
                        # TODO: Allow for key selection

        # st.write("Relationship Types")
        selected_rels = []
        for rel in selected_datamodel["edges"]:
            for element in st.session_state[SCHEMA_KEY]:
                if element["data"]["id"] == rel:
                    label = element["data"]["label"]
                    selected_rels.append(label)
                    with st.expander(f"{label}"):
                        st.json(element["data"])
                        # TODO: Allow for key selection

    if st.button("Refresh Graph", key="refresh-graph"):
        refresh_graph(selected_nodes, selected_rels)

with c2:
    with st.container(border=True):
        st.subheader("Graph Data")
        selected_data = cytoscape(
            st.session_state[NODES_KEY] + st.session_state[RELS_KEY],
            stylesheet,
            key="graph",
            height="600px",
        )


with c2:
    with st.container(border=True):
        st.subheader("SELECTIONS")
        st.write("Nodes")
        for n_name in selected_data["nodes"]:
            for element in st.session_state[NODES_KEY]:
                if element["data"]["id"] == n_name:
                    with st.expander(f"{n_name}"):
                        st.json(element["data"])

        st.write("Relationships")
        for rel in selected_data["edges"]:
            for element in st.session_state[RELS_KEY]:
                if element["data"]["id"] == rel:
                    with st.expander(f"{rel}"):
                        st.json(element["data"])
