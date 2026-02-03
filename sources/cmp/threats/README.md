# CMP Threats Taxonomy (Version 4.0)

This directory manages the ingestion and transformation of the **IUCN - Conservation Measures Partnership (CMP) Direct Threats Classification (v4.0)** into a machine-readable SKOS taxonomy.

## 1. Source Data
*   **Source Authority:** IUCN - Conservation Measures Partnership (CMP)
*   **Version:** 4.0 (Released June 2016)
*   **Source Format:** Google Sheet (exported as CSV)
*   **Accessible at:** [CMP Threats Classification v4.0](https://docs.google.com/spreadsheets/d/1yfm7ua9hQJpjycx6FYQJ6Jy5LA4bP0XP61EW3-sX8ZY/edit?gid=179026760#gid=179026760)

## 2. Ingestion Workflow
To ensure reproducibility, this taxonomy is generated programmatically from the raw spreadsheet. This allows the taxonomy to be updated easily if the CMP releases a patch or if further metadata is added to the source.

### Setup
Ensure you have the project dependencies installed via `uv`:
```bash
uv sync
```

### Execution
Run the ingestion script from the root of the repository:
```bash
make cmp-threats
# Or directly:
uv run python sources/cmp/threats/parse_cmp_threats.py
```

## 3. Transformation Logic (`parse_cmp_threats.py`)
The script performs the following steps:
1.  **Extraction:** Reads the "IUCN-CMP Threats v 4.0" sheet from the source CSV.
2.  **Hierarchy Mapping:** Maps the three-level hierarchy (e.g., `1. Residential & Commercial Development` -> `1.1 Housing & Urban Areas`) to `skos:broader` relationships.
3.  **URI Minting:** Generates stable URIs using the pattern: `https://conservationstandards.org/library-item/threats-classification/#`
4.  **Metadata Enrichment:** 
    *   Maps "Threat Category" to `skos:prefLabel`.
    *   Maps "Threat Definition" to `skos:definition`.
    *   Adds a custom `cmp-t:OTHER` category to support crosswalks with unclassified conservation data.
    *   Applies an `owl:Ontology` header to the file for TopBraid EDG compatibility.

## 4. Output: `cmp_threats_4.0.ttl`
The resulting file is a **SKOS Concept Scheme**. 
- **Base URI:** `https://conservationstandards.org/library-item/threats-classification/#`
- **Primary Class:** `skos:Concept`
- **Interoperability:** This file is designed to be imported (via `owl:imports`) by the **Results Chain Ontology** to populate `rc:ThreatReductionResult` nodes.

### Example Triple
```turtle
cmpt:1.1 a skos:Concept ;
    skos:prefLabel "Residential Areas"@en ;
    skos:notation "1.1" ;
    skos:definition "Cities, towns, and settlements including non-housing development typically integrated with housing."@en ;
    skos:broader cmpt:1 ;
    skos:inScheme cmpt:ThreatScheme .
```

## 5. Provenance Note
This RDF implementation is a technical translation of the CMP framework and is not formally maintained by the CMP.

---
*Date of last ingestion: 2026-01-29*  
*Maintainer: Erik Anderson*