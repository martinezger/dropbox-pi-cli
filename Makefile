build:
	python3 setup.py sdist bdist_wheel

install:
	python3 -m pip install dist/dropbox_pi_cli-0.0.1-py3-none-any.whl

uninstall:
	python3 -m pip uninstall dist/dropbox_pi_cli-0.0.1-py3-none-any.whl

release:
	python3 -m twine upload --repository pypi dist/*

