setup :
	python3 -m venv ./venv

fclean :
	rm -rf ./venv

re : fclean setup


.PHONY: setup fclean re