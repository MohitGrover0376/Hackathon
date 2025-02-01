import nltk
import fetchCID
import CIDtoDreamText
from nltk.tokenize import word_tokenize
from collections import defaultdict

# Download required NLTK data
nltk.download("punkt")

class DreamCategorizer:
    def __init__(self):
        # Predefined dream categories
        self.dream_categories = {
            "Nightmares": ["fear", "chased", "trapped", "death", "monster", "dark"],
            "Flying Dreams": ["fly", "floating", "hover", "wings", "sky"],
            "Adventure Dreams": ["travel", "explore", "forest", "mountain"],
            "Technology Dreams": ["AI", "robots", "computer", "coding", "future"],
            "Emotional Dreams": ["love", "sad", "happiness", "family", "cry"],
            "Water Dreams": ["ocean", "drowning", "swimming", "lake", "fish"],
            "Work/Study Dreams": ["exam", "job", "office", "deadline", "study"]
        }

    def categorize_dream(self, dream_text):
        """Categorize a single dream text"""
        if not dream_text:
            return "Invalid Dream Text"
            
        tokens = word_tokenize(dream_text.lower())  # Tokenize and lowercase

        # Count matching words in each category
        category_scores = {
            category: sum(1 for word in tokens if word in keywords) 
            for category, keywords in self.dream_categories.items()
        }

        # Get the category with highest match
        best_match = max(category_scores.items(), key=lambda x: x[1])
        
        return best_match[0] if best_match[1] > 0 else "Uncategorized"

    def process_user_dreams(self, user_address):
        """Fetch and categorize all dreams for a user"""
        # Get dream data from the blockchain
        dreams = fetchCID.get_dream_cids(user_address)
        
        if not dreams:
            print("No dreams found for this user")
            return None

        # Initialize results dictionary
        categorized_dreams = {}
        category_stats = defaultdict(int)

        # Process each dream
        for dream in dreams:
            cid = dream['ipfsHash']
            # Fetch dream text using CIDtoDreamText
            dream_text = CIDtoDreamText.fetch_dream_text(cid)
            
            if dream_text:
                # Categorize the dream
                category = self.categorize_dream(dream_text)
                categorized_dreams[cid] = {
                    'category': category,
                    'text': dream_text,
                    'timestamp': dream['timestamp']
                }
                category_stats[category] += 1
            else:
                print(f"Failed to fetch dream text for CID: {cid}")

        return {
            'categorized_dreams': categorized_dreams,
            'category_stats': dict(category_stats)
        }

def main():
    # Initialize the categorizer
    categorizer = DreamCategorizer()
    
    # Example user address
    user_address = "0x37dC3933E0f9a1d624136A945905D08550eb9C58"
    
    # Process and categorize dreams
    results = categorizer.process_user_dreams(user_address)
    
    if results:
        print("\nDream Categories Summary:")
        for category, count in results['category_stats'].items():
            print(f"{category}: {count} dreams")
        
        print("\nDetailed Dream Analysis:")
        for cid, dream_info in results['categorized_dreams'].items():
            print(f"\nCID: {cid}")
            print(f"Category: {dream_info['category']}")
            print(f"Timestamp: {dream_info['timestamp']}")
            print(f"Dream Text: {dream_info['text'][:100]}...")  # Show first 100 characters
    else:
        print("No dreams found or error occurred")

if __name__ == "__main__":
    main()
