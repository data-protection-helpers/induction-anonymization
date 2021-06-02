Statistical Generative Modeling
===============================

# Overview
Source:
  * [The Synthetic Data Vault : generative modeling for relational databases](https://dspace.mit.edu/handle/1721.1/109616),
  * By [Neha R. Patki](https://www.linkedin.com/in/nehapatki/)

# Quick starter

* Install PyEnv:
```bash
$ git clone https://github.com/pyenv/pyenv.git $HOME/.pyenv
$ cat >> ~/.bashrc << _EOF

# Python
export PYENV_ROOT="\${HOME}/.pyenv"
export PATH="\${PYENV_ROOT}/bin:\${PATH}"
if command -v pyenv 1>/dev/null 2>&1
then
        eval "\$(pyenv init -)"
fi
if command -v pipenv 1>/dev/null 2>&1
then
        eval "\$(pipenv --completion)"
fi

_EOF
$ . ~/.bashrc
```

* Install Python 3.9.5:
```bash
$ pyenv install 3.9.5 && pyenv local 3.9.5
$ python -V
Python 3.9.5
$ python -mpip install -U pip pipenv
```

* Install the Python virtual environment:
```bash
$ pipenv --rm; pipenv install; pipenv install --dev
```

* Launch Jupyter Lab:
```bash
$ pipenv run jupyter lab
```

* It should open the browser on http://localhost:8888/lab

* Double-click on
  [`statistical_generative_modeling.ipynb`](https://github.com/data-protection-helpers/induction-anonymization/blob/master/mit-anonymization/python/statistical_generative_modeling.ipynb)

* Enjoy!

# Contributions
[Pull requests](https://github.com/data-protection-helpers/induction-anonymization/pulls)
are preferred.
[Issues/tickets](https://github.com/data-protection-helpers/induction-anonymization/issues)
are welcome too.


