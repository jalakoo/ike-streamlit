import streamlit as st
from config import *
from models import Neo4jCredentials
import requests


# SIDEBAR
# Also keeping here instead of separate file due to hot reloading issues
# This section to provide .env loaded config + optionally overriding per session
def sidebar_ui():
    with st.sidebar:
        with st.expander("Neo4j Config", expanded=True):

            server_url = st.text_input(
                "Server URL",
                ENV_DB_URI,
                help="URL of a server configured to return Neo4j data as Cytoscape compatible JSON. NOT the URI of the Neo4j database itself.",
            )
            if server_url != st.session_state[DB_URI_KEY]:
                st.session_state[DB_URI_KEY] = server_url

            uri = st.text_input("URI", st.session_state[N4J_CREDS_KEY].uri)
            username = st.text_input(
                "Username", st.session_state[N4J_CREDS_KEY].username
            )
            password = st.text_input(
                "Password", st.session_state[N4J_CREDS_KEY].password, type="password"
            )

            database = st.text_input(
                "Database", st.session_state[N4J_CREDS_KEY].database
            )

            creds = Neo4jCredentials(
                uri=uri,
                username=username,
                password=password,
                database=database,
            )

            if creds != st.session_state[N4J_CREDS_KEY]:
                st.session_state[N4J_CREDS_KEY] = creds

            if st.button("Validate"):

                # Validate connection
                try:
                    v_url = server_url + "/validate/"
                    headers = {
                        "Content-type": "application/json",
                        "Accept": "text/plain",
                    }
                    response = requests.post(
                        v_url,
                        headers=headers,
                        data=st.session_state[N4J_CREDS_KEY].json(),
                    )
                    if response.status_code == 200:
                        # Code for successful request
                        st.success(f"Credentials valid and connected to {server_url}")
                    else:
                        # Code for handling error response
                        st.error(f"Problem connecting to {server_url}: {response.text}")

                except Exception as e:
                    st.error(f"Problem connecting to {server_url}: {e}")
