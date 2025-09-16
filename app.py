import streamlit as st
import pandas as pd
from textblob import TextBlob
from reply import generate_draft_reply

# Load filtered emails
df = pd.read_excel("filtered_emails.xlsx")

st.set_page_config(page_title="Smart Email Support Assistant", layout="wide")

# Sidebar for search and filters
st.sidebar.title("Filters")
search = st.sidebar.text_input("🔍 Search emails by keyword")
show_support_only = st.sidebar.checkbox("Show only support emails")

# PRIORITY & SENTIMENT
urgent_keywords = ["urgent", "immediate", "asap", "critical", "cannot access", "important"]

def detect_priority(text):
    return "High" if any(word in str(text).lower() for word in urgent_keywords) else "Normal"

df["priority"] = df.apply(
    lambda row: "High" if detect_priority(row["subject"]) == "High" or detect_priority(row["body"]) == "High" else "Normal",
    axis=1
)

def get_sentiment(text):
    analysis = TextBlob(str(text))
    if analysis.sentiment.polarity > 0.1:
        return "Positive"
    elif analysis.sentiment.polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

df["sentiment"] = df["body"].apply(get_sentiment)

# Apply filters
results = df.copy()
if search:
    results = results[results['subject'].str.contains(search, case=False, na=False) | 
                      results['body'].str.contains(search, case=False, na=False)]
if show_support_only:
    results = results[results["is_support"]]

# Dashboard Metrics
st.title("📧 Smart Email Support Assistant")
st.markdown("#### Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Emails", len(df))
col2.metric("Support Emails", df['is_support'].sum())
col3.metric("Urgent Emails", (df["priority"] == "High").sum())
col4.metric("Positive Emails", (df["sentiment"] == "Positive").sum())

st.markdown("### 📩 Email List")

# Display emails in card-like style
for _, row in results.iterrows():
    with st.container():
        cols = st.columns([3,1,1,1,2])  # Subject/From | Priority | Sentiment | Support | Draft
        cols[0].markdown(f"**From:** {row['from']}  \n**Subject:** {row['subject']}")
        # Priority badge
        if row["priority"] == "High":
            cols[1].markdown(f"<span style='color:red'>**{row['priority']}**</span>", unsafe_allow_html=True)
        else:
            cols[1].markdown(f"<span style='color:green'>**{row['priority']}**</span>", unsafe_allow_html=True)
        # Sentiment badge
        if row["sentiment"] == "Positive":
            cols[2].markdown(f"<span style='color:green'>**{row['sentiment']}**</span>", unsafe_allow_html=True)
        elif row["sentiment"] == "Negative":
            cols[2].markdown(f"<span style='color:red'>**{row['sentiment']}**</span>", unsafe_allow_html=True)
        else:
            cols[2].markdown(f"<span style='color:gray'>**{row['sentiment']}**</span>", unsafe_allow_html=True)
        # Support
        cols[3].markdown(f"{row['is_support']}")
        
        # Draft Reply button
        if cols[4].button("Generate Draft Reply", key=row.name):
            try:
                draft_reply = generate_draft_reply(row['subject'], row['body'])
            except Exception as e:
                draft_reply = f"Could not generate reply: {str(e)}"
            st.text_area("📄 Draft Reply", value=draft_reply, height=150)
        
        st.markdown("---")
