define USAGE
Super awesome hand-crafted build system ⚙️

Commands:
	init      Install Python dependencies with pipenv
	test      Run tests
	serve     Run app in dev environment.
endef

export USAGE
help:
	@echo "$$USAGE"

init:
	pip3 install -r requirements.txt

test:
	pytest -v planet/tests

serve:
	FLASK_APP=planet flask run