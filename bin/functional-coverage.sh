coverage run -m unittest discover -s ./tests/functional -t ./
coverage report
coverage html --omit="*/test*,venv/*" -d ./target/functional/coverage_html/
echo 'results generated in ./target/functional/coverage_html/'