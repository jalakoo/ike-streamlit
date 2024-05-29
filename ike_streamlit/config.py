import streamlit as st
import os
from models import Neo4jCredentials

# Get all the real estate!
st.set_page_config(layout="wide", page_title="IKE - Interactive Knowledge Explorer")

# CONFIG
# Running here as keeping these in a separate file can result in failed Streamlit hot reloading
DB_URI_KEY = "SERVER_URL"
N4J_CREDS_KEY = "NEO4J_CREDS"
N4J_URI_KEY = "NEO4J_URI"
N4J_USERNAME_KEY = "NEO4J_USERNAME"
N4J_PASSWORD_KEY = "NEO4J_PASSWORD"
N4J_DATABASE_KEY = "NEO4J_DATABASE"
NODE_LABELS_KEY = "NODE_LABELS"
REL_TYPES_KEY = "EDGE_TYPES"
SCHEMA_KEY = "SCHEMA"
NODES_KEY = "NODES"
RELS_KEY = "EDGES"

ENV_DB_URI = os.getenv(DB_URI_KEY, "http://localhost:8000")
ENV_NEO4J_URI = os.getenv(N4J_URI_KEY, "bolt://localhost:7687")
ENV_NEO4J_USERNAME = os.getenv(N4J_USERNAME_KEY, "neo4j")
ENV_NEO4J_PASSWORD = os.getenv(N4J_PASSWORD_KEY, "password")
ENV_NEO4J_DATABASE = os.getenv(N4J_DATABASE_KEY, "neo4j")

if N4J_CREDS_KEY not in st.session_state:
    st.session_state[N4J_CREDS_KEY] = Neo4jCredentials(
        uri=ENV_NEO4J_URI,
        username=ENV_NEO4J_USERNAME,
        password=ENV_NEO4J_PASSWORD,
        database=ENV_NEO4J_DATABASE,
    )
if DB_URI_KEY not in st.session_state:
    st.session_state[DB_URI_KEY] = ENV_DB_URI

if SCHEMA_KEY not in st.session_state:
    st.session_state[SCHEMA_KEY] = []
if NODE_LABELS_KEY not in st.session_state:
    st.session_state[NODE_LABELS_KEY] = []
if REL_TYPES_KEY not in st.session_state:
    st.session_state[REL_TYPES_KEY] = []
if NODES_KEY not in st.session_state:
    st.session_state[NODES_KEY] = []
if RELS_KEY not in st.session_state:
    st.session_state[RELS_KEY] = []
