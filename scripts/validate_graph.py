"""Validate sample results chains against the SHACL shapes.

Chain A meets every shape. Chain B breaks some on purpose: violations make a graph
non-conforming, warnings (the "should align" shapes) are reported but don't.

The script exits non-zero if chain A doesn't conform, or if chain B's violations and
warnings differ from the ones it is built to produce, so a broken shape or ontology
fails `make validate`.

Run: make validate
"""

import sys

from pyshacl import validate
from rdflib import Graph, Namespace
from rdflib.namespace import SH, SKOS

SHAPES = "ontologies/shapes/results_chain_shapes.shacl.ttl"
ONTOLOGY = "ontologies/results_chain/results_chain.ttl"

PREFIXES = """
@prefix rc: <https://eriktuck.github.io/results-chain-ontology#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix cmpa: <https://conservationstandards.org/library-item/actions-classification#> .
@prefix cmpt: <https://conservationstandards.org/library-item/threats-classification#> .
@prefix ex: <http://example.org/data#> .
"""

CHAIN_A = PREFIXES + """
# ---- Chain A: meets every shape -------------------------------------------

ex:Strategy_A a rc:Strategy ;
    skos:exactMatch cmpa:1.1 ;
    rc:leadsTo ex:Threat_A ;
    rc:occursIn ex:Kafue ;
    rc:basis rc:Stated ;
    rc:supportingQuote "We will train and deploy community rangers."@en ;
    rc:quotePage 4 ;
    prov:wasDerivedFrom ex:ProjectPlan_A .

ex:Threat_A a rc:ThreatReductionResult ;
    skos:related cmpt:5.1 ;
    rc:hasIndicator ex:Indicator_A1 ;
    rc:leadsTo ex:Impact_A ;
    rc:basis rc:Stated .

ex:Impact_A a rc:Impact ;
    rc:hasTarget <https://www.gbif.org/species/2435350> ;  # Loxodonta africana
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

"""

CHAIN_B = PREFIXES + """
# ---- Chain B: breaks some shapes -------------------------------------------

ex:Strategy_B a rc:Strategy ;
    rc:leadsTo ex:Impact_B ;          # warning: no CMP action
    rc:basis rc:Probably ;            # violation: not Stated or Inferred
    rc:quotePage 0 .                  # violations: a page with no quote, and pages start at 1

ex:Impact_B a rc:Impact ;             # violation: no indicator
    rc:hasTarget <http://example.org/my-species> .  # warning: not ENVO or a taxon
"""


RC = Namespace("https://eriktuck.github.io/results-chain-ontology#")
EX = Namespace("http://example.org/data#")

# (focus node, path) of each result chain B is built to produce.
EXPECTED_B = {
    SH.Violation: {
        (EX.Strategy_B, RC.basis),
        (EX.Strategy_B, RC.quotePage),
        (EX.Strategy_B, RC.supportingQuote),
        (EX.Impact_B, RC.hasIndicator),
    },
    SH.Warning: {
        (EX.Strategy_B, SKOS.exactMatch),
        (EX.Impact_B, RC.hasTarget),
    },
}


def run_validation(name: str, data_ttl: str):
    conforms, report, text = validate(
        Graph().parse(data=data_ttl, format="turtle"),
        shacl_graph=Graph().parse(SHAPES, format="turtle"),
        ont_graph=Graph().parse(ONTOLOGY, format="turtle"),
        inference="rdfs",  # so a ThreatReductionResult is also checked as a Result
        abort_on_first=False,
        allow_warnings=True,  # warnings are reported but don't make the graph non-conforming
    )
    print(f"==== {name} ====")
    print(text)
    results = {SH.Violation: set(), SH.Warning: set()}
    for r in report.subjects(SH.resultSeverity, None):
        severity = report.value(r, SH.resultSeverity)
        results.setdefault(severity, set()).add(
            (report.value(r, SH.focusNode), report.value(r, SH.resultPath))
        )
    return conforms, results


def main() -> int:
    ok = True

    conforms_a, results_a = run_validation("Chain A (should conform with no warnings)", CHAIN_A)
    if not conforms_a or any(results_a.values()):
        print("FAIL: chain A should conform with no violations or warnings.")
        ok = False

    _, results_b = run_validation("Chain B (invalid on purpose)", CHAIN_B)
    for severity, expected in EXPECTED_B.items():
        got = results_b.get(severity, set())
        if got != expected:
            label = severity.split("#")[-1]
            print(f"FAIL: chain B {label}s differ from the expected set.")
            for missing in sorted(expected - got):
                print(f"  missing:    {missing}")
            for extra in sorted(got - expected):
                print(f"  unexpected: {extra}")
            ok = False

    print("Validation behaved as expected." if ok else "Validation did not behave as expected.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
