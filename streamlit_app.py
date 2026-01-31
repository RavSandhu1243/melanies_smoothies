import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# Title
st.title("Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

# Name input
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

# --- Snowpark session setup ---
connection_parameters = {
    "account": st.secrets["connections"]["snowflake"]["account"],
    "user": st.secrets["connections"]["snowflake"]["user"],
    "role": st.secrets["connections"]["snowflake"]["role"],
    "warehouse": st.secrets["connections"]["snowflake"]["warehouse"],
    "database": st.secrets["connections"]["snowflake"]["database"],
    "schema": st.secrets["connections"]["snowflake"]["schema"],
    "authenticator": "oauth",
    "token": st.secrets["connections"]["snowflake"]["token"],
}

session = Session.builder.configs(connection_parameters).create()

# --- Load fruit options ---
fruit_df = session.table("fruit_options").select(col("FRUIT_NAME"))
fruit_list = [row["FRUIT_NAME"] for row in fruit_df.collect()]  # Convert to Python list

# --- Multiselect widget ---
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# --- Insert order when button clicked ---
if ingredients_list and name_on_order:
    ingredients_string = " ".join(ingredients_list)

    insert_stmt = f"""
        INSERT INTO orders(ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    if st.button("Submit Order"):
        session.sql(insert_stmt).collect()
        st.success("Your Smoothie is ordered! ✅")
