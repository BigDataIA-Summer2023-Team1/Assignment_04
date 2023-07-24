import streamlit as st
import pandas as pd
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

connection = st.session_state['conn']

# Streamlit app
st.subheader('List all the states with at least 10 customers who during a given month bought items with the price tag at least 20 percent higher than the average price of items in the same category.')

# Input fields

salesYear = st.selectbox(
    'Select Sales Year',
    (1998, 1999, 2000, 2001, 2002))

st.write('Year selected:', salesYear)

salesMonth = st.selectbox(
    'Select Sales Month',
    (1, 2, 3, 4, 5, 6, 7))

st.write('Month selected:', salesMonth)

def compute_results(salesYear, salesMonth):
    query = ''' select a.ca_state state, count(*) cnt
        from customer_address a
            ,customer c
            ,store_sales s
            ,date_dim d
            ,item i
        where       a.ca_address_sk = c.c_current_addr_sk
            and c.c_customer_sk = s.ss_customer_sk
            and s.ss_sold_date_sk = d.d_date_sk
            and s.ss_item_sk = i.i_item_sk
            and d.d_month_seq = 
                (select distinct (d_month_seq)
                from date_dim
                    where d_year = {salesYear}
                    and d_moy =  {salesMonth})
            and i.i_current_price > 1.2 * 
                    (select avg(j.i_current_price) 
                from item j 
                where j.i_category = i.i_category)
        group by a.ca_state
        having count(*) >= 10
        order by cnt, a.ca_state 
        limit 100;'''.format(salesYear = salesYear, salesMonth = salesMonth)
    results = connection.execute(query)
    return results

# Search button
if st.button("Fetch Data"):
    # Perform the search
    results = compute_results(salesYear, salesMonth)
    # Display results
    st.subheader("Query Results")
    if results:
        # Convert results to a DataFrame
        df = pd.DataFrame(results)
        # Display the DataFrame as a table
        st.table(df)
    else:
        st.write("No results found.")

