build:
	python3 setup.py sdist bdist_wheel

release:
	python3 -m twine upload --repository pypi dist/*

