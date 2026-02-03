# ENVO Ontology (Environment Ontology)

This directory manages the local cache of the **Environment Ontology (ENVO)**, a community-driven ontology for the representation of entities relevant to environmental science, habitats, and ecosystems.

## 1. Source Data
*   **Source Authority:** [ENVO / OBO Foundry](http://www.obofoundry.org/ontology/envo.html)
*   **Format:** OWL (Web Ontology Language)
*   **Persistent URL (PURL):** `http://purl.obolibrary.org/obo/envo.owl`
*   **Description:** ENVO provides a standardized vocabulary for habitats, biomes, and environmental processes.

## 2. Ingestion Workflow
Because the ENVO file is large (~50MB+) and frequently updated by the OBO community, this directory uses a download script to fetch the latest stable release.

### Setup
Ensure you have the project dependencies installed:
```bash
uv sync
```

### Execution
Run the download script from the root of the repository:
```bash
make envo
# Or directly:
uv run python sources/envo/download_envo.py
```

## 3. Script Logic (`download_envo.py`)
- **Streaming Download:** To minimize memory usage, the script streams the `.owl` file in 8KB chunks.
- **Stable Redirects:** The script targets the OBO PURL, which automatically redirects to the most recent stable version on the ENVO GitHub repository.

## 4. Output: `envo.owl`
The resulting file is the full ENVO ontology in OWL/XML or Turtle format.
- **Interoperability:** This file is imported into the **Results Chain Ontology** to provide standardized targets for `rc:Impact` individuals using `skos:narrowMatch` or `skos:exactMatch`.

## 5. Provenance Note
This directory contains a local mirror of the ENVO ontology. All intellectual property remains with the ENVO consortium and the OBO Foundry.

---
*Date of last download: 2026-01-28*  
*Maintainer: Erik Anderson*
