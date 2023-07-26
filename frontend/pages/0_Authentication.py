import streamlit as st

from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from sqlalchemy.exc import DBAPIError


def connect_snowflake(user, password, account_identifier):
    engine = create_engine(URL(
        user=user,
        password=password,
        account=account_identifier,
        database='SNOWFLAKE_SAMPLE_DATA',
        schema='TPCDS_SF10TCL',
        warehouse='COMPUTE_WH',
        role='ACCOUNTADMIN',
        numpy=True,
    )
    )

    try:
        connection = engine.connect()
        st.success("Successfully Connected to Snowflake")

        return connection
    except DBAPIError as e:
        st.error("Couldn't connect to snowflake!!!, Please provide proper credentials")
    finally:
        engine.dispose()


st.subheader('Snowflake Authentication')

st.session_state['conn'] = None

user = st.text_input("User")
account_identifier = st.text_input("Account Identifier")
password = st.text_input("Password", type="password")

connect_to_db_btn = st.button("Connect to Snowflake")
if connect_to_db_btn:
    if not user:
        st.error("Snowflake username is required!!")
    if not account_identifier:
        st.error("Snowflake account_identifier is required!!")
    if not password:
        st.error("Snowflake password is required!!")

    if user and account_identifier and password:
        conn = connect_snowflake(user, password, account_identifier)
        st.session_state['conn'] = conn
