import os
import time

import openai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from template import (
    OPENAI_MODEL,
    OPENAI_MINI_MODEL,
    COST_PER_1K_OUTPUT_TOKENS,
    call_openai,
    call_openai_mini,
    compare_models,
    batch_compare,
    format_comparison_table,
)

st.set_page_config(page_title="Day 1 — LLM API Lab", page_icon="🤖", layout="wide")
st.title("🤖 Day 1 — LLM API Foundation")

tab1, tab2, tab3 = st.tabs(["Compare Models", "Streaming Chat", "Batch Compare"])

# Tab 1: Compare GPT-4o vs GPT-4o-mini
with tab1:
    st.header("Compare GPT-4o vs GPT-4o-mini")
    prompt = st.text_area("Prompt", placeholder="Enter your prompt here...", height=100)

    col_temp, col_top_p, col_max = st.columns(3)
    with col_temp:
        temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.05)
    with col_top_p:
        top_p = st.slider("Top-p", 0.0, 1.0, 0.9, 0.05)
    with col_max:
        max_tokens = st.number_input("Max tokens", min_value=64, max_value=2048, value=256, step=64)

    if st.button("Compare", type="primary", disabled=not prompt.strip()):
        with st.spinner("Calling both models..."):
            try:
                gpt4o_response, gpt4o_latency = call_openai(prompt, temperature=temperature, top_p=top_p, max_tokens=max_tokens)
                mini_response, mini_latency = call_openai_mini(prompt, temperature=temperature, top_p=top_p, max_tokens=max_tokens)
            except Exception as e:
                st.error(f"API error: {e}")
                st.stop()

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("GPT-4o")
            st.write(gpt4o_response)
            st.caption(f"Latency: {gpt4o_latency:.2f}s | Est. cost: ${(len(gpt4o_response.split())/0.75)/1000*COST_PER_1K_OUTPUT_TOKENS['gpt-4o']:.5f}")
        with col2:
            st.subheader("GPT-4o-mini")
            st.write(mini_response)
            st.caption(f"Latency: {mini_latency:.2f}s | Est. cost: ${(len(mini_response.split())/0.75)/1000*COST_PER_1K_OUTPUT_TOKENS['gpt-4o-mini']:.5f}")

# Tab 2: Streaming Chat
with tab2:
    st.header("Streaming Chatbot (GPT-4o)")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if user_input := st.chat_input("Type your message..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Keep only last 6 messages (3 turns)
        history = st.session_state.messages[-6:]

        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            try:
                stream = client.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=history,
                    stream=True,
                )
                for chunk in stream:
                    delta = chunk.choices[0].delta.content or ""
                    full_response += delta
                    response_placeholder.write(full_response + "▌")
                response_placeholder.write(full_response)
            except Exception as e:
                st.error(f"API error: {e}")
                st.stop()

        st.session_state.messages.append({"role": "assistant", "content": full_response})

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

# Tab 3: Batch Compare
with tab3:
    st.header("Batch Compare")
    st.caption("Enter one prompt per line.")
    batch_input = st.text_area("Prompts (one per line)", height=150,
                               placeholder="What is AI?\nExplain transformers in one sentence.\nWhat is RAG?")

    if st.button("Run Batch", type="primary", disabled=not batch_input.strip()):
        prompts = [p.strip() for p in batch_input.strip().splitlines() if p.strip()]
        with st.spinner(f"Running {len(prompts)} comparisons..."):
            try:
                results = batch_compare(prompts)
            except Exception as e:
                st.error(f"API error: {e}")
                st.stop()

        st.code(format_comparison_table(results), language=None)

        for i, r in enumerate(results, 1):
            with st.expander(f"#{i} — {r['prompt'][:60]}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("GPT-4o")
                    st.write(r["gpt4o_response"])
                    st.caption(f"Latency: {r['gpt4o_latency']:.2f}s")
                with col2:
                    st.subheader("GPT-4o-mini")
                    st.write(r["mini_response"])
                    st.caption(f"Latency: {r['mini_latency']:.2f}s")
