PYTHON ?= python3
DEMO_SCENARIO := examples/demo.txt

.PHONY: test run

test:
	$(PYTHON) -m unittest discover -s tests -v

run: $(DEMO_SCENARIO)
	$(PYTHON) -m src.cli $(DEMO_SCENARIO)

$(DEMO_SCENARIO):
	mkdir -p $(dir $(DEMO_SCENARIO))
	printf 'START 0 0 N\nOBSTACLE 0 2\nCOMMANDS FFRFF\n' > $(DEMO_SCENARIO)
