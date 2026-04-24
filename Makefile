# Variables
PYTHON = uv run python
SRC_DIR = sources
MAP_DIR = mappings
ONT_DIR = ontologies

# Script Paths
CMP_ACT_SCRIPT = $(SRC_DIR)/cmp/actions/parse_cmp_actions.py
CMP_THR_SCRIPT = $(SRC_DIR)/cmp/threats/parse_cmp_threats.py
CE_SCRAPE_SCRIPT = $(SRC_DIR)/conservation_evidence/scrape_conservation_evidence.py
CE_MAP_SCRIPT = $(MAP_DIR)/ce_to_cmp/crosswalk_ce_cmp.py
ENVO_SCRIPT = $(SRC_DIR)/envo/download_envo.py
LOD_SCRIPT = $(SRC_DIR)/lod4stats/download_lod4stats.py
UNBIS_SCRIPT = $(SRC_DIR)/unbis/download_unbis.py
VALIDATE_SCRIPT = scripts/validate_graph.py

# .PHONY prevents conflicts with files of the same name
.PHONY: all help cmp ce envo unbis lod4stats validate clean

# Default target
help:
	@echo "Conservation Knowledge Graph Pipeline"
	@echo "--------------------------------------"
	@echo "Usage:"
	@echo "  make all          - Run the full ingestion and validation pipeline"
	@echo "  make cmp          - Run CMP Actions and Threats ingestion"
	@echo "  make ce           - Scrape Conservation Evidence and run crosswalk"
	@echo "  make envo         - Download latest ENVO ontology"
	@echo "  make unbis        - Download UNBIS Thesaurus"
	@echo "  make lod4stats    - Download SDG mappings (LOD4Stats)"
	@echo "  make validate     - Run SHACL validation on the graph"
	@echo "  make clean        - Remove __pycache__ and temporary files"

# Full Pipeline
all: envo unbis lod4stats cmp ce
	@echo "Full pipeline completed successfully."

# Individual Components
cmp:
	@echo "Processing CMP Actions and Threats..."
	$(PYTHON) $(CMP_ACT_SCRIPT)
	$(PYTHON) $(CMP_THR_SCRIPT)

ce:
	@echo "Scraping Conservation Evidence and generating crosswalk..."
	$(PYTHON) $(CE_SCRAPE_SCRIPT)
	$(PYTHON) $(CE_MAP_SCRIPT)

envo:
	@echo "Downloading ENVO..."
	$(PYTHON) $(ENVO_SCRIPT)

unbis:
	@echo "Downloading UNBIS..."
	$(PYTHON) $(UNBIS_SCRIPT)

lod4stats:
	@echo "Downloading LOD4Stats (SDG Mappings)..."
	$(PYTHON) $(LOD_SCRIPT)

validate:
	@echo "Running SHACL Validation..."
	$(PYTHON) $(VALIDATE_SCRIPT)

clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Tool Versions
ROBOT_VER := v1.9.4
WIDOCO_VER := 1.4.25
WIDOCO_JAR_NAME := widoco-$(WIDOCO_VER)-jar-with-dependencies_JDK-17.jar

# Files
ROBOT := robot.jar
WIDOCO := widoco.jar

# Helper Targets
.PHONY: setup
setup: $(ROBOT) $(WIDOCO)
	@echo "All tools are ready."

# Download ROBOT if not present
$(ROBOT):
	@echo "Downloading ROBOT $(ROBOT_VER)..."
	@curl -L https://github.com/ontodev/robot/releases/download/$(ROBOT_VER)/robot.jar -o $(ROBOT)
	
# Download WIDOCO if not present
$(WIDOCO):
	@echo "Downloading WIDOCO $(WIDOCO_VER)..."
	@curl -L https://github.com/dgarijo/Widoco/releases/download/v$(WIDOCO_VER)/$(WIDOCO_JAR_NAME) -o $(WIDOCO)
	@curl -L https://github.com/dgarijo/Widoco/releases/download/v1.4.25/widoco-1.4.25-jar-with-dependencies_JDK-17.jar
# Merge files
merge: setup
	@echo "Merging ontology..."
	java -jar $(ROBOT) merge \
		--input ontologies/results_chain/results_chain.ttl \
		--catalog catalog-v001.xml \
		--output merged_results_chain.ttl
	@echo "Merging completed."

# Create Documentation
.PHONY: docs
docs: merge setup
	@echo "Converting Markdown to HTML fragments..."
	@mkdir -p sections
	pandoc markdown/abstract.md -o sections/abstract-en.html
	pandoc markdown/introduction.md -o sections/introduction-en.html
	@echo "Running Widoco..."
	java -Xmx8g -jar $(WIDOCO) \
		-ontFile merged_results_chain.ttl \
		-outFolder ./output \
		-confFile widoco.conf \
		-rewriteAll \
		-webVowl \
		-oops
	@echo "Flattening structure for GitHub Pages root..."
	find output/* -maxdepth 0 -not -name 'doc' -exec rm -rf {} +
	cp -rl output/doc/* output/
	rm -rf output/doc/
	mv output/index-en.html output/index.html
	@echo "Documentation generated in ./output"

# Deploy to GitHub Pages
.PHONY: deploy
deploy: docs
	@echo "Pushing to gh-pages branch..."
	cd output && \
	git add . && \
	git commit -m "Site update: $$(date)" && \
	git push origin gh-pages
	@echo "🚀 Documentation published to GitHub Pages!"