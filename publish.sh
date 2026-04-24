#!/bin/bash

# Run WIDOCO
java -jar widoco.jar -ontFile ./merged_results_chain.ttl -outFolder ./output -confFile -rewriteAll widoco.conf -webVowl -oops

# pandoc markdown/abstract.md -o sections/abstract-en.html
# pandoc markdown/introduction.md -o sections/introduction-en.html

# Flatten the structure
mv output/doc/* output/
mv output/index-en.html output/index.html
rmdir output/doc

# Commit and push
cd output
git add .
git commit -m "Site update: $(date)"
git push origin gh-pages
cd ..

echo "Documentation published to GitHub Pages!"
