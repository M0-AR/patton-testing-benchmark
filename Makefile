.PHONY: verify test live report
live:
	python3 scripts/fetch_live_data.py
test:
	PYTHONPATH=src python3 -m pytest -v --tb=short
report:
	mkdir -p test-results && PYTHONPATH=src python3 -m pytest -v --tb=short --junitxml=test-results/junit.xml | tee test-results/benchmark.txt
verify: live test report
	@echo "VERIFY OK: live data + pytest green (see test-results/)"
