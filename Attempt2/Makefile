.PHONY: test
test:
	@echo "--------------------RUNNING TESTS--------------------"
	pytest -q tests/testLexer.py
	pytest -q tests/testParser.py
	pytest -q tests/testInterpreter.py

.PHONY: generate-ast
generate-ast:
	cd tools && python3 generate_ast.py

.PHONY: run
run:
	python3 emlang.py tests/eml/test_dev.eml