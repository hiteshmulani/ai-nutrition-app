import streamlit as st
import openai
import json
from datetime import datetime

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

# Load or create meal log file
LOG_FILE = "meal_log.json"
try:
    with open(LOG_FILE, "r") as f:
        meal_log = json.load(f)
except FileNotFoundError:
    meal_log = []

tab = st.tabs(["Analyze Meal", "Recipe Assistant", "Meal Log"])

with tab[0]:
    st.markdown("**Analyze your meal** and get nutrition feedback.")
    api_key = st.text_input("🔐 OpenAI API Key", type="password")
    meal = st.text_area("🍽️ What did you eat?", placeholder="e.g. jowar roti, paneer bhurji")
    if st.button("Analyze Meal"):
        if not api_key or not meal:
            st.error("Enter your API key and meal.")
        else:
            openai.api_key = api_key
            resp = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful nutritionist AI."},
                    {"role": "user", "content": f"Analyze this meal: {meal}. Provide calories, macros, vitamins, and suggestions."}
                ],
                temperature=0.7,
                max_tokens=300
            )
            st.markdown("### 🤖 Nutrition Coach says:")
            st.markdown(resp.choices[0].message.content)

with tab[1]:
    st.markdown("**Get a healthy recipe** based on your inputs.")
    api_key2 = st.text_input("🔐 OpenAI API Key", type="password", key="recipe_key")
    query = st.text_area("🍳 Ingredients or Goal", placeholder="e.g. jowar flour, curd, capsicum")
    if st.button("Get Recipe"):
        if not api_key2 or not query:
            st.error("Enter API key & query.")
        else:
            openai.api_key = api_key2
            resp2 = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a healthy recipe assistant."},
                    {"role": "user", "content": f"Suggest a nutritious recipe using: {query}. Include title, ingredients, steps, nutrition."}
                ],
                temperature=0.7,
                max_tokens=400
            )
            st.markdown("### 🍴 Recipe Assistant says:")
            st.markdown(resp2.choices[0].message.content)

with tab[2]:
    st.markdown("**Your meal history**")
    meal = st.text_input("🍽️ Log a meal:", placeholder="e.g. grilled paneer with salad")
    if st.button("Log My Meal"):
        if not meal:
            st.error("Enter a meal description.")
        else:
            entry = {"meal": meal, "time": datetime.now().isoformat()}
            meal_log.append(entry)
            with open(LOG_FILE, "w") as f:
                json.dump(meal_log, f)
            st.success("Meal logged!")
    if meal_log:
        st.write(meal_log)

