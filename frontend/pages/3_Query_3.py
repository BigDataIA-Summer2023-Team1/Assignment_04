import pandas as pd
import streamlit as st


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


def fetch_query3_records(_conn, aggregation, manufacturing_id, month, records_limit):
    query = prepare_query(aggregation, manufacturing_id, month, records_limit)

    results = _conn.execute(query).fetchall()

    df = pd.DataFrame(results)
    df['sum_agg'] = df['sum_agg'].astype(float).round(2)

    return df


st.subheader("Report the total extended sales price per item brand of a specific manufacturer for all sales "
         "in a specific month of the year.")


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
        results = fetch_query3_records(st.session_state['conn'], aggregation, manufacturing_id, month_map[month], records_limit)
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
