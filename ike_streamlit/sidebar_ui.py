import streamlit as st
from config import *
from config_ui import config_ui


# SIDEBAR
# Also keeping here instead of separate file due to hot reloading issues
# This section to provide .env loaded config + optionally overriding per session
def sidebar_ui():
    with st.sidebar:
        with st.expander("Neo4j Config", expanded=True):
            config_ui()
