import streamlit as st


def connect_and_execute_query(query):
    results = []

    try:
        conn = st.experimental_connection('snowpark')
        results = conn.query(query, ttl=600)

        return results
    except Exception as e:
        print("Error Connecting to snowflake or executing query: ", e)

        return results

