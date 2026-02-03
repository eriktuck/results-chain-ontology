import pandas as pd
import re
from pathlib import Path

# URL for the CSV export of the Google Sheet (Threats Sheet)
csv_url = "https://docs.google.com/spreadsheets/d/1yfm7ua9hQJpjycx6FYQJ6Jy5LA4bP0XP61EW3-sX8ZY/export?format=csv&gid=179026760"

def parse_threats():
    # 1. SETUP PATHS
    # Ensures the file is saved in sources/cmp/threats/
    target_dir = Path(__file__).parent 
    target_file = target_dir / "cmp_threats_4.0.ttl"

    # 2. LOAD DATA
    # Real data starts around row 2
    df = pd.read_csv(csv_url, skiprows=2)
    df = df.fillna("") # Clean NaNs

    # Track the current parent for each level
    current_parents = {0: None, 1: None, 2: None}

    # 3. HEADER & PREFIXES
    ttl_output = [
        "@prefix cmpt: <https://conservationstandards.org/library-item/threats-classification#> .",
        "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .",
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
        "@prefix owl: <http://www.w3.org/2002/07/owl#> .",
        "@prefix dcterms: <http://purl.org/dc/terms/> .",
        "",
        "<https://conservationstandards.org/library-item/threats-classification/> a owl:Ontology ;",
        '    rdfs:label "CMP Direct Threats Classification v4.0 (Ontology)"@en ;',
        '    owl:versionInfo "4.0" ;',
        '    dcterms:description "Machine-readable SKOS representation of the CMP Direct Threats Taxonomy."@en .',
        "",
        "cmpt:ThreatScheme a skos:ConceptScheme ;",
        '    rdfs:label "CMP Direct Threats Classification v4.0"@en .',
        "",
        "# Custom addition for crosswalk compatibility",
        "cmpt:OTHER a skos:Concept ;",
        '    skos:prefLabel "UNCLASSIFIED / OTHER"@en ;',
        '    skos:notation "OTHER" ;',
        '    skos:definition "Catch-all category for unclassified threats."@en ;',
        "    skos:topConceptOf cmpt:ThreatScheme .",
        ""
    ]

    for _, row in df.iterrows():
        # Column 0: L1 (Level 0 or Level 1)
        # Column 1: L2 (Level 2)
        # Column 10: Definition (Based on the provided spreadsheet structure)
        col0 = str(row.iloc[0]).strip()
        col1 = str(row.iloc[1]).strip()
        definition = str(row.iloc[10]).strip().replace('"', '\\"')

        label = ""
        code = ""
        level = -1

        # 4. PARSING LOGIC
        # Detect Level 0 (A., B.) or Level 1 (1., 2.)
        if col0 != "":
            if re.match(r'^[A-Z]\.', col0): # Level A.
                level = 0
                parts = col0.split('.', 1)
                code = parts[0].strip()
                label = parts[1].strip() if len(parts) > 1 else ""
            elif re.match(r'^\d+\.', col0): # Level 1.
                level = 1
                parts = col0.split('.', 1)
                code = parts[0].strip()
                label = parts[1].strip() if len(parts) > 1 else ""
        
        # Detect Level 2 (1.1, 1.2)
        elif col1 != "":
            level = 2
            match = re.match(r'^(\d+\.\d+)', col1)
            if match:
                code = match.group(1).strip()
                label = col1.replace(code, "").strip()

        if level != -1:
            code = code.strip()
            label = label.strip()
            
            # Record parents for hierarchy
            current_parents[level] = code
            
            # Build Turtle block
            ttl_output.append(f"cmpt:{code} a skos:Concept ;")
            ttl_output.append(f'    skos:prefLabel "{label}"@en ;')
            ttl_output.append(f'    skos:notation "{code}" ;')
            
            if definition:
                ttl_output.append(f'    skos:definition "{definition}"@en ;')
            
            # Hierarchy Logic
            if level == 0:
                ttl_output.append(f"    skos:topConceptOf cmpt:ThreatScheme .")
            elif level == 1:
                parent = current_parents[0]
                if parent:
                    ttl_output.append(f"    skos:broader cmpt:{parent} ;")
                ttl_output.append(f"    skos:inScheme cmpt:ThreatScheme .")
            elif level == 2:
                parent = current_parents[1]
                if parent:
                    ttl_output.append(f"    skos:broader cmpt:{parent} ;")
                ttl_output.append(f"    skos:inScheme cmpt:ThreatScheme .")
            
            ttl_output.append("")

    # 5. WRITE FILE
    with open(target_file, "w", encoding="utf-8") as f:
        f.write("\n".join(ttl_output))
    
    print(f"Success: {target_file} generated successfully.")

if __name__ == "__main__":
    parse_threats()