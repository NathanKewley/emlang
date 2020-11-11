.PHONY: test
test:
	@echo "--------------------RUNNING TESTS--------------------"
	pytest -q tests/testLexer.py --color yes -rapP
	pytest -q tests/testParser.py --color yes -rapP
	pytest -q tests/testInterpreter.py --color yes -rapP
	pytest -q tests/testBinary.py --color yes -rapP

.PHONY: generate-ast
generate-ast:
	cd tools && python3 generate_ast.py

.PHONY: run
run:
	python3 emlang.py tests/eml/test_dev.eml