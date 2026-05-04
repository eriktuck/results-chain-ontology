from pyshacl import validate
from rdflib import Graph

# Define the SHACL Shapes file path
shacl_shapes = "ontologies/shapes/results_chain_shapes.shacl.ttl"

# Sample Data (One valid, one invalid)
# - "Project_A" is valid.
# - "Project_B" is invalid because Strategy has no skos:exactMatch and Impact has no indicator.
sample_data = """
@prefix rc: <https://eriktuck.github.io/results-chain-ontology#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix ex: <http://example.org/data#> .

# VALID DATA
ex:Strategy_A a rc:Strategy ;
    skos:exactMatch <https://conservationstandards.org/library-item/1.1> ;
    rc:leadsTo ex:Result_A .

ex:Result_A a rc:Result ;
    rc:leadsTo ex:Impact_A .

ex:Impact_A a rc:Impact ;
    rc:hasIndicator ex:Indicator_1 .

ex:Indicator_1 a rc:Indicator .

# INVALID DATA
ex:Strategy_B a rc:Strategy ;
    rc:leadsTo ex:Impact_B . # Fails: No skos:exactMatch

ex:Impact_B a rc:Impact . # Fails: No indicator
"""

def run_validation():
    # Load data and shapes into RDFLib Graphs
    data_graph = Graph().parse(data=sample_data, format="turtle")
    shacl_graph = Graph().parse(shacl_shapes, format="turtle")

    print("--- Running SHACL Validation ---")
    
    # Run validation
    # ont_graph=None because we aren't using complex RDFS reasoning here, 
    # but you can pass your ontology file there if needed.
    conforms, results_graph, results_text = validate(
        data_graph,
        shacl_graph=shacl_graph,
        inference='rdfs', # Helps recognize subclasses like ThreatReductionResult as Results
        abort_on_first=False,
        serialize_report_graph=True
    )

    if conforms:
        print("✅ Validation Success: Data conforms to the Results Chain shapes.")
    else:
        print("❌ Validation Failed!")
        print("-" * 30)
        print(results_text) # This prints a human-readable summary of errors

if __name__ == "__main__":
    run_validation()