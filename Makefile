.PHONY: format check

format:
	black pv_simulator
	isort pv_simulator

check:
	echo 'Checking code format with black...'
	black --check pv_simulator
	echo 'Checking import order...'
	isort --check pv_simulator
	echo 'Running flake8...'
	flake8 pv_simulator --config=.flake8
	echo 'Running mypy...'
	mypy pv_simulator --config=mypy.ini

