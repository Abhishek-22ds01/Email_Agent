import random

def generate_draft_reply(subject, body):
    """
    Dummy AI draft reply generator.
    Later you can replace with Grok/OpenAI integration.
    """
    try:
        # Simple keyword-based draft replies
        if "urgent" in body.lower():
            return f"Dear Customer,\n\nWe understand your concern regarding '{subject}'. Our team is addressing this on priority. Please allow us some time.\n\nBest Regards,\nSupport Team"
        elif "error" in body.lower() or "issue" in body.lower():
            return f"Dear Customer,\n\nThank you for reporting the issue regarding '{subject}'. We are looking into it and will get back to you shortly.\n\nBest,\nSupport Team"
        else:
            responses = [
                f"Dear Customer,\n\nThanks for reaching out about '{subject}'. We have received your request and will respond soon.\n\nKind Regards,\nSupport Team",
                f"Hello,\n\nWe’ve noted your email about '{subject}'. Our team is reviewing your request and will update you shortly.\n\nBest,\nSupport Team",
                f"Hi,\n\nYour email regarding '{subject}' has been received. Please allow some time for us to investigate and respond.\n\nRegards,\nSupport Team"
            ]
            return random.choice(responses)
    except Exception as e:
        return f"⚠️ Could not generate reply: {str(e)}"
