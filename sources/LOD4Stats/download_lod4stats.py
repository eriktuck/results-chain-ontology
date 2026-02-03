import requests
from pathlib import Path

HEADER_INJECTIONS = {
    "sdg-kos-goals-targets-indicators.ttl": """@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<http://metadata.un.org/sdg/> a owl:Ontology ;
    rdfs:label "SDG Goals, Targets, and Indicators Taxonomy (UN Stats Mirror)"@en ;
    owl:imports <http://metadata.un.org/sdg/ontology> .

""",
    "sdg-kos-subject-mappings.ttl": """@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<http://metadata.un.org/mappings/sdg-subjects> a owl:Ontology ;
    rdfs:label "SDG Subject Mappings (UN Stats Mirror)"@en ;
    owl:imports <http://metadata.un.org/sdg/> .

"""
}

def download_and_patch_sdg_files():
    base_raw_url = "https://raw.githubusercontent.com/UNStats/LOD4Stats/master/sdg-data/"
    
    files_to_download = [
        "sdgs-ontology.ttl",
        "sdg-kos-goals-targets-indicators.ttl",
        "sdg-kos-subject-mappings.ttl"
    ]

    target_dir = Path(__file__).parent

    for file_name in files_to_download:
        file_url = f"{base_raw_url}{file_name}"
        save_path = target_dir / file_name
        
        print(f"Downloading {file_name}...")
        
        try:
            response = requests.get(file_url)
            response.raise_for_status()
            
            content = response.text

            # Check if this file needs a header injection
            if file_name in HEADER_INJECTIONS:
                print(f"  -> Injecting Ontology Header into {file_name}")
                content = HEADER_INJECTIONS[file_name] + content
            
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Successfully saved and patched: {save_path}")
            
        except requests.exceptions.HTTPError as e:
            print(f"Failed to download {file_name}: {e}")
        except Exception as e:
            print(f"An error occurred with {file_name}: {e}")

if __name__ == "__main__":
    download_and_patch_sdg_files()
