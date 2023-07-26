## Assignment 04: Live application Links :octopus:

- Please use this application responsibly, as we have limited free credits remaining.

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://assignment04-64byggjesa-pd.a.run.app/)

[![codelabs](https://img.shields.io/badge/codelabs-4285F4?style=for-the-badge&logo=codelabs&logoColor=white)](https://codelabs-preview.appspot.com/?file_id=1n75MAmBIV-t9-6I4U4SAKOnjA9vzeoFxn-50t2yD8jM)

## Problem Statement :memo:
Leverage Streamlit for data insights drawn from computing queries on snowflake warehouse that models the decision support 
functions of a retail product supplier. The supporting schema contains vital business information, such as customer, order, and product data

Understand the generalized query model utilized by TPC-DS that allows the benchmark to capture important aspects of the 
interactive, iterative nature of on-line analytical processing (OLAP) queries, the longer-running complex queries of 
data mining and knowledge discovery, and the more planned behavior of well known report queries.

## Project Goals :dart:
Task -1:
1. Design streamlit screens for different bussiness use cases.
2. Screen to authenticate snowflake credentials to compute queries.
3. Input validation on metadata that need to be chosen by user as qualification substitutions that are passed to queries.


Task -2:
1. Connect to snowflake using toml file.
2. Leverage streamlit cache for better performance.
3. Dockerize the streamlit application.
4. Write github actions that continuously integrate and continuously Deploy to GCP Cloud Run.
5. Deploy the streamlit application on GCP cloud run.

## Technologies Used :computer:
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)
[![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
[![GitHub Actions](https://img.shields.io/badge/Github%20Actions-282a2e?style=for-the-badge&logo=githubactions&logoColor=367cfe)](https://github.com/features/actions)
[![Snowflake](https://img.shields.io/badge/snowflake-blue?style=for-the-badge&logo=SNOWFLAKE)](https://docs.snowflake.com/)
![Google Cloud Run](https://img.shields.io/badge/Google_Cloud-Green?style=for-the-badge&logo=google-cloud&logoColor=white)


## Data Source :flashlight:
1. https://docs.snowflake.com/en/user-guide/sample-data-tpcds


## Architecture Diagram
![img.png](architecture.png)

## Requirements
```
streamlit==1.23.1
pyarrow==10.0.1
snowflake-sqlalchemy
snowflake-snowpark-python
```

## Project Structure
```
📦 Assignment_04
├─ .github
│  └─ workflows
│     └─ deploy.yml
├─ .gitignore
├─ Makefile
├─ README.md
├─ docker-compose-local.yml
└─ frontend
   ├─ .gitignore
   ├─ Dockerfile
   ├─ Images
   │  ├─ Catalog_Returns.png
   │  ├─ Catalog_Sales.png
   │  ├─ Inventory.png
   │  ├─ Store_Sales.png
   │  ├─ Store_returns.png
   │  ├─ Web_Returns.png
   │  └─ Web_Sales.png
   ├─ main.py
   ├─ pages
   │  ├─ 0_Authentication.py
   │  ├─ 1_Query_1.py
   │  ├─ 2_Query_2.py
   │  ├─ 3_Query_3.py
   │  ├─ 4_Query_4.py
   │  ├─ 5_Query_5.py
   │  └─ 6_Query_6.py
   └─ requirements.txt
```
©generated by [Project Tree Generator](https://woochanleee.github.io/project-tree-generator)

## How to run Application locally
To run the application locally, follow these steps:
1. Clone the repository to get all the source code on your machine.

2. Install docker desktop on your system

3. Create a .env file in the root directory with the following variables:
    ``` 
      # Snowflake Variables
    ```

4. Once you have set up your environment variables, Start the application by executing
  ``` 
    Make build-up
  ```

5. Once the docker containers spin up, Access the application at following links
    ``` 
     1. Stremlit UI: http://localhost:30006/
    ```

6. To delete all active docker containers execute
     ``` 
     Make down
     ``` 

## References
1. Snowflake Sample Data: https://docs.snowflake.com/en/user-guide/sample-data-tpcds
2. Snowflake SQLAlchemy Connector: https://docs.snowflake.com/developer-guide/python-connector/sqlalchemy
3. TPC-DS Schemas: https://www.tpc.org/tpc_documents_current_versions/pdf/tpc-ds_v2.5.0.pdf
4. Queries: https://github.com/gregrahn/tpcds-kit
5. Streamlit: https://docs.streamlit.io/
6. Github Actions: https://docs.github.com/en/actions
7. Google Cloud Run: https://cloud.google.com/run#section-4
8. Github Action for GCloud Authentication: https://github.com/marketplace/actions/authenticate-to-google-cloud
9. Snowflake-Streamlit Connection :https://docs.streamlit.io/knowledge-base/tutorials/databases/snowflake
10. Streamlit Caching: https://docs.streamlit.io/library/advanced-features/caching
11. QueryViz: http://demo.queryvis.com/

## Learning Outcomes
1. To leverage streamlit for visualization/data insights drawn from snowflake computations.
2. Demoralising tables and querying according to the case.
3. Leverage github actions to continuously integrate and deploy on google cloud run.


## Team Information and Contribution

Name | Contributions 
--- | --- |
Sanjana Karra | Designed Streamlit screen for Query1, Query 2, Main Screen
Nikhil Reddy Polepally | Designed Streamlit screen for Query 5, Query 6, Documentation
Shiva Sai Charan Ruthala | Designed Streamlit screen for Query 3, Query 4, Deployment
