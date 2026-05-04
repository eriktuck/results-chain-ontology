import requests
from bs4 import BeautifulSoup
import time
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

user_email = os.getenv("USER_EMAIL", "anonymous@example.com")
headers = {
    "User-Agent": f"CMP-Ontology/1.0 (contact: {user_email})",
    "From": user_email
}

# Base URL for filtering CE by IUCN/CMP v1.1 Action ID
CROSSWALK_URL = "https://www.conservationevidence.com/data/index?pp=4000&terms=&action_type_id%5B%5D={}"

# Bridge Dictionary: CMP v1.1 ID -> CMP v2.0 ID
# Based on the official CMP 1.1 to 2.0 Crosswalk
# https://docs.google.com/spreadsheets/d/1i25GTaEA80HwMvsTiYkdOoXRPWiVPZ5l6KioWx9g2zM/edit?gid=200832250#gid=200832250
V1_TO_V2_BRIDGE = {
    "1.1": "6.1",
    "1.2": "6.2",
    "2.1": "1.1",
    "2.2": "1.1",
    "2.3": "1.2",
    "3.1": "2.1", 
    "3.2": "2.1",
    "3.3": "2.2",
    "3.4": "2.3",
    "4.1": "9.1", 
    "4.2": "9.2",
    "4.3": "3.1", 
    "4.2": "9.2", 
    "4.3": "3.1",
    "5.1": "7.1", 
    "5.2": "7.2",
    "5.3": "7.1", 
    "5.4": "4",
    "6.1": "5.1", 
    "6.2": "5.2", 
    "6.3": "5.3",
    "6.4": "5.4",
    "6.5": "5.5",
    "7.1": "10.2",
    "7.2": "10.3",
    "7.3": "10.4"
}

# Bridge Dictionary: CE URL params -> CMP v2.0 ID
# Note: CE uses only the major action categories (1, 2, 3...)
# so we map directly from those to the CMP v2.0 major categories.
# In CE, 7 is a catchall not "External Capacity Building" as would
# be expected from CMP v1.1.
CE_TO_V2_BRIDGE = {
    "1": "6",
    "2": "1",
    "3": "2",
    "4": "3",
    "5": "7",
    "6": "5",
    "7": "Unclassified"
}

def get_v2_mappings():
    all_mappings = []
    
    for v1_id, v2_id in CE_TO_V2_BRIDGE.items():
        if v2_id == "Unclassified": continue
        
        url = CROSSWALK_URL.format(v1_id)
        print(f"Mapping CE (v1.1: {v1_id}) to CMP (v2.0: {v2_id})...")
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            rows = soup.find_all('tr')
            count = 0
            for row in rows:
                action_cell = row.find('td', {'data-head': 'Actions'})
                if action_cell:
                    link_tag = action_cell.find('a', class_='overlay')
                    if link_tag:
                        # Clean up the URI by removing query params
                        ce_uri = "https://www.conservationevidence.com" + link_tag.get('href').split('?')[0]
                        all_mappings.append((ce_uri, v2_id))
                        count += 1
            print(f"  Linked {count} interventions.")
            time.sleep(1)
            
        except Exception as e:
            print(f"  Error mapping {v1_id}: {e}")
            
    return all_mappings

def generate_bridge_ttl(mappings):
    """
    Generates a formal OWL Ontology file for the crosswalk
    including imports and metadata for TopBraid EDG compatibility.
    """
    ttl = [
        "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .",
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
        "@prefix owl: <http://www.w3.org/2002/07/owl#> .",
        "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .",
        "@prefix dcterms: <http://purl.org/dc/terms/> .",
        "@prefix cmpa: <https://conservationstandards.org/library-item/actions-classification#> .",
        "",
        "<https://eriktuck.github.io/results-chain-ontology/mappings/ce-to-cmp> a owl:Ontology ;",
        "    rdfs:label \"Crosswalk: Conservation Evidence to CMP Actions v2.0\"@en ;",
        "    dcterms:description \"Mappings between Conservation Evidence interventions and the CMP v2.0 Actions Taxonomy.\"@en ;",
        "    owl:versionInfo \"1.0\" ;",
        "",
        "    owl:imports <https://www.conservationevidence.com/actions/Ontology> ;",
        "    owl:imports <https://conservationstandards.org/library-item/actions-classification/> .",
        "",
        "#### CROSSWALK MAPPINGS ####"
    ]
    
    # Track duplicates to keep the file clean
    seen_links = set()

    for ce_uri, v2_id in mappings:
        mapping_triple = f"<{ce_uri}> skos:broadMatch cmpa:{v2_id} ."
        if mapping_triple not in seen_links:
            ttl.append(mapping_triple)
            seen_links.add(mapping_triple)
        
    # Set the path based on your repo structure
    target_dir = Path(__file__).parent 
    target_file = target_dir / "ce_to_cmp2_crosswalk.ttl"
    
    with open(target_file, "w", encoding="utf-8") as f:
        f.write("\n".join(ttl))
    
    print(f"\nSuccess: {len(seen_links)} unique cross-version links saved to {target_file}")

if __name__ == "__main__":
    mappings = get_v2_mappings()
    generate_bridge_ttl(mappings)