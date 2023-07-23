import streamlit as st
import numpy as np
import pandas as pd

from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from sqlalchemy.exc import DBAPIError


def connect_snowflake(user, password, account_identifier):
    connection = None

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
        if connection:
            connection.close()
        engine.dispose()


def prepare_query(select_one, year, records_limit):
    return """
        with year_total as (
         select c_customer_id customer_id
               ,c_first_name customer_first_name
               ,c_last_name customer_last_name
               ,c_preferred_cust_flag customer_preferred_cust_flag
               ,c_birth_country customer_birth_country
               ,c_login customer_login
               ,c_email_address customer_email_address
               ,d_year dyear
               ,sum(((ss_ext_list_price-ss_ext_wholesale_cost-ss_ext_discount_amt)+ss_ext_sales_price)/2) year_total
               ,'s' sale_type
         from customer
             ,store_sales
             ,date_dim
         where c_customer_sk = ss_customer_sk
           and ss_sold_date_sk = d_date_sk
         group by c_customer_id
                 ,c_first_name
                 ,c_last_name
                 ,c_preferred_cust_flag
                 ,c_birth_country
                 ,c_login
                 ,c_email_address
                 ,d_year
         union all
         select c_customer_id customer_id
               ,c_first_name customer_first_name
               ,c_last_name customer_last_name
               ,c_preferred_cust_flag customer_preferred_cust_flag
               ,c_birth_country customer_birth_country
               ,c_login customer_login
               ,c_email_address customer_email_address
               ,d_year dyear
               ,sum((((cs_ext_list_price-cs_ext_wholesale_cost-cs_ext_discount_amt)+cs_ext_sales_price)/2) ) year_total
               ,'c' sale_type
         from customer
             ,catalog_sales
             ,date_dim
         where c_customer_sk = cs_bill_customer_sk
           and cs_sold_date_sk = d_date_sk
         group by c_customer_id
                 ,c_first_name
                 ,c_last_name
                 ,c_preferred_cust_flag
                 ,c_birth_country
                 ,c_login
                 ,c_email_address
                 ,d_year
        union all
         select c_customer_id customer_id
               ,c_first_name customer_first_name
               ,c_last_name customer_last_name
               ,c_preferred_cust_flag customer_preferred_cust_flag
               ,c_birth_country customer_birth_country
               ,c_login customer_login
               ,c_email_address customer_email_address
               ,d_year dyear
               ,sum((((ws_ext_list_price-ws_ext_wholesale_cost-ws_ext_discount_amt)+ws_ext_sales_price)/2) ) year_total
               ,'w' sale_type
         from customer
             ,web_sales
             ,date_dim
         where c_customer_sk = ws_bill_customer_sk
           and ws_sold_date_sk = d_date_sk
         group by c_customer_id
                 ,c_first_name
                 ,c_last_name
                 ,c_preferred_cust_flag
                 ,c_birth_country
                 ,c_login
                 ,c_email_address
                 ,d_year
                 )
        select t_s_secyear.customer_id
                         ,t_s_secyear.customer_first_name
                         ,t_s_secyear.customer_last_name
                         ,{select_one}
         from year_total t_s_firstyear
             ,year_total t_s_secyear
             ,year_total t_c_firstyear
             ,year_total t_c_secyear
             ,year_total t_w_firstyear
             ,year_total t_w_secyear
         where t_s_secyear.customer_id = t_s_firstyear.customer_id
           and t_s_firstyear.customer_id = t_c_secyear.customer_id
           and t_s_firstyear.customer_id = t_c_firstyear.customer_id
           and t_s_firstyear.customer_id = t_w_firstyear.customer_id
           and t_s_firstyear.customer_id = t_w_secyear.customer_id
           and t_s_firstyear.sale_type = 's'
           and t_c_firstyear.sale_type = 'c'
           and t_w_firstyear.sale_type = 'w'
           and t_s_secyear.sale_type = 's'
           and t_c_secyear.sale_type = 'c'
           and t_w_secyear.sale_type = 'w'
           and t_s_firstyear.dyear =  {year}
           and t_s_secyear.dyear = {next_year}
           and t_c_firstyear.dyear =  {year}
           and t_c_secyear.dyear =  {next_year}
           and t_w_firstyear.dyear = {year}
           and t_w_secyear.dyear = {next_year}
           and t_s_firstyear.year_total > 0
           and t_c_firstyear.year_total > 0
           and t_w_firstyear.year_total > 0
           and case when t_c_firstyear.year_total > 0 then t_c_secyear.year_total / t_c_firstyear.year_total else null end
                   > case when t_s_firstyear.year_total > 0 then t_s_secyear.year_total / t_s_firstyear.year_total else null end
           and case when t_c_firstyear.year_total > 0 then t_c_secyear.year_total / t_c_firstyear.year_total else null end
                   > case when t_w_firstyear.year_total > 0 then t_w_secyear.year_total / t_w_firstyear.year_total else null end
         order by t_s_secyear.customer_id
                 ,t_s_secyear.customer_first_name
                 ,t_s_secyear.customer_last_name
                 ,{select_one}
        limit {records_limit};
    """.format(select_one=select_one, year=year, next_year=year+1, records_limit=records_limit)


def fetch_records(conn, select_one, year, records_limit):
    print("conn: ", conn)
    query = prepare_query(select_one, year, records_limit)

    results = conn.execute(query)

    return pd.DataFrame(results)


st.subheader('Query 4')
st.write("Find customers who spend more money via catalog than in stores. "
         "Identify preferred customers and their country of origin.")


conn = None
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
            print("try - conn: ", conn)

with st.form("query", clear_on_submit=False):
    select_one = st.selectbox(
        'Select', ["t_s_secyear.customer_preferred_cust_flag", "t_s_secyear.customer_birth_country",
                   "t_s_secyear.customer_login", "t_s_secyear.customer_email_address"])
    st.write('You selected:', select_one)

    year = st.slider("year: ", 1998, 2001, 2001)
    records_limit = st.slider("No of records to display:", 10, 100, 15)

    show_data_btn = st.form_submit_button("Fetch Data")

    if show_data_btn:
        results = fetch_records(conn, select_one, year, records_limit)
        custom_style = """
            <style>
            .custom-text-box {
                border: 2px solid green;
                padding: 10px;
                border-radius: 5px;
            }
            </style>
        """

        query = prepare_query(select_one, year, records_limit)

        # Display the text inside the styled box
        st.write(query)
        st.markdown('<div class="custom-text-box">' + query + '</div>', unsafe_allow_html=True)
        st.table(results)
