import streamlit as st
from config import *
import requests
from data_ import get_schema, get_labels


def connect():
    # Validate connection
    try:
        v_url = st.session_state[DB_URI_KEY] + "/validate/"
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

            get_labels()

            get_schema()

            st.session_state[DID_CONNECT_KEY] = True

            # Code for successful request
            st.success(
                f"Credentials valid and connected to {st.session_state[DB_URI_KEY]}"
            )
        else:
            # Code for handling error response
            st.session_state[DID_CONNECT_KEY] = False

            st.error(
                f"Problem connecting to {st.session_state[DB_URI_KEY]}: {response.text}"
            )

    except Exception as e:

        st.session_state[DID_CONNECT_KEY] = False

        st.error(f"Problem connecting to {st.session_state[DB_URI_KEY]}: {e}")


def config_ui():
    server_url = st.text_input(
        "Server URL",
        ENV_DB_URI,
        help="URL of a server configured to return Neo4j data as Cytoscape compatible JSON. NOT the URI of the Neo4j database itself.",
    )
    if server_url != st.session_state[DB_URI_KEY]:
        st.session_state[DB_URI_KEY] = server_url

    uri = st.text_input("URI", st.session_state[N4J_CREDS_KEY].uri)
    username = st.text_input("Username", st.session_state[N4J_CREDS_KEY].username)
    password = st.text_input(
        "Password", st.session_state[N4J_CREDS_KEY].password, type="password"
    )

    database = st.text_input("Database", st.session_state[N4J_CREDS_KEY].database)

    creds = Neo4jCredentials(
        uri=uri,
        username=username,
        password=password,
        database=database,
    )

    if creds != st.session_state[N4J_CREDS_KEY]:
        st.session_state[N4J_CREDS_KEY] = creds

    if creds.is_ready() is False:
        st.warning("Fill-in credentials then click 'Connect'")
    elif st.session_state[DID_CONNECT_KEY] == False and creds.is_ready():
        connect()

    if st.button("Connect"):
        connect()
        # # Validate connection
        # try:
        #     v_url = st.session_state[DB_URI_KEY] + "/validate/"
        #     headers = {
        #         "Content-type": "application/json",
        #         "Accept": "text/plain",
        #     }
        #     response = requests.post(
        #         v_url,
        #         headers=headers,
        #         data=st.session_state[N4J_CREDS_KEY].json(),
        #     )
        #     if response.status_code == 200:

        #         get_labels()

        #         get_schema()

        #         # Code for successful request
        #         st.success(f"Credentials valid and connected to {server_url}")
        #     else:
        #         # Code for handling error response
        #         st.error(
        #             f"Problem connecting to {st.session_state[DB_URI_KEY]}: {response.text}"
        #         )

        # except Exception as e:
        #     st.error(f"Problem connecting to {st.session_state[DB_URI_KEY]}: {e}")
