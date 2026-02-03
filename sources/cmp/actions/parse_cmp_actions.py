import pandas as pd
import re
from pathlib import Path

csv_url = "https://docs.google.com/spreadsheets/d/1i25GTaEA80HwMvsTiYkdOoXRPWiVPZ5l6KioWx9g2zM/export?format=csv&gid=1144804238"

def parse_cmp():
    target_dir = Path(__file__).parent 
    target_file = target_dir / "cmp_actions_2.0.ttl"

    df = pd.read_csv(csv_url, skiprows=2)
    df = df.fillna("")

    current_parents = {0: None, 1: None, 2: None}

    ttl_output = [
        "@prefix cmpa: <https://conservationstandards.org/library-item/actions-classification#> .",
        "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .",
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
        "@prefix owl: <http://www.w3.org/2002/07/owl#> .",
        "@prefix dcterms: <http://purl.org/dc/terms/> .",
        "",
        "<https://conservationstandards.org/library-item/actions-classification/> a owl:Ontology ;",
        '    rdfs:label "CMP Actions Classification v2.0 (Ontology)"@en ;',
        '    owl:versionInfo "2.0" ;',
        '    dcterms:description "Machine-readable SKOS representation of the CMP Actions Taxonomy."@en .',
        "",
        "cmpa:ActionScheme a skos:ConceptScheme ;",
        '    rdfs:label "CMP Actions Classification v2.0"@en .',
        "",
        "# Custom addition for crosswalk compatibility",
        "cmpa:OTHER a skos:Concept ;",
        '    skos:prefLabel "UNCLASSIFIED / OTHER"@en ;',
        '    skos:notation "OTHER" ;',
        '    skos:definition "Catch-all category for unclassified actions."@en ;',
        "    skos:topConceptOf cmpa:ActionScheme .",
        ""
    ]

    for _, row in df.iterrows():
        col0 = str(row.iloc[0]).strip()
        col1 = str(row.iloc[1]).strip()
        col2 = str(row.iloc[2]).strip()
        definition = str(row.iloc[4]).strip().replace('"', '\\"')

        label = ""
        code = ""
        level = -1

        if col0 != "":
            if re.match(r'^[A-Z]\.', col0): # Level A.
                level = 0
                parts = col0.split('.', 1)
                code = parts[0]
                label = parts[1] if len(parts) > 1 else ""
            elif re.match(r'^\d+\.', col0): # Level 1.
                level = 1
                parts = col0.split('.', 1)
                code = parts[0]
                label = parts[1] if len(parts) > 1 else ""
        
        elif col1 != "":
            level = 2
            match = re.match(r'^(\d+\.\d+)', col1)
            if match:
                code = match.group(1)
                label = col1.replace(code, "").strip()

        if level != -1:
            code = code.strip()
            label = label.strip()
            current_parents[level] = code
            
            ttl_output.append(f"cmpa:{code} a skos:Concept ;")
            ttl_output.append(f'    skos:prefLabel "{label}"@en ;')
            ttl_output.append(f'    skos:notation "{code}" ;')
            if definition:
                ttl_output.append(f'    skos:definition "{definition}"@en ;')
            
            if level == 0:
                ttl_output.append(f"    skos:topConceptOf cmpa:ActionScheme .")
            elif level == 1:
                parent = current_parents[0]
                if parent: ttl_output.append(f"    skos:broader cmpa:{parent} ;")
                ttl_output.append(f"    skos:inScheme cmpa:ActionScheme .")
            elif level == 2:
                parent = current_parents[1]
                if parent: ttl_output.append(f"    skos:broader cmpa:{parent} ;")
                ttl_output.append(f"    skos:inScheme cmpa:ActionScheme .")
            
            ttl_output.append("")

    with open(target_file, "w", encoding="utf-8") as f:
        f.write("\n".join(ttl_output))
    
    print(f"Success: {target_file} generated.")

if __name__ == "__main__":
    parse_cmp()