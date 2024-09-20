# pylint: disable=missing-module-docstring
import logging
import os
import subprocess
import sys
from typing import Optional

import duckdb
import streamlit as st

logging.basicConfig(level=logging.DEBUG)


def setup() -> None:
    """
    A function to setup the required folders for the app to run
    """
    # Check that the 'data' folder containing the DB exists. Otherwise, create it
    folder_content = os.listdir()
    if "data" not in folder_content:
        logging.debug("Current directory content: %s", folder_content)
        logging.debug("Creating data folder")
        os.mkdir("data")

    # If the DB doesn't exist, create it using init_db.py script
    db_file_name = "exercises_sql_tables.duckdb"
    if db_file_name not in os.listdir("data"):
        subprocess.run([sys.executable, "init_db.py"], check=False)


def check_user_solution(user_query: str) -> None:
    """
    A function to compare the SQL query of the user to the solution by:
    1. Comparing the columns of the solution and the user's result
    2. Comparing the values of the solution and the user's result
    :param user_query: The SQL query of the user
    """
    st.write(f"Last query: {user_query}")
    result = con.execute(user_query).df()
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


setup()
con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

st.write(
    """
# SQL SRS
Spaced Repetition System SQL practice
"""
)

with st.sidebar:
    available_themes_df = con.execute("SELECT DISTINCT theme FROM memory_state").df()
    theme: Optional[str] = st.selectbox(
        "What would you like to review?",
        available_themes_df["theme"].unique(),
        index=None,
        placeholder="Select a theme...",
    )
    if theme:
        st.write(f"You selected: {theme}")
        select_exercise_query = f"SELECT * FROM memory_state WHERE theme = '{theme}'"  # pylint: disable=invalid-name
    else:
        select_exercise_query = (  # pylint: disable=invalid-name
            "SELECT * FROM memory_state"
        )

    exercises = (
        con.execute(select_exercise_query)
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
    check_user_solution(query)

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
