import requests
import fetchCID
from dream_analyzer import DreamAnalyzer
import json
from datetime import datetime

class DreamJournalAnalyzer:
    def __init__(self):
        self.analyzer = DreamAnalyzer()

    def fetch_dream_text(self, cid):
        """Fetch dream text from Lighthouse using CID"""
        url = f"https://gateway.lighthouse.storage/ipfs/{cid}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text.strip()  # Extract dream text
            else:
                print(f"Failed to fetch dream text for CID {cid}. Status code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching dream text for CID {cid}: {str(e)}")
            return None

    def analyze_user_dreams(self, user_address):
        """Fetch and analyze all dreams for a given user"""
        # Get dream data from the blockchain
        dreams = fetchCID.get_dream_cids(user_address)
        
        if not dreams:
            return {
                "status": "error",
                "message": "No dreams found or error occurred",
                "data": None
            }

        # Process and analyze each dream
        analyzed_dreams = []
        for dream in dreams:
            dream_text = self.fetch_dream_text(dream['ipfsHash'])
            
            if dream_text:
                analysis = self.analyzer.analyze_dream(dream_text)
                analyzed_dreams.append({
                    "cid": dream['ipfsHash'],
                    "timestamp": dream['timestamp'],
                    "dream_text": dream_text,
                    "analysis": analysis
                })

        # Generate comprehensive analysis report
        report = self.generate_analysis_report(analyzed_dreams)
        
        return {
            "status": "success",
            "message": f"Successfully analyzed {len(analyzed_dreams)} dreams",
            "data": report
        }

    def generate_analysis_report(self, analyzed_dreams):
        """Generate a comprehensive analysis report for all dreams"""
        total_dreams = len(analyzed_dreams)
        if total_dreams == 0:
            return None

        # Initialize counters for aggregate statistics
        category_counts = {}
        emotion_counts = {}
        dream_patterns = {
            "recurring_themes": set(),
            "common_emotions": set()
        }

        # Analyze patterns across all dreams
        for dream in analyzed_dreams:
            analysis = dream["analysis"]
            
            # Aggregate categories
            for category, count in analysis["categories"].items():
                category_counts[category] = category_counts.get(category, 0) + count
                if count > 0:
                    dream_patterns["recurring_themes"].add(category)

            # Aggregate emotions
            for emotion, count in analysis["emotions"].items():
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + count
                if count > 0:
                    dream_patterns["common_emotions"].add(emotion)

        # Calculate percentages and prepare final report
        report = {
            "summary": {
                "total_dreams": total_dreams,
                "date_range": {
                    "start": analyzed_dreams[-1]["timestamp"],
                    "end": analyzed_dreams[0]["timestamp"]
                }
            },
            "dream_patterns": {
                "recurring_themes": list(dream_patterns["recurring_themes"]),
                "common_emotions": list(dream_patterns["common_emotions"])
            },
            "category_distribution": {
                category: {
                    "count": count,
                    "percentage": (count / total_dreams) * 100
                }
                for category, count in category_counts.items()
            },
            "emotion_distribution": {
                emotion: {
                    "count": count,
                    "percentage": (count / total_dreams) * 100
                }
                for emotion, count in emotion_counts.items()
            },
            "detailed_analyses": analyzed_dreams
        }

        return report

def main():
    # Initialize the analyzer
    journal_analyzer = DreamJournalAnalyzer()
    
    # Example user address
    user_address = "0x37dC3933E0f9a1d624136A945905D08550eb9C58"
    
    # Analyze dreams
    result = journal_analyzer.analyze_user_dreams(user_address)
    
    if result["status"] == "success":
        print("\nDream Analysis Report:")
        print(json.dumps(result["data"], indent=2))
        
        # Save the report to a file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"dream_analysis_report_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(result["data"], f, indent=2)
        
        print(f"\nDetailed report saved to {filename}")
    else:
        print(f"\nError: {result['message']}")

if __name__ == "__main__":
    main()