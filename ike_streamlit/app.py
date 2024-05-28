import streamlit as st
from st_cytoscape import cytoscape
from config import *
from sidebar_ui import sidebar_ui
from filters_ui import filters_ui

sidebar_ui()

# MAIN UI
c1, c2, c3 = st.columns([1, 3, 1])

with c1:
    filters_ui()

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
        for element in st.session_state[NODES_KEY]:
            if element["data"]["id"] == n_name:
                with st.expander(f"{n_name}"):
                    st.json(element["data"])

    st.write("Selected Relationships")
    for rel in selected["edges"]:
        for element in st.session_state[RELS_KEY]:
            if element["data"]["id"] == rel:
                with st.expander(f"{rel}"):
                    st.json(element["data"])
