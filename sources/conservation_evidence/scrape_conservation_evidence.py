import requests
from bs4 import BeautifulSoup
import time
import re
from pathlib import Path
from urllib.parse import urljoin
import os
from dotenv import load_dotenv

load_dotenv()

user_email = os.getenv("USER_EMAIL", "anonymous@example.com")
headers = {
    "User-Agent": f"CMP-Ontology/1.0 (contact: {user_email})",
    "From": user_email
}

# Configuration
BASE_URL = "https://www.conservationevidence.com"
INDEX_URL = f"{BASE_URL}/synopsis/index"
# The pattern for the 'all-on-one-page' view
DATA_TEMPLATE = BASE_URL + "/data/index?pp=1000&synopsis_id%5B%5D={}"

def get_synopses():
    """Scrape the index to find actual Synopses names and IDs."""
    print(f"Accessing {INDEX_URL}...")
    response = requests.get(INDEX_URL, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    synopses = []
    
    # Each synopsis is contained in a div with this class
    blocks = soup.select('div.media.block__wrapper')
    
    for block in blocks:
        # The name is in the <h4> tag inside the content area
        name_tag = block.find('h4')
        # The ID is in the "View online" button link
        link_tag = block.find('a', href=re.compile(r'synopsis_id'))
        
        if name_tag and link_tag:
            name = name_tag.get_text(strip=True)
            href = link_tag.get('href')
            
            # Regex to extract the ID from the URL
            match = re.search(r'synopsis_id(?:%5B%5D|\[\])=(\d+)', href)
            if match:
                s_id = match.group(1)
                # Ensure we don't have duplicate IDs (sometimes previous editions are listed)
                if s_id not in [s['id'] for s in synopses]:
                    synopses.append({'id': s_id, 'name': name})
    
    print(f"Found {len(synopses)} synopses: {[s['name'] for s in synopses]}")
    return synopses

def get_actions(s_id, s_name):
    """Scrape all actions for a specific synopsis."""
    url = DATA_TEMPLATE.format(s_id)
    print(f"  Scraping actions for: {s_name}...")
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        actions = []
        
        # Target the table rows in the results listing
        rows = soup.find_all('tr')
        for row in rows:
            # Look for the action title and link cell
            action_cell = row.find('td', {'data-head': 'Actions'})
            if action_cell:
                title_tag = action_cell.find('p', class_='title')
                link_tag = action_cell.find('a', class_='overlay')
                
                if title_tag and link_tag:
                    label = title_tag.get_text(strip=True)
                    # Get the canonical path (e.g., /actions/4061) and make it absolute
                    path = link_tag.get('href').split('?')[0]
                    canonical_uri = urljoin(BASE_URL, path)
                    
                    actions.append({
                        'label': label,
                        'uri': canonical_uri
                    })
        return actions
    except Exception as e:
        print(f"    Error scraping {s_name}: {e}")
        return []

def generate_ttl(data):
    """Export to Turtle format."""
    ttl = [
        "@prefix ces: <https://www.conservationevidence.com/synopsis/> .",
        "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .",
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
        "@prefix owl: <http://www.w3.org/2002/07/owl#> .",
        "@prefix dcterms: <http://purl.org/dc/terms/> .",
        "",
        "<https://www.conservationevidence.com/actions/Ontology> a owl:Ontology ;",
        '    rdfs:label "Conservation Evidence Actions Taxonomy (Ingested)"@en ;',
        '    dcterms:description "Web-scraped SKOS representation of the Conservation Evidence database."@en .',
        "",
        "<https://www.conservationevidence.com/actions/Scheme> a skos:ConceptScheme ;",
        '    rdfs:label "Conservation Evidence Actions Taxonomy"@en .',
        ""
    ]

    for synopsis in data:
        # Create a URI-safe name for the synopsis
        safe_syn_name = re.sub(r'[^a-zA-Z0-9]', '', synopsis['name'])
        syn_uri = f"ces:{safe_syn_name}"
        
        # Add Synopsis as a top-level concept
        ttl.append(f"{syn_uri} a skos:Concept ;")
        ttl.append(f'    skos:prefLabel "{synopsis["name"]}"@en ;')
        ttl.append(f"    skos:topConceptOf <https://www.conservationevidence.com/actions/Scheme> .\n")

        for action in synopsis['actions']:
            # Add Action with the canonical URL as the URI
            ttl.append(f"<{action['uri']}> a skos:Concept ;")
            # Escape quotes in labels
            clean_label = action['label'].replace('"', '\\"')
            ttl.append(f'    skos:prefLabel "{clean_label}"@en ;')
            ttl.append(f"    skos:broader {syn_uri} .\n")

    target_dir = Path(__file__).parent 
    target_file = target_dir / "ce_taxonomy.ttl"
    
    with open(target_file, "w", encoding="utf-8") as f:
        f.write("\n".join(ttl))

if __name__ == "__main__":
    synopses_list = get_synopses()
    full_data = []

    for synopsis in synopses_list:
        actions = get_actions(synopsis['id'], synopsis['name'])
        synopsis['actions'] = actions
        full_data.append(synopsis)
        time.sleep(1)  # Polite delay

    generate_ttl(full_data)
    print("Done! saved to ce_taxonomy.ttl")