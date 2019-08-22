format:
	autoflake -r --in-place --remove-unused-variables --remove-all-unused-imports ./nfe_reader ./tests
	isort --check-only -rc .
	black --check ./nfe_reader ./tests
	flake8 ./nfe_reader

test:
	pytest . --cov=.
