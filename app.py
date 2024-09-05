import streamlit as st
import pandas as pd
import duckdb
from typing import Optional

st.write("""
# SQL SRS
Spaced Repetition System SQL practice
""")

option = st.selectbox(
    "What would you like to review?",
    ("Joins", "GroupBy", "Window Functions"),
    index=None,
    placeholder="Select a theme..."
)

st.write(f"You selected: {option}")

data = {"a": [1, 2, 3], "b": [4, 5, 6]}
df = pd.DataFrame(data)

tab1, tab2, tab3 = st.tabs(["SQL", "Dog", "Owl"])

with tab1:
    query: Optional[str] = st.text_area(label="Enter your SQL query. Dataframe name: 'df'")
    if query:
        st.write(f"Last query: {query}")
        queried_df = duckdb.query(query).df()
        st.dataframe(queried_df)
    else:
        st.dataframe(df)

with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
