.PHONY: test
test:
	pytest -q tests/test_lexer.py --import-mode=prepend

.PHONY: generate-ast
generate-ast:
	cd tools && python3 generate_ast.py

.PHONY: run
run:
	python3 emlang.py tests/eml/test_dev.eml