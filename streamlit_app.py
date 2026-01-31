import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# Title
st.title("Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

# Name input
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

params = {
    "account": "YVCYRQR-OKB08473",
    "user": "RAVSANDHU",
    "role": "SYSADMIN",
    "warehouse": "COMPUTE_WH",
    "database": "SMOOTHIES",
    "schema": "PUBLIC",
    "authenticator": "oauth",
    "token": "PASTE_TOKEN_HERE"
}

session = Session.builder.configs(params).create()
print(session.sql("SELECT CURRENT_USER(), CURRENT_ROLE()").collect())

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
