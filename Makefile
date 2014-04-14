SYSDEPS := python-virtualenv

.PHONY: clean
clean:
	rm -rf bin include lib local __pycache__ *.pyc

.PHONY: run
run:
	bin/python bot.py

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
