# UNBIS Thesaurus (United Nations Bibliographic Information System)

This directory manages the ingestion of the **UNBIS Thesaurus**, a multidisciplinary terminology database maintained by the **Dag Hammarskjöld Library**. It provides the primary controlled vocabulary for indexing indicators and subjects within the Global Conservation Knowledge Graph.

## 1. Source Data
*   **Source Authority:** [United Nations Dag Hammarskjöld Library](https://digitallibrary.un.org/)
*   **Version:** July 2025 Snapshot (Record: 4075456)
*   **Format:** Turtle (`.ttl`)
*   **Official Link:** [UNBIS Thesaurus July 2025](https://digitallibrary.un.org/record/4075456)

## 2. Ingestion Workflow
The UNBIS Thesaurus is published as periodic snapshots. This directory uses a script to pull the specific 2025 Turtle release to ensure consistency across the knowledge graph.

### Setup
Ensure you have the project dependencies installed:
```bash
uv sync
```

### Execution
Run the download script from the root of the repository:
```bash
make unbis
# Or directly:
uv run python sources/unbis/download_unbis.py
```

## 3. Script Logic (`download_unbis.py`)
- **Direct Retrieval:** Fetches the specific Turtle distribution (`unbist-20250708_2.ttl`) from the UN Digital Library.
- **Streaming Transfer:** Uses a streaming download to handle the ~7.5MB file size efficiently.
- **Verification:** Reports the final file size and storage path upon completion.

## 4. Output: `unbis_thesaurus.ttl`
The resulting file is a **SKOS Concept Scheme**.
- **Primary Class:** `skos:Concept`
- **Interoperability:** In this project, UNBIS concepts are mapped to **`rc:Indicator`** nodes. Because **LOD4Stats** provides a crosswalk between UNBIS and SDG targets, these indicators serve as the semantic bridge connecting local conservation actions to the UN 2030 Agenda.

### Example Triple
```turtle
# Example of a UNBIS concept used as an indicator
<http://metadata.un.org/thesaurus/1002047> a skos:Concept ;
    skos:prefLabel "Forest conservation"@en ;
    skos:broader <http://metadata.un.org/thesaurus/1002058> .
```

## 5. Provenance Note
The UNBIS Thesaurus is the intellectual property of the United Nations. This repository maintains a local copy for interoperability purposes under the UN Open Data guidelines.

---
*Date of last download: 2026-01-29*  
*Maintainer: Erik Anderson*