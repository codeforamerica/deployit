venv-deployit: venv-deployit/bin/activate

venv-deployit/bin/activate: requirements.txt
	test -d venv-deployit || virtualenv --no-site-packages venv-deployit
	. venv-deployit/bin/activate; pip install -Ur requirements.txt
	touch venv-deployit/bin/activate
