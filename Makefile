test:
	    python3 -m pytest tests
init:
	    pip install -r requirements.txt

run:
	./run_server.sh

.PHONY: init test

