import streamlit as st
import requests

st.title("LLM Agent Orchestrator")
query = st.text_input("Enter your query (e.g., 'Calculate 3*2' or 'What is Python?')")
if st.button("Run"):
    try:
        response = requests.post(
            "http://localhost:8000/orchestrate",
            #params={"query": query}
            json={"query": query},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        result = response.json()
        st.write(f"**Query**: {result['query']}")
        st.write(f"**Result**: {result['result']}")
    except requests.RequestException as e:
        st.error(f"Error: {str(e)}")
