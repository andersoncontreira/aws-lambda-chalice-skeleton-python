coverage run -m unittest discover -s ./tests/unit -t ./
coverage report
coverage html --omit="*/test*,venv/*" -d ./target/unit/coverage_html/
echo 'results generated in ./target/unit/coverage_html/'