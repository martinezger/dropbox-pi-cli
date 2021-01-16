build:
	python3 setup.py sdist bdist_wheel

install:
	python3 -m pip install dist/*.whl

uninstall:
	python3 -m pip uninstall dist/*.whl

release:
	python3 -m twine upload --repository pypi dist/*

