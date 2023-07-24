import pandas as pd
import streamlit as st


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


def fetch_query4_records(_conn, select_one, year, records_limit):
    query = prepare_query(select_one, year, records_limit)

    results = _conn.execute(query)

    return pd.DataFrame(results)



st.subheader("Find customers who spend more money via catalog than in stores. "
         "Identify preferred customers and their country of origin.")

with st.form("query", clear_on_submit=False):
    select_one = st.selectbox(
        'Select', ["t_s_secyear.customer_preferred_cust_flag", "t_s_secyear.customer_birth_country",
                   "t_s_secyear.customer_login", "t_s_secyear.customer_email_address"])
    st.write('You selected:', select_one)

    year = st.slider("year: ", 1998, 2001, 2001)
    records_limit = st.slider("No of records to display:", 10, 100, 15)

    show_data_btn = st.form_submit_button("Fetch Data")
    if show_data_btn:
        results = fetch_query4_records(st.session_state['conn'], select_one, year, records_limit)
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
