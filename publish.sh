#!/bin/bash

pandoc markdown/abstract.md -o sections/abstract-en.html
pandoc markdown/introduction.md -o sections/introduction-en.html

java -jar widoco.jar -ontFile ./merged_results_chain.ttl -outFolder ./output -confFile widoco.conf -rewriteAll -webVowl -oops

find output/* -maxdepth 0 -not -name 'doc' -exec rm -rf {} +
cp -rl output/doc/* output/
rm -rf output/doc/
mv output/index-en.html output/index.html

cd output
git add .
git commit -m "Site update: $(date)"
git push origin gh-pages
cd ..

echo "🚀 Documentation published to GitHub Pages!"