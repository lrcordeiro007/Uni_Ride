.PHONY: setup run test db-reset db-test clean

setup:
	./dev_tool.sh setup

run:
	./dev_tool.sh run

test:
	./dev_tool.sh test

db-reset:
	./dev_tool.sh db-reset

db-test:
	./dev_tool.sh db-test-setup

clean:
	./dev_tool.sh clean