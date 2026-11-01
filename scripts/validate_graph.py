"""Validate sample results chains against the SHACL shapes.

Chain A meets every shape. Chain B breaks some: violations fail validation, warnings
(the "should align" shapes) are reported but don't.

Run: make validate
"""

import sys

from pyshacl import validate
from rdflib import Graph

SHAPES = "ontologies/shapes/results_chain_shapes.shacl.ttl"
ONTOLOGY = "ontologies/results_chain/results_chain.ttl"

SAMPLE = """
@prefix rc: <https://eriktuck.github.io/results-chain-ontology#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix cmpa: <https://conservationstandards.org/library-item/actions-classification#> .
@prefix cmpt: <https://conservationstandards.org/library-item/threats-classification#> .
@prefix ex: <http://example.org/data#> .

# ---- Chain A: meets every shape -------------------------------------------

ex:Strategy_A a rc:Strategy ;
    skos:exactMatch cmpa:1.1 ;
    rc:leadsTo ex:Threat_A ;
    rc:occursIn ex:Kafue ;
    rc:basis rc:Stated ;
    rc:supportingQuote "We will train and deploy community rangers." ;
    rc:quotePage 4 ;
    prov:wasDerivedFrom ex:ProjectPlan_A .

ex:Threat_A a rc:ThreatReductionResult ;
    skos:related cmpt:5.1 ;
    rc:hasIndicator ex:Indicator_A1 ;
    rc:leadsTo ex:Impact_A ;
    rc:basis rc:Stated .

ex:Impact_A a rc:Impact ;
    skos:narrowMatch <https://www.gbif.org/species/2435350> ;  # Loxodonta africana
    rc:hasIndicator ex:Indicator_A2 ;
    rc:basis rc:Stated .

# The Strategy -> Threat link was inferred; reify it to say so.
ex:Link_A a rdf:Statement ;
    rdf:subject ex:Strategy_A ;
    rdf:predicate rc:leadsTo ;
    rdf:object ex:Threat_A ;
    rc:basis rc:Inferred .

ex:Indicator_A1 a rc:Indicator ; skos:related <http://metadata.un.org/thesaurus/1007011> .  # WILDLIFE CONSERVATION
ex:Indicator_A2 a rc:Indicator ; skos:related <http://metadata.un.org/thesaurus/1007011> .  # WILDLIFE CONSERVATION
ex:Kafue a rc:Context ; owl:sameAs <http://www.wikidata.org/entity/Q1721097> .  # Kafue National Park

# ---- Chain B: breaks some shapes -------------------------------------------

ex:Strategy_B a rc:Strategy ;
    rc:leadsTo ex:Impact_B ;          # warning: no CMP action
    rc:basis rc:Probably ;            # violation: not Stated or Inferred
    rc:quotePage 2 .                  # violation: a page with no quote

ex:Impact_B a rc:Impact ;             # violation: no indicator
    skos:narrowMatch <http://example.org/my-species> .  # warning: not ENVO or a taxon
"""


def run_validation() -> bool:
    data = Graph().parse(data=SAMPLE, format="turtle")
    conforms, report, text = validate(
        data,
        shacl_graph=Graph().parse(SHAPES, format="turtle"),
        ont_graph=Graph().parse(ONTOLOGY, format="turtle"),
        inference="rdfs",  # so a ThreatReductionResult is also checked as a Result
        abort_on_first=False,
        allow_warnings=True,  # warnings are reported but don't fail validation
    )
    print(text)
    return conforms


if __name__ == "__main__":
    # Chain B is invalid on purpose, so this demo is expected not to conform.
    conforms = run_validation()
    print("Conforms." if conforms else "Does not conform (expected: chain B is invalid on purpose).")
    sys.exit(0)
