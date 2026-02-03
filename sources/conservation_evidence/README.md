
# Conservation Evidence Taxonomy

This directory handles the scraping and transformation of the **Conservation Evidence** database (University of Cambridge) into a machine-readable SKOS taxonomy.

## 1. Source Data
*   **Source Authority:** [Conservation Evidence](https://www.conservationevidence.com/)
*   **Contents:** Synopses and associated conservation actions.
*   **Method:** Web Scraping (via `scrape_ce_taxonomy.py`).

## 2. Ingestion Workflow
### Setup
Ensure you have the project dependencies installed via `uv`:
```bash
uv sync
```

### Execution
Run from the root of the repository:
```bash
make ce-actions
# Or directly:
uv run python sources/conservation_evidence/scrape_ce_taxonomy.py
```

## 3. Structure
- **Base URI:** `https://www.conservationevidence.com/actions/`
- **Logic:** Each "Synopsis" is treated as a `skos:Collection` or broad concept, with individual "Actions" as `skos:Concept` items nested within them.

## 4.0 Output `ce-taxonomy.ttl`
Based on the script logic provided, here is the **Output** description for the **Conservation Evidence (CE) Taxonomy** README. 

Note that I have framed this to match your new repository structure (`sources/conservation_evidence/`) and have assumed the addition of the `owl:Ontology` header (which we previously established is necessary for TopBraid EDG to manage the file effectively).

***

## 4. Output: `ce_taxonomy.ttl`

The resulting file is a **SKOS Concept Scheme** that represents the evidence-based conservation actions curated by the University of Cambridge. Unlike the CMP taxonomies, this file uses a mix of internal URI minting for categories and canonical external URIs for specific actions.

- **Prefixes:** 
  - `ces`: `https://www.conservationevidence.com/synopsis/` (Categories)
  - `skos`: `http://www.w3.org/2004/02/skos/core#`
- **Primary Class:** `skos:Concept`
- **Interoperability:** This file is designed to be imported (via `owl:imports`) by the **Results Chain Ontology**. Individual actions can be mapped to `rc:Strategy` instances to link evidence-based interventions to the results chain logic.

### Structural Features
1.  **Ontology Header:** (To be added) Contains metadata identifying the file as a managed asset collection within TopBraid EDG.
2.  **Canonical URIs:** Individual actions use their **live website URLs** as their RDF URIs (e.g., `<https://www.conservationevidence.com/actions/4061>`). This ensures that the Knowledge Graph remains directly linked to the source evidence and full synopses online.
3.  **Two-Level Hierarchy:**
    - **Synopses (Level 0):** High-level categories (e.g., *Bird Conservation*, *Bat Conservation*) are minted as URI-safe strings and mapped as `skos:topConceptOf` the scheme.
    - **Actions (Level 1):** Specific interventions are mapped as `skos:broader` than their respective Synopses.
4.  **Web-Scraped Provenance:** Because the data is scraped directly from the live database, the taxonomy captures the most recent set of evidence available at the time of execution.

### Example Triple
```turtle
# The Synopsis (Category)
ces:BirdConservation a skos:Concept ;
    skos:prefLabel "Bird Conservation"@en ;
    skos:topConceptOf <https://www.conservationevidence.com/actions/Scheme> .

# The specific Action
<https://www.conservationevidence.com/actions/4061> a skos:Concept ;
    skos:prefLabel "Provide nesting boxes for birds"@en ;
    skos:broader ces:BirdConservation .
```

## 5. Provenance Note
This RDF implementation is a technical translation of the Conservation Evidence framework and is not formally maintained by Conservation Evidence.

---
*Date of last ingestion: 2026-01-29*  
*Maintainer: Erik Anderson*