# storyweaver_frontend.py

import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="StoryWeaver", layout="centered")
st.title("📚 StoryWeaver – AI Children's Book Generator")

with st.form("story_form"):
    name = st.text_input("👶 Child's Name", placeholder="e.g. Aria")
    animal = st.text_input("🦄 Favorite Animal", placeholder="e.g. Dragon")
    theme = st.text_input("🌈 Theme", placeholder="e.g. Friendship in the forest")
    submit = st.form_submit_button("✨ Create Story")

if submit:
    with st.spinner("Weaving your magical story... 🧵"):
        response = requests.post(f"{API_URL}/generate-story/", json={
            "child_name": name,
            "favorite_animal": animal,
            "theme": theme
        })
        if response.status_code == 200:
            result = response.json()
            st.success("Story created! 📖")

            st.subheader("📖 Story")
            st.write(result["story"])

            st.subheader("🎨 Illustration")
            st.image(result["image_url"], use_column_width=True)

            st.subheader("📄 Download Your Book")
            pdf_link = f"{API_URL}{result['pdf_url']}"
            st.markdown(f"[📥 Download PDF]({pdf_link})", unsafe_allow_html=True)
        else:
            st.error("Something went wrong. Try again!")
