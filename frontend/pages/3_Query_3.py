import streamlit as st
import numpy as np
import pandas as pd

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
        print("================================================================")

        return connection
    except DBAPIError as e:
        st.error("Couldn't connect to snowflake!!!, Please provide proper credentials")
    finally:
        engine.dispose()


def prepare_query(aggregation, manufacturing_id, month, records_limit):
    return """
        select dt.d_year 
           ,item.i_brand_id brand_id 
           ,item.i_brand brand
           ,sum({aggregation}) sum_agg
         from  date_dim dt 
              ,store_sales
              ,item
         where dt.d_date_sk = store_sales.ss_sold_date_sk
           and store_sales.ss_item_sk = item.i_item_sk
           and item.i_manufact_id = {manufacturing_id}
           and dt.d_moy={month}
         group by dt.d_year
              ,item.i_brand
              ,item.i_brand_id
         order by dt.d_year
                 ,sum_agg desc
                 ,brand_id
         limit {records_limit};
    """.format(aggregation=aggregation, manufacturing_id=manufacturing_id, month=month, records_limit=records_limit)


def fetch_records(conn, aggregation, manufacturing_id, month, records_limit):
    print("conn: ", conn)
    query = prepare_query(aggregation, manufacturing_id, month, records_limit)

    results = conn.execute(query)

    return pd.DataFrame(results)


st.subheader('Query 3')
st.write("Report the total extended sales price per item brand of a specific manufacturer for all sales "
         "in a specific month of the year.")

st.session_state['conn'] = None
with st.sidebar:
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


with st.form("query", clear_on_submit=False):
    # Create two columns
    col1, col2 = st.columns(2)

    with col1:
        aggregation = st.selectbox(
            'Aggregation on', ["ss_ext_sales_price", "ss_sales_price", "ss_ext_discount_amt", "ss_net_profit"])
        st.write('You selected:', aggregation)

    with col2:
        month_map = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9,
                     "Oct": 10, "Nov": 11, "Dec": 12}

        month = st.selectbox(
            'Month', ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])

        st.write('Month selected:', month)

    manufacturing_id = st.slider("Manufacturing ID:", 1, 1000, 100)
    records_limit = st.slider("No of records to display:", 10, 100, 15)

    show_data_btn = st.form_submit_button("Fetch Data")

    if show_data_btn:
        results = fetch_records(st.session_state['conn'], aggregation, manufacturing_id, month_map[month], records_limit)
        custom_style = """
            <style>
            .custom-text-box {
                border: 2px solid green;
                padding: 10px;
                border-radius: 5px;
            }
            </style>
        """

        query = prepare_query(aggregation, manufacturing_id, month_map[month], records_limit)

        # Display the text inside the styled box
        st.write(query)
        st.markdown('<div class="custom-text-box">' + query + '</div>', unsafe_allow_html=True)
        st.table(results)

