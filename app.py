import streamlit as st
import pandas as pd
from textblob import TextBlob  # 📌 For sentiment analysis
from reply import generate_draft_reply
 # Load filtered emails from Excel
df = pd.read_excel("filtered_emails.xlsx")

st.title("📧 Smart Email Support Assistant")
st.write("View, search, and filter your emails in one place")

# PRIROTY SET 

urgent_keywords = ["urgent", "immediate", "asap", "critical", "cannot access", "important"]

def detect_priority(text):
    if any(word in str(text).lower() for word in urgent_keywords):
        return "High"
    return "Normal"

df["priority"] = df.apply(
    lambda row: "High" if detect_priority(row["subject"]) == "High" or detect_priority(row["body"]) == "High" else "Normal",
    axis=1
)

# SENTIMENT ANALYSIS

def get_sentiment(text):
    analysis = TextBlob(str(text))
    if analysis.sentiment.polarity > 0.1:
        return "Positive"
    elif analysis.sentiment.polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

df["sentiment"] = df["body"].apply(get_sentiment)

# Show total emails
st.metric("Total Emails", len(df))
st.metric("Support Emails", df['is_support'].sum())
st.metric("Urgent Emails", (df["priority"] == "High").sum())
st.metric("Positive Emails", (df["sentiment"] == "Positive").sum())

# Search box
search = st.text_input("🔍 Search emails by keyword")

if search:
    results = df[df['subject'].str.contains(search, case=False, na=False) | 
                 df['body'].str.contains(search, case=False, na=False)]
else:
    results = df

st.subheader("📩 Email List")

# Iterate over results and add Draft Reply button
for _, row in results.iterrows():
    st.write(f"**From:** {row['from']}")
    st.write(f"**Subject:** {row['subject']}")
    st.write(f"**Priority:** {row['priority']}")
    st.write(f"**Sentiment:** {row['sentiment']}")
    st.write(f"**Support Related:** {row['is_support']}")
    
    # Draft reply button
    if st.button(f"Generate Draft Reply", key=row.name):
        try:
            draft_reply = generate_draft_reply(row['subject'], row['body'])
        except Exception as e:
            draft_reply = f"Could not generate reply: {str(e)}"
        st.text_area("📄 Draft Reply", value=draft_reply, height=150)
    
    st.markdown("---")

# Show only support emails toggle
if st.checkbox("Show only support emails"):
    support_emails = results[results["is_support"]]
    for _, row in support_emails.iterrows():
        st.write(f"**From:** {row['from']}")
        st.write(f"**Subject:** {row['subject']}")
        st.write(f"**Priority:** {row['priority']}")
        st.write(f"**Sentiment:** {row['sentiment']}")
        # Draft reply button
        if st.button(f"Generate Draft Reply (Support)", key=f"support_{row.name}"):
            try:
                draft_reply = generate_draft_reply(row['subject'], row['body'])
            except Exception as e:
                draft_reply = f"Could not generate reply: {str(e)}"
            st.text_area("📄 Draft Reply", value=draft_reply, height=150)
        st.markdown("---")
