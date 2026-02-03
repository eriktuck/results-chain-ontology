# Crosswalk: ENVO to UNBIS

This directory contains the semantic bridge between the **Environment Ontology (ENVO)** and the **UNBIS Thesaurus**. This mapping allows the knowledge graph to connect technical environmental impacts to international policy indicators and Sustainable Development Goals (SDGs).

## 1. Objective
To map environmental entities (habitats, biomes, and processes) defined in ENVO to corresponding thematic subjects and indicators in the UNBIS Thesaurus.

## 2. Methodology
The crosswalk was performed using the **TopBraid EDG Crosswalk Tool**. 

### Curation Process
1.  **Candidate Generation:** Initial mapping suggestions were generated using TopBraid’s internal lexical matching algorithms (comparing `rdfs:label`, `skos:prefLabel`, and `skos:altLabel`).
2.  **Manual Curation:** Every suggested mapping was manually reviewed and either **Approved** or **Rejected**.
3.  **Approval Criteria:** Mappings were approved only if they met the following strict criteria:
    *   **Exact String Matches:** Identical labels.
    *   **Morphological Variations:** Differences in pluralization or minor grammatical shifts that did not alter the core concept (e.g., `ENVO:Forest` to `UNBIS:Forests`).
    *   **Lexical Similarity:** Terms that are synonymous in a conservation context where the scope of the UNBIS term clearly covered the ENVO entity.

### Curation Philosophy
This crosswalk follows a **conservative mapping strategy**:
*   **Precision over Recall:** We prioritize the accuracy of the link over the total number of links. 
*   **Exclusionary Bias:** If a mapping was ambiguous or if the UNBIS term was significantly broader than the ENVO term without a clear thematic fit, it was **Rejected**.
*   **One-to-One Preference:** While some one-to-many mappings exist, the focus was on identifying the single most appropriate indicator for each environmental impact.

## 3. Technical Details
- **Source File:** `sources/envo/envo.owl`
- **Target File:** `sources/unbis/unbis_thesaurus.ttl`
- **Output File:** `envo_to_unbis_crosswalk.ttl`
- **Mapping Property:** Predominantly uses `skos:closeMatch`.

## 4. Maintenance
As this is a manually curated file exported from TopBraid EDG, it should not be overwritten by automated scripts. 

**To Update:** Import the `.ttl` file back into a TopBraid EDG Crosswalk collection to perform the necessary edits. In the Settings tab, manually pick ENVO as "From" and UNBIS as "To." Re-export the **Sorted Turtle** file to this directory.

The ENVO import and UNBIS import is commented out for now to reduce file size and speed up documentation steps.

## 5. Usage in the Knowledge Graph
This mapping is imported by the **Results Chain Ontology**. It enables the following graph traversal:
`[rc:Impact] -> (via ENVO) -> [Mapping] -> (via UNBIS) -> [rc:Indicator] -> (via LOD4Stats) -> [SDG Target]`

---
*Date of Curation: 2026-01-28*  
*Curator: Erik Anderson*
*Tool: Version: 8.5.1*
