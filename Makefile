setup :
	python -m venv ./venv

fclean :
	rm -rf ./venv

re : fclean setup


.PHONY: setup fclean