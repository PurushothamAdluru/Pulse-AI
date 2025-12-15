import streamlit as st
import json
import pandas as pd
import plotly.express as px

# Load data
def load_data():
    with open("data.json", "r") as f:
        return json.load(f)

data = load_data()
df = pd.DataFrame(data)

st.set_page_config(page_title="AI Marketing Dashboard", layout="wide")
st.title("📊 AI Customer Intent & Marketing Dashboard")

# --- METRICS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Conversations", len(df))
col2.metric("Unique Intents", df['intent'].nunique())
col3.metric("Average Lead Score", round(df['lead_score'].mean(), 2))
col4.metric("Positive Sentiments", sum(df['sentiment'] == "positive"))

st.markdown("---")

# --- FILTERS ---
st.sidebar.header("Filters")
intent_filter = st.sidebar.multiselect("Filter by Intent", df['intent'].unique())
sentiment_filter = st.sidebar.multiselect("Filter by Sentiment", df['sentiment'].unique())

filtered_df = df.copy()
if intent_filter:
    filtered_df = filtered_df[filtered_df['intent'].isin(intent_filter)]
if sentiment_filter:
    filtered_df = filtered_df[filtered_df['sentiment'].isin(sentiment_filter)]

# --- CHARTS ---
colA, colB = st.columns(2)

with colA:
    fig_intent = px.bar(filtered_df['intent'].value_counts(), 
                        title="Intent Distribution", 
                        labels={'value': 'Count', 'index': 'Intent'})
    st.plotly_chart(fig_intent, use_container_width=True)

with colB:
    fig_sentiment = px.pie(filtered_df, 
                           names='sentiment', 
                           title="Sentiment Breakdown")
    st.plotly_chart(fig_sentiment, use_container_width=True)

st.markdown("---")

# Lead score histogram
fig_score = px.histogram(filtered_df, 
                         x='lead_score', 
                         nbins=10, 
                         title="Lead Score Distribution")
st.plotly_chart(fig_score, use_container_width=True)

st.markdown("---")

# --- RAW TABLE ---
st.subheader("Conversation Log")
st.dataframe(filtered_df)
