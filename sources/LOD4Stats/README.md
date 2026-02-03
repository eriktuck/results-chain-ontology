# LOD4Stats: UN SDG Ontology & Mappings

This directory manages the ingestion of the **LOD4Stats** datasets, an initiative by the **United Nations Statistics Division (UNStats)** to provide Sustainable Development Goals (SDGs) as Linked Open Data.

## 1. Source Data
*   **Source Authority:** [UN Statistics Division (UNStats)](https://unstats.un.org/sdgs/)
*   **Repository:** [UNStats/LOD4Stats](https://github.com/UNStats/LOD4Stats)
*   **Format:** Turtle (`.ttl`)
*   **Description:** This dataset provides the formal OWL ontology for SDGs, the SKOS Knowledge Organization System (KOS) for Goals, Targets, and Indicators, and the subject mappings to other vocabularies like UNBIS.

## 2. Ingestion Workflow
These files are fetched directly from the official UNStats GitHub repository to ensure the latest versions of the SDG structural definitions are used.

### Setup
Ensure you have the project dependencies installed:
```bash
uv sync
```

### Execution
Run the download script from the root of the repository:
```bash
make lod4stats
# Or directly:
uv run python sources/lod4stats/download_lod4stats.py
```

## 3. Script Logic (`download_lod4stats.py`)
The script automates the retrieval of three specific files from the `master/sdg-data/` branch of the LOD4Stats repository:
1.  **`sdgs-ontology.ttl`**: The structural classes and properties for SDGs.
2.  **`sdg-kos-goals-targets-indicators.ttl`**: The actual instances of the 17 Goals, 169 Targets, and 231 Indicators.
3.  **`sdg-kos-subject-mappings.ttl`**: The crosswalks between SDG indicators and external thesauri.

## 4. Output: RDF Files
The script populates this directory with the following files:
- **`sdgs-ontology.ttl`**
- **`sdg-kos-goals-targets-indicators.ttl`**
- **`sdg-kos-subject-mappings.ttl`**

### Interoperability
In the Global Conservation Knowledge Graph, these files serve as the bridge between the **Results Chain** and the **UN 2030 Agenda**:
- **`rc:Indicator`** nodes (mapped to UNBIS) use the **subject-mappings** provided here to demonstrate alignment with specific **SDG Targets**.

## 5. Provenance Note
These files are mirrors of the official UNStats Linked Data. All intellectual property and maintenance of the SDG descriptors belong to the United Nations.

---
*Date of last download: 2026-01-29*  
*Maintainer: Erik Anderson*