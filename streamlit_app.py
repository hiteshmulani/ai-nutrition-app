import streamlit as st
import json
from datetime import datetime
from openai import OpenAI

st.set_page_config(page_title="AI Nutrition Coach", layout="centered")

st.markdown("""
<style>
.main {background-color: #f8f8f8;}
.stTextInput, .stTextArea {font-size:16px;}
.stButton>button {background:#2c3e50;color:#fff;font-size:16px;border-radius:8px;padding:8px 16px;}
.stMarkdown {font-size:16px;}
</style>
""", unsafe_allow_html=True)

st.title("🥗 AI Nutrition Coach")
st.subheader("Minimal. Smart. Personalized.")

# Use Streamlit Secrets for API Key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Meal log setup
LOG_FILE = "meal_log.json"
try:
    with open(LOG_FILE, "r") as f:
        meal_log = json.load(f)
except FileNotFoundError:
    meal_log = []

# Tabs
tabs = st.tabs(["Analyze Meal", "Recipe Assistant", "Meal Log"])

# 1. Meal Analyzer
with tabs[0]:
    st.markdown("**Analyze your meal** and get nutrition feedback.")
    meal = st.text_area("🍽️ What did you eat?", placeholder="e.g. jowar roti, paneer bhurji")
    if st.button("Analyze Meal"):
        if not meal:
            st.error("Please enter your meal description.")
        else:
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a helpful nutritionist AI."},
                        {"role": "user", "content": f"Analyze this meal: {meal}. Provide calories, macros, vitamins, and suggestions."}
                    ],
                    temperature=0.7,
                    max_tokens=300
                )
                st.markdown("### 🤖 Nutrition Coach says:")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {str(e)}")

# 2. Recipe Assistant
with tabs[1]:
    st.markdown("**Get a healthy recipe** based on your inputs.")
    query = st.text_area("🍳 Ingredients or Goal", placeholder="e.g. jowar flour, curd, capsicum")
    if st.button("Get Recipe"):
        if not query:
            st.error("Please enter your query.")
        else:
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a healthy recipe assistant."},
                        {"role": "user", "content": f"Suggest a nutritious recipe using: {query}. Include title, ingredients, steps, nutrition."}
                    ],
                    temperature=0.7,
                    max_tokens=400
                )
                st.markdown("### 🍴 Recipe Assistant says:")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {str(e)}")

# 3. Meal Log
with tabs[2]:
    st.markdown("**Your meal history**")
    new_meal = st.text_input("📋 Log a new meal:", placeholder="e.g. grilled paneer with salad")
    if st.button("Log My Meal"):
        if not new_meal:
            st.error("Please enter a meal to log.")
        else:
            entry = {"meal": new_meal, "time": datetime.now().isoformat()}
            meal_log.append(entry)
            with open(LOG_FILE, "w") as f:
                json.dump(meal_log, f)
            st.success("Meal logged!")

    if meal_log:
        st.markdown("### 🕓 Logged Meals")
        for entry in reversed(meal_log[-10:]):
            st.write(f"📅 {entry['time'][:16]} — 🍽️ {entry['meal']}")
