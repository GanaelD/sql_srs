# pylint: disable=missing-module-docstring
import io
from typing import Optional
import streamlit as st
import pandas as pd
import duckdb

CSV = """
beverage,price
Orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(CSV))

CSV2 = """
food_item,food_price
Cookie,2.5
Pain au chocolat,2
Muffin,3
"""
food_items = pd.read_csv(io.StringIO(CSV2))

ANSWER_STR = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

solution_df = duckdb.query(ANSWER_STR).df()

st.write(
    """
# SQL SRS
Spaced Repetition System SQL practice
"""
)

with st.sidebar:
    option: Optional[str] = st.selectbox(
        "What would you like to review?",
        ("Joins", "GroupBy", "Window Functions"),
        index=None,
        placeholder="Select a theme...",
    )

    st.write(f"You selected: {option}")

st.header("Enter your code:")
query: Optional[str] = st.text_area(
    label="Enter your SQL query. Dataframe name: 'df'", key="user_input"
)
if query:
    st.write(f"Last query: {query}")
    result = duckdb.query(query).df()
    st.dataframe(result)

    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError:
        st.write("Some columns are missing")

    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"Result has a {n_lines_difference} lines difference with the solution df"
        )

tab2, tab3 = st.tabs(["Tables", "Answer"])

with tab2:
    st.write("Table: beverages")
    st.dataframe(beverages)

    st.write("Table: food_items")
    st.dataframe(food_items)

    st.write("Expected:")
    st.dataframe(solution_df)

with tab3:
    st.write(ANSWER_STR)
