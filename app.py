# pylint: disable=missing-module-docstring
from typing import Optional

import duckdb
import streamlit as st

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# solution_df = duckdb.query(ANSWER_STR).df()

st.write(
    """
# SQL SRS
Spaced Repetition System SQL practice
"""
)

with st.sidebar:
    theme: Optional[str] = st.selectbox(
        "What would you like to review?",
        ("Joins", "GroupBy", "Window Functions"),
        index=None,
        placeholder="Select a theme...",
    )
    st.write(f"You selected: {theme}")

    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df()
    st.write(exercise)

st.header("Enter your code:")
query: Optional[str] = st.text_area(
    label="Enter your SQL query. Dataframe name: 'df'", key="user_input"
)
# if query:
#     st.write(f"Last query: {query}")
#     result = duckdb.query(query).df()
#     st.dataframe(result)
#
#     try:
#         result = result[solution_df.columns]
#         st.dataframe(result.compare(solution_df))
#     except KeyError:
#         st.write("Some columns are missing")
#
#     n_lines_difference = result.shape[0] - solution_df.shape[0]
#     if n_lines_difference != 0:
#         st.write(
#             f"Result has a {n_lines_difference} lines difference with the solution df"
#         )
#
# tab2, tab3 = st.tabs(["Tables", "Answer"])
#
# with tab2:
#     st.write("Table: beverages")
#     st.dataframe(beverages)
#
#     st.write("Table: food_items")
#     st.dataframe(food_items)
#
#     st.write("Expected:")
#     st.dataframe(solution_df)
#
# with tab3:
#     st.write(ANSWER_STR)
