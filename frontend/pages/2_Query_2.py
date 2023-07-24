import streamlit as st
import pandas as pd
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

connection = st.session_state['conn']

# Streamlit app

st.subheader('Report of increase of weekly web and catalog sales from one year to the next year for each week.')
# Year selection using slider
year = st.slider('Select Year', min_value=1998, max_value=2001, step=1, value=1998)

def compute_data(year):
    query= '''with wscs as
            (select sold_date_sk
                    ,sales_price
            from (select ws_sold_date_sk sold_date_sk
                        ,ws_ext_sales_price sales_price
                    from web_sales 
                    union all
                    select cs_sold_date_sk sold_date_sk
                        ,cs_ext_sales_price sales_price
                    from catalog_sales)),
            wswscs as 
            (select d_week_seq,
                    sum(case when (d_day_name='Sunday') then sales_price else null end) sun_sales,
                    sum(case when (d_day_name='Monday') then sales_price else null end) mon_sales,
                    sum(case when (d_day_name='Tuesday') then sales_price else  null end) tue_sales,
                    sum(case when (d_day_name='Wednesday') then sales_price else null end) wed_sales,
                    sum(case when (d_day_name='Thursday') then sales_price else null end) thu_sales,
                    sum(case when (d_day_name='Friday') then sales_price else null end) fri_sales,
                    sum(case when (d_day_name='Saturday') then sales_price else null end) sat_sales
            from wscs
                ,date_dim
            where d_date_sk = sold_date_sk
            group by d_week_seq)
            select d_week_seq1
                ,round(sun_sales1/sun_sales2,2)
                ,round(mon_sales1/mon_sales2,2)
                ,round(tue_sales1/tue_sales2,2)
                ,round(wed_sales1/wed_sales2,2)
                ,round(thu_sales1/thu_sales2,2)
                ,round(fri_sales1/fri_sales2,2)
                ,round(sat_sales1/sat_sales2,2)
            from
            (select wswscs.d_week_seq d_week_seq1
                    ,sun_sales sun_sales1
                    ,mon_sales mon_sales1
                    ,tue_sales tue_sales1
                    ,wed_sales wed_sales1
                    ,thu_sales thu_sales1
                    ,fri_sales fri_sales1
                    ,sat_sales sat_sales1
            from wswscs,date_dim 
            where date_dim.d_week_seq = wswscs.d_week_seq and
                    d_year = {year}) y,
            (select wswscs.d_week_seq d_week_seq2
                    ,sun_sales sun_sales2
                    ,mon_sales mon_sales2
                    ,tue_sales tue_sales2
                    ,wed_sales wed_sales2
                    ,thu_sales thu_sales2
                    ,fri_sales fri_sales2
                    ,sat_sales sat_sales2
            from wswscs
                ,date_dim 
            where date_dim.d_week_seq = wswscs.d_week_seq and
                    d_year = {next_year}) z
            where d_week_seq1=d_week_seq2-53
            order by d_week_seq1;
    '''.format(year=year, next_year=year+1)
       
    results = connection.execute(query)    
    return results
    
if st.button('Fetch Data'):
    results = compute_data(year)
     # Display results
    st.subheader("Search Results")
    if results:
        # Convert results to a DataFrame
        df = pd.DataFrame(results)
        # Display the DataFrame as a table
        st.table(df)
    else:
        st.write("No results found.")