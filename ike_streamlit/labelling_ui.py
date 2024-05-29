import streamlit as st
from config import *


def labelling_ui():
    st.subheader("Labelling Options")
    st.write("Nodes")
    for node in st.session_state[NODE_LABELS_KEY]:
        with st.expander(f"{node}"):
            # TODO: Options to change label display by a Node property value
            st.write("TBD")

    st.write("Relationships")
    for rel in st.session_state[REL_TYPES_KEY]:
        with st.expander(f"{rel}"):
            # TODO: Options to change label display by a Relationship property value
            st.write("TBD")
