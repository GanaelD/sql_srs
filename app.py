# pylint: disable=missing-module-docstring
import os
import sys
import subprocess
import logging
from typing import Optional

import duckdb
import streamlit as st

logging.basicConfig(level=logging.DEBUG)

# Check that the 'data' folder containing the DB exists. Otherwise create it
folder_content = os.listdir()
if "data" not in folder_content:
    logging.debug(f"Current directory content: {folder_content}")
    logging.debug("Creating data folder")
    os.mkdir("data")

# If the DB doesn't exist, create it using init_db.py script
DB_FILE_NAME = "exercises_sql_tables.duckdb"
if DB_FILE_NAME not in os.listdir("data"):
    subprocess.run([sys.executable, "init_db.py"])


con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

st.write(
    """
# SQL SRS
Spaced Repetition System SQL practice
"""
)

with st.sidebar:
    theme: Optional[str] = st.selectbox(
        "What would you like to review?",
        ("joins", "group_by", "window_functions"),
        index=None,
        placeholder="Select a theme...",
    )
    st.write(f"You selected: {theme}")

    exercises = (
        con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'")
        .df()
        .sort_values("last_reviewed")
        .reset_index()
    )
    st.dataframe(exercises)

    exercise_name = exercises.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r", encoding="utf-8") as f:
        answer = f.read()

    solution_df = con.execute(answer).df()

st.header("Enter your code:")
query: Optional[str] = st.text_area(label="Your SQL query goes here", key="user_input")
if query:
    st.write(f"Last query: {query}")
    result = con.execute(query).df()
    st.dataframe(result)

    try:
        result = result[solution_df.columns]
        difference_df = result.compare(
            solution_df, result_names=("your_df", "expected_df")
        )
        if difference_df.shape[0] > 0:
            st.write("**Incorrect dataframe!** Here are the differences:")
            st.dataframe(difference_df)
    except KeyError:
        st.write("Some columns are missing")

    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"Result has a {n_lines_difference} lines difference with the solution df"
        )

tab2, tab3 = st.tabs(["Tables", "Answer"])

with tab2:
    exercise_tables = exercises.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"Table: {table}")
        table_df = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(table_df)

    st.write("Expected:")
    st.dataframe(solution_df)

with tab3:
    st.write(answer)
