import requests
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

user_email = os.getenv("USER_EMAIL", "anonymous@example.com")
headers = {
    "User-Agent": f"CMP-Ontology/1.0 (contact: {user_email})",
    "From": user_email
}

def download_unbis_ttl():
    # Direct link to the July 2025 Turtle snapshot from record 4075456
    url = "https://digitallibrary.un.org/record/4075456/files/unbist-20250708_2.ttl"
    
    target_dir = Path(__file__).parent
    target_file = target_dir / "unbis_thesaurus.ttl"

    try:
        print(f"Downloading UNBIS Thesaurus (Turtle)...")
        # stream=True is good practice for 7MB+ files
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        
        with open(target_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        print(f"Success! File saved to: {target_file}")
        print(f"File size: {target_file.stat().st_size / 1024 / 1024:.2f} MB")
        
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_unbis_ttl()
