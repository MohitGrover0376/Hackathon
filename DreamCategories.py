import nltk
import CIDtoDreamText
from nltk.tokenize import word_tokenize

nltk.download("punkt")

# Predefined dream categories
dream_categories = {
    "Nightmares": ["fear", "chased", "trapped", "death", "monster", "dark"],
    "Flying Dreams": ["fly", "floating", "hover", "wings", "sky"],
    "Adventure Dreams": ["travel", "explore", "forest", "mountain"],
    "Technology Dreams": ["AI", "robots", "computer", "coding", "future"],
    "Emotional Dreams": ["love", "sad", "happiness", "family", "cry"],
    "Water Dreams": ["ocean", "drowning", "swimming", "lake", "fish"],
    "Work/Study Dreams": ["exam", "job", "office", "deadline", "study"]
}

def categorize_dream(dream_text):
    tokens = word_tokenize(dream_text.lower())  # Tokenize and lowercase

    # Count matching words in each category
    category_scores = {category: sum(1 for word in tokens if word in keywords) 
                       for category, keywords in dream_categories.items()}

    # Get the category with highest match
    best_match = max(category_scores, key=category_scores.get)
    
    return best_match if category_scores[best_match] > 0 else "Uncategorized"

# Categorize fetched dreams
categorized_dreams = {cid: categorize_dream(dream_text) for cid, dream_text in CIDtoDreamText.dreamstext.items()}

print("Categorized Dreams:", categorized_dreams)