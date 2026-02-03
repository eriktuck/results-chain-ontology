# CMP Actions Taxonomy (Version 2.0)

This directory manages the ingestion and transformation of the **Conservation Measures Partnership (CMP) Conservation Actions Classification (v2.0)** into a machine-readable SKOS taxonomy.

## 1. Source Data
*   **Source Authority:** Conservation Measures Partnership (CMP)
*   **Version:** 2.0 (Released June 2016)
*   **Source Format:** Google Sheet (exported as CSV)
*   **Accessible at:** [CMP Actions Classification v2.0](https://docs.google.com/spreadsheets/d/1i25GTaEA80HwMvsTiYkdOoXRPWiVPZ5l6KioWx9g2zM/export?format=csv&gid=1144804238)

## 2. Ingestion Workflow
To ensure reproducibility, this taxonomy is generated programmatically from the raw spreadsheet. This allows the taxonomy to be updated easily if the CMP releases a patch or if further metadata (like localized labels) is added to the source.

### Setup
Ensure you have the project dependencies installed via `uv`:
```bash
uv sync
```

### Execution
Run the ingestion script from the root of the repository:
```bash
make cmp-actions
# Or directly:
uv run python sources/cmp/actions/parse_cmp_actions.py
```

## 3. Transformation Logic (`parse_cmp_actions.py`)
The script performs the following steps:
1.  **Extraction:** Reads the "Actions v 2.0" sheet.
2.  **Hierarchy Mapping:** Maps the three-level hierarchy (e.g., `1. Land/Water Protection` -> `1.1 Site/Area Protection`) to `skos:narrower` relationships.
3.  **URI Minting:** Generates stable URIs using the pattern: `https://conservationstandards.org/library-item/actions-classification/#`
4.  **Metadata Enrichment:** 
    *   Maps "Action Category" to `skos:prefLabel`.
    *   Maps "Action Definition" to `skos:definition`.
    *   Applies an `owl:Ontology` header to the file for TopBraid EDG compatibility.

## 4. Output: `cmp_actions_2.0.ttl`
The resulting file is a **SKOS Concept Scheme**. 
- **Base URI:** `ttps://conservationstandards.org/library-item/actions-classification/#`
- **Primary Class:** `skos:Concept`
- **Interoperability:** This file is designed to be imported (via `owl:imports`) by the **Results Chain Ontology**. 

### Example Triple
```turtle
cmpa:1.1 a skos:Concept ;
    skos:prefLabel "Site/Area Stewardship"@en ;
    skos:notation "1.1" ;
    skos:definition "Enhancing viability / mitigating stresses for sites and/or ecosystem targets, especially on a smaller scale"@en ;
    skos:broader cmpa:1 ;
    skos:inScheme cmpa:ActionScheme .
```

## 5. Provenance Note
This RDF implementation is a technical translation of the CMP framework and is not formally maintained by the CMP.

---
*Date of last ingestion: 2026-01-29*  
*Maintainer: Erik Anderson*