import streamlit as st
import pandas as pd
import duckdb
import io
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

csv = """
beverage,price
Orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(csv))

csv2 = """
food_item,food_price
Cookie,2.5
Pain au chocolat,2
Muffin,3
"""
food_items = pd.read_csv(io.StringIO(csv2))

answer = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

solution = duckdb.query(answer).df()

st.header("Enter your code:")
query: Optional[str] = st.text_area(label="Enter your SQL query. Dataframe name: 'df'", key="user_input")
if query:
    st.write(f"Last query: {query}")
    queried_df = duckdb.query(query).df()
    st.dataframe(queried_df)

tab2, tab3 = st.tabs(["Tables", "Answer"])

with tab2:
    st.write("Table: beverages")
    st.dataframe(beverages)

    st.write("Table: food_items")
    st.dataframe(food_items)

    st.write("Expected:")
    st.dataframe(solution)

with tab3:
    st.write(answer)
