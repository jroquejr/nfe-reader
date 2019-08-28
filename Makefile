format:
	autoflake -r $(AUTOFLAKE_OPTIONS) --remove-unused-variables --remove-all-unused-imports ./nfe_reader ./api ./tests
	isort -rc . $(ISORT_OPTIONS)
	black --exclude '.*/(snapshots|snapshottest)/.*' $(BLACK_OPTIONS) ./nfe_reader ./api ./tests

check-format: ISORT_OPTIONS := --check-only
check-format: BLACK_OPTIONS := --check
check-format: format
	flake8 ./nfe_reader ./api

test: check-format
	pytest . --cov=. $(PYTEST_OPTIONS)


coverage: PYTEST_OPTIONS := --cov-report html
coverage: test
	open htmlcov/index.html
