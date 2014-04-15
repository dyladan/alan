SYSDEPS := python-virtualenv libxslt1-dev

.PHONY: run
run:
	bin/python alan.py

.PHONY: clean
clean:
	rm -rf bin include lib local __pycache__ *.pyc

.PHONY: setup
setup:
	virtualenv -p python3 .
	bin/pip install -r requirements.txt

.PHONY: sysdeps
sysdeps:
	if [ $(NONINTERACTIVE) ]; then\
		sudo apt-get install -y $(SYSDEPS);\
	else \
		sudo apt-get install $(SYSDEPS); \
	fi
