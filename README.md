# Conservation Results Chain Ontology

This directory contains the formal RDF/OWL implementation of the **Results Chain** framework used to model causal logic in global conservation.

Read the [documentation](https://eriktuck.github.io/results-chain-ontology/) or find the WebVOWL [here](https://eriktuck.github.io/results-chain-ontology/webvowl/index.html).

## Theoretical Foundation

This ontology is a technical translation of the conceptual framework established by **Margoluis et al. (2013)**. It provides a machine-readable structure to map how specific strategies lead to threat reduction and, ultimately, biodiversity impact.

### Reference
> **Margoluis, R., Stem, C., Salafsky, N., & Brown, M. (2013).** *Using Results Chains to Improve Strategy Design and Monitoring of Conservation Projects.* Conservation Biology, 27(1), 5-18. [doi:10.1111/j.1523-1739.2012.01940.x](https://doi.org/10.1111/j.1523-1739.2012.01940.x)

---

## Core Schema

The ontology defines the following classes and properties to represent the "Theory of Change" for conservation interventions.

### Classes
| Class | Label | Purpose |
| :--- | :--- | :--- |
| `rc:Strategy` | Strategy | Interventions implemented by a project. |
| `rc:Result` | Result | Desired future states of a factor (includes intermediate outcomes). |
| `rc:ThreatReductionResult` | Threat Reduction | A specific result where a direct threat is diminished. |
| `rc:Impact` | Impact | The desired state of a conservation target (e.g., species or habitat). |
| `rc:Context` | Context | The external environment (geographic locations, institutional entities). |
| `rc:Indicator` | Indicator | Specific variables used to measure progress. |

### Object Properties
| Property | Label | Logic | Domain $\rightarrow$ Range |
| :--- | :--- | :--- | :--- |
| `rc:leadsTo` | leads to | **Transitive.** Causal link between strategies and results. | (Strategy/Result) $\rightarrow$ (Result/Impact) |
| `rc:addresses` | addresses | Direct link between a strategy and a threat. | Strategy $\rightarrow$ ThreatReductionResult |
| `rc:occursIn` | occurs in | Spatial or institutional anchoring. | (Strategy/Result/Impact) $\rightarrow$ Context |
| `rc:hasIndicator` | has indicator | Linking measurement to logic. | (Result/Impact) $\rightarrow$ Indicator |

---

## External Interoperability

A core feature of this ontology is its alignment with global standards found in the `/sources` and `/mappings` folders.

| Class | External Standard | Mapping Method |
| :--- | :--- | :--- |
| **Strategy** | CMP Action Taxonomy / Conservation Evidence | `skos:exactMatch` |
| **ThreatReductionResult** | CMP Threat Taxonomy | `skos:related` |
| **Impact** | ENVO (Environment Ontology) | `skos:narrowMatch` |
| **Context** | Wikidata / DBpedia | `owl:sameAs` (via Wikifiers) |
| **Indicator** | UNBIS Thesaurus | `skos:related` |

The ENVO import and UNBIS import is commented out for now to reduce file size and speed up documentation steps.

---

## Technical Metadata
- **Namespace:** `http://example.org/ontology/results-chain#`
- **Prefix:** `rc`
- **Format:** Turtle (`.ttl`)
- **Compatibility:** Optimized for **TopBraid EDG**.

### Usage in the Knowledge Graph
This ontology acts as the "Logic Layer" (TBox). While specific data instances (ABox) are populated via application-specific ingestion scripts, they must conform to these classes and properties to ensure reasoning and cross-project comparability. 

The `rc:leadsTo` property is defined as **Transitive**, allowing for graph queries that can trace an initial `Strategy` all the way to an `Impact` across multiple intermediate `Results`.

---
*Disclaimer: This repository is a technical implementation and is not formally affiliated with the Conservation Measures Partnership (CMP), though it strives for full compatibility with their Open Standards for the Practice of Conservation.*

## Acknowledgments
ROBOT
R.C. Jackson, J.P. Balhoff, E. Douglass, N.L. Harris, C.J. Mungall, and J.A. Overton. ROBOT: A tool for automating ontology workflows. BMC Bioinformatics, vol. 20, July 2019.

Widoco
@inproceedings{garijo2017widoco,
  title={WIDOCO: a wizard for documenting ontologies},
  author={Garijo, Daniel},
  booktitle={International Semantic Web Conference},
  pages={94--102},
  year={2017},
  organization={Springer, Cham},
  doi = {10.1007/978-3-319-68204-4_9},
  funding = {USNSF ICER-1541029, NIH 1R01GM117097-01},
  url={http://dgarijo.com/papers/widoco-iswc2017.pdf}
}