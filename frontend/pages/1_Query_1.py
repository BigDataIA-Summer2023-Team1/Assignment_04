import pandas as pd
import streamlit as st

from utils.generic import connect_and_execute_query


@st.cache_data(max_entries=1000)
def fetch_states_from_snowflake(connection=None):
    states_query = 'SELECT DISTINCT S_STATE  FROM store'
    states_results = connect_and_execute_query(states_query)


    # states = [result[0] for result in states_results]
    return [row.S_STATE for row in states_results.itertuples()]


# Streamlit App
st.subheader(
    'Customers who have returned items more than 20% more often than the average customer returns for a store in a given state for a given year.')

# Define the list of available agg fields
available_agg_fields = ["SR_RETURN_AMT", "SR_FEE", "SR_REFUNDED_CASH", "SR_RETURN_AMT_INC_TAX", "SR_REVERSED_CHARGE",
                        "SR_STORE_CREDIT", "SR_RETURN_TAX"]

# Fetch the list of states from Snowflake table
states = fetch_states_from_snowflake()
# Input fields
year = st.slider('Select Year', min_value=1998, max_value=2001, step=1, value=1998)
agg_field = st.selectbox('Select Agg Fields', available_agg_fields)
state = st.selectbox('Select State', states)


@st.cache_data(max_entries=1000)
def fetch_data(year, agg_field, state):
    query='''with customer_total_return as
            (select sr_customer_sk as ctr_customer_sk
            ,sr_store_sk as ctr_store_sk
            ,sum({agg_field}) as ctr_total_return
            from store_returns
            ,date_dim
            where sr_returned_date_sk = d_date_sk
            and d_year = {year}
            group by sr_customer_sk
            ,sr_store_sk)
            select  c_customer_id
            from customer_total_return ctr1
            ,store
            ,customer
            where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
            from customer_total_return ctr2
            where ctr1.ctr_store_sk = ctr2.ctr_store_sk)
            and s_store_sk = ctr1.ctr_store_sk
            and s_state = '{state}'
            and ctr1.ctr_customer_sk = c_customer_sk
            order by c_customer_id
            limit 100;'''.format(year=year, agg_field=agg_field, state=state)

    res = connect_and_execute_query(query)

    return res


if st.button('Fetch Data'):
    results = fetch_data(year, agg_field, state)
    # Display results
    st.subheader("Search Results")
    if not results.empty:

        st.table(results)
    else:
        st.write("No results found.")
