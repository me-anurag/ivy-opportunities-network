import random

def classify_opportunity(text):

    text = text.lower()

    if any(word in text for word in [
        "ai", "machine learning", "deep learning",
        "neural", "data science", "computer vision", "nlp"
    ]):
        return "AI"

    elif any(word in text for word in [
        "engineering", "robotics", "electronics",
        "mechanical", "electrical", "hardware"
    ]):
        return "Engineering"

    elif any(word in text for word in [
        "law", "legal", "policy", "constitution"
    ]):
        return "Law"

    elif any(word in text for word in [
        "biology", "medical", "medicine", "clinical",
        "biomedical", "health"
    ]):
        return "Biomedical"

    # Balanced fallback distribution
    else:
        return random.choice([
            "Engineering",
            "Law",
            "Biomedical",
            "AI"
        ])