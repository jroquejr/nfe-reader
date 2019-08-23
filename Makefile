format:
	autoflake -r $(AUTOFLAKE_OPTIONS) --remove-unused-variables --remove-all-unused-imports ./nfe_reader ./tests
	isort -rc . $(ISORT_OPTIONS)
	black --exclude '.*/(snapshots|snapshottest)/.*' $(BLACK_OPTIONS) ./nfe_reader ./tests 

check-format: ISORT_OPTIONS := --check-only
check-format: BLACK_OPTIONS := --check
check-format: format
	flake8 ./nfe_reader

test: check-format
	pytest . --cov=.
