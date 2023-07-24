import streamlit as st

st.title('Assignment 04')
st.title('Schema Overview')
st.markdown("""
    The TPC-DS schema models the sales and sales returns process for an organization that employs three primary sales channels: stores, catalogs, and the Internet. The schema includes seven fact tables:
    
    - A pair of fact tables focused on the product sales and returns for each of the three channels.
    - A single fact table that models inventory for the catalog and internet sales channels.
    
    The sales channels are represented by the following fact tables:
    - Fact table for product sales in stores: `sales_stores`
    - Fact table for product sales through catalogs: `sales_catalogs`
    - Fact table for product sales on the Internet: `sales_internet`
    
    The sales returns for each channel are represented by the following fact tables:
    - Fact table for product returns in stores: `returns_stores`
    - Fact table for product returns through catalogs: `returns_catalogs`
    - Fact table for product returns on the Internet: `returns_internet`
    
    The inventory for the catalog and internet sales channels is represented by the following fact table:
    - Fact table for inventory management: `inventory`
    
    This Streamlit application allows you to interact with the data and explore different aspects of the sales and inventory process.
    """)

st.title('Store Sales ER-Diagram')
image_path = './Images/Store_Sales.png'  
st.image(image_path, caption='Store Sales ER Diagram', use_column_width=True)
st.markdown("""Each row in this table represents a single lineitem for a sale made through the store channel and recorded in the
store_sales fact table.""")

st.title('Store Returns ER-Diagram')
image_path = './Images/Store_returns.png'  
st.image(image_path, caption='Store Returns ER Diagram', use_column_width=True)
st.markdown("""Each row in this table represents a single lineitem for the return of an item sold through the store channel and
recorded in the store_returns fact table.""")

st.title('Catalog Sales ER-Diagram')
image_path = './Images/Catalog_Sales.png'  
st.image(image_path, caption='Catalog Sales ER Diagram', use_column_width=True)
st.markdown("""Each row in this table represents a single lineitem for a sale made through the catalog channel and recorded in
the catalog_sales fact table.""")

st.title('Catalog Returns ER-Diagram')
image_path = './Images/Catalog_Returns.png'  
st.image(image_path, caption='Catalog Returns ER Diagram', use_column_width=True)
st.markdown("""Each row in this table represents a single lineitem for the return of an item sold through the catalog channel and
recorded in the catalog_returns table.""")

st.title('Web Sales ER-Diagram')
image_path = './Images/Web_Sales.png'  
st.image(image_path, caption='Web Sales ER Diagram', use_column_width=True)
st.markdown("""Each row in this table represents a single lineitem for a sale made through the web channel and recorded in the
web_sales fact table.""")

st.title('Web Returns ER-Diagram')
image_path = './Images/Web_Returns.png'  
st.image(image_path, caption='Web Returns ER Diagram', use_column_width=True)
st.markdown("""Each row in this table represents a single lineitem for the return of an item sold through the web sales channel
and recorded in the web_returns table.
""")

st.title('Inventory ER-Diagram')
image_path = './Images/Inventory.png'  
st.image(image_path, caption='Inventory', use_column_width=True)
st.markdown("""Each row in this table represents the quantity of a particular item on-hand at a given warehouse during a
specific week.""")
