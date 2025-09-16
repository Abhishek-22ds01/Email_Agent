# FETCH EMAIL IDS THROUGH IMAP LIBRARY
import imaplib
import email
from email.header import decode_header

EMAIL = "Abhishek98739999@gmail.com"
PASSWORD = "vqxy shoq pzir gegb"

imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(EMAIL, PASSWORD)
imap.select("inbox")

status, messages = imap.search(None, "ALL")
email_ids = messages[0].split()

emails = []  # 📌 Real emails will be stored here

# Fetch latest 10 emails (you can change the number)
for eid in email_ids[-10:]:
    status, msg_data = imap.fetch(eid, "(RFC822)")
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            
            # Decode subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")
            
            from_ = msg.get("From")
            
            # Extract email body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")
            
            # Store email in list
            emails.append({
                "from": from_,
                "subject": subject,
                "body": body
            })
# print("="*50)
# print("From:", from_)
# print("Subject:", subject)
# print("Body:", body[:200], "...") 

imap.close()
imap.logout()



import pandas as pd

df= pd.DataFrame(emails)  # Convert your real emails into DataFrame
df.head()          # Check first few rows




def filter_emails(emails):

    keywords = ["support", "help", "request", "query"]

    def is_support(text):
        text = text.lower()
        return any(word in text for word in keywords)

    df["is_support"] = df["subject"].apply(is_support) | df["body"].apply(is_support)
    return df

if __name__ == "__main__":
    print("📥 Fetching emails...")
    print(f"✅ Retrieved {len(emails)} emails")

    df = filter_emails(emails)

    print("\n📌 Filtered Emails:")
    print(df[["from", "subject", "is_support"]])
     
    # SAVE FILTER EMAIL INTO EXCEL
    df.to_excel("filtered_emails.xlsx", index=False)
