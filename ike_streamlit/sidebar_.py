import streamlit as st
import os
from neo4j_ import valid_credentials, Neo4jCredentials

N4J_URI_KEY = "NEO4J_URI"
N4J_USERNAME_KEY = "NEO4J_USERNAME"
N4J_PASSWORD_KEY = "NEO4J_PASSWORD"
N4J_DATABASE_KEY = "NEO4J_DATABASE"

ENV_NEO4J_URI = os.getenv(N4J_URI_KEY, "bolt://localhost:7687")
ENV_NEO4J_USERNAME = os.getenv(N4J_USERNAME_KEY, "neo4j")
ENV_NEO4J_PASSWORD = os.getenv(N4J_PASSWORD_KEY, "password")
ENV_NEO4J_DATABASE = os.getenv(N4J_DATABASE_KEY, "neo4j")

if N4J_URI_KEY not in st.session_state:
    st.session_state[N4J_URI_KEY] = ENV_NEO4J_URI
if N4J_USERNAME_KEY not in st.session_state:
    st.session_state[N4J_USERNAME_KEY] = ENV_NEO4J_USERNAME
if N4J_PASSWORD_KEY not in st.session_state:
    st.session_state[N4J_PASSWORD_KEY] = ENV_NEO4J_PASSWORD
if N4J_DATABASE_KEY not in st.session_state:
    st.session_state[N4J_DATABASE_KEY] = ENV_NEO4J_DATABASE


def sidebar():
    with st.sidebar:
        st.subheader("Neo4j Config")
        uri = st.text_input("URI", st.session_state[N4J_URI_KEY])
        username = st.text_input("Username", st.session_state[N4J_USERNAME_KEY])
        password = st.text_input(
            "Password", st.session_state[N4J_PASSWORD_KEY], type="password"
        )
        database = st.text_input("Database", st.session_state[N4J_DATABASE_KEY])

        if uri != st.session_state[N4J_URI_KEY]:
            st.session_state[N4J_URI_KEY] = uri
        if username != st.session_state[N4J_USERNAME_KEY]:
            st.session_state[N4J_USERNAME_KEY] = username
        if password != st.session_state[N4J_PASSWORD_KEY]:
            st.session_state[N4J_PASSWORD_KEY] = password
        if database != st.session_state[N4J_DATABASE_KEY]:
            st.session_state[N4J_DATABASE_KEY] = database

        if st.button("Connect"):
            # Validate connection
            creds = Neo4jCredentials(
                uri=st.session_state[N4J_URI_KEY],
                username=st.session_state[N4J_USERNAME_KEY],
                password=st.session_state[N4J_PASSWORD_KEY],
                database=st.session_state[N4J_DATABASE_KEY],
            )
            if valid_credentials(creds):
                st.success("Connected")
            else:
                st.error("Invalid credentials")
