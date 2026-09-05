import os
import streamlit as st
from groq import Groq

# Page layout setup
st.set_page_config(page_title="AI Content Assistant", page_icon="📝", layout="centered")

st.title("📝 AI Content Assistant")
st.write("Generate tailored posts, captions, and hashtags instantly powered by Groq.")

# Retrieve API key securely from environment variables / secrets
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    st.warning("⚠️ GROQ_API_KEY environment variable is not set. Please add it to your environment or Streamlit Secrets.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=api_key)

# Input controls
col1, col2 = st.columns(2)

with col1:
    content_type = st.selectbox(
        "Content Type",
        ["Social Media Post", "Blog Summary", "Product Announcement", "Newsletter Snippet", "Educational Post"]
    )
    platform = st.selectbox(
        "Platform",
        ["LinkedIn", "Twitter/X", "Instagram", "Facebook", "Threads"]
    )

with col2:
    tone = st.selectbox(
        "Tone",
        ["Professional", "Casual & Friendly", "Energetic & Hype", "Informative", "Witty & Humorous"]
    )
    target_audience = st.text_input("Target Audience", placeholder="e.g., Software Engineers, Fitness Enthusiasts")

topic = st.text_area("Topic / Core Idea", placeholder="e.g., Launching a new productivity tool for remote teams.")

# Generate Content Button
if st.button("🚀 Generate Post", type="primary"):
    if not topic.strip():
        st.error("Please enter a topic before generating.")
    else:
        with st.spinner("Generating content..."):
            prompt = f"""
            You are an expert social media strategist and content writer.
            Create content based on these inputs:

            - Content Type: {content_type}
            - Platform: {platform}
            - Tone: {tone}
            - Target Audience: {target_audience}
            - Topic: {topic}

            Format your response clearly into three distinct sections:
            1. **Main Content Post** (Formatted appropriately for the chosen platform)
            2. **Short Engaging Caption**
            3. **Relevant Hashtags** (5-10 targeted hashtags)
            """

            try:
                # Call Groq API using llama-3.3-70b-versatile
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                
                output = response.choices[0].message.content
                st.subheader("🎉 Generated Content")
                st.markdown(output)
            except Exception as e:
                st.error(f"Error generating content: {e}")