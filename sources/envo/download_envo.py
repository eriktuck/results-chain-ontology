import os
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


def download_envo():
    # 1. Configuration
    # This PURL always redirects to the latest stable envo.owl
    url = "http://purl.obolibrary.org/obo/envo.owl"
    
    # Define the local path
    target_dir = Path(__file__).parent
    target_file = target_dir / "envo.owl"

    print(f"Starting download of ENVO.owl...")
    print(f"Destination: {target_file.absolute()}")

    try:
        # 3. Stream the download
        # ENVO is large (~50MB+), so we download in chunks to save memory
        with requests.get(url, headers=headers, stream=True) as response:
            # Check if the download link is valid
            response.raise_for_status()
            
            with open(target_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                        
        print("Download complete!")
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")

if __name__ == "__main__":
    download_envo()
