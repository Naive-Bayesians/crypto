# crypto

## First Time Setup

1. Install PyEnv to manage python installations. `brew install pyenv`

2. Add the following lines to your `~/.bash_profile`

    ```bash

    export PATH="~/.pyenv/bin:$PATH"

    eval "$(pyenv init --path)"

    eval "$(pyenv virtualenv-init -)"

    ```

3. Open a new terminal window or `source ~/.bash_profile`

4. Install the latest version of Python using `pyenv install 3.9.6`

5. Check if your system python is the same `python --version`

6. Install poetry

 

    ```bash

    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

    source ~/.poetry/env

    ```

 
7. Set your virtual env to be within your project

    ```bash

    poetry config virtualenvs.in-project true

    ```

 

## Running Experiments

```bash
poetry install
poetry run main
```

Runs are configured using the configs in `configs/config.yaml`. Every run automatically creates an `output/` subdirectory within your experiment directory with a time stamp for all the artefacts (files, logs, configs).

Create a new experiment by creating a new subfolder e.g. `exp_ABC ` in the `experiments` folder.

 

```bash

└── exp_ABC
    ├── __init__.py
    ├── experiment.py
    ├── notebooks
    │   ├── notebook_A.ipynb
    │   └── notebook_B.ipynb
    └── output
        ├── 2021-07-23_11-43-53
        └── 2021-07-23_11-46-02

```

You can tell which experiment to run by setting the name in the experiment section of the config.
The application finds the experiment using the name of the subdirectory that matches the experiment name and finds a `run()` method in it.
All config params can be accessed via the dot notation `cfg.param1.subparam2`

 

### Running Tests

```bash
poetry run pytest
```
with coverage `poetry run pytest --cov`.

 
### Notebooks
To launch a Jupyter Notebook from your poetry environment use `poetry shell` (similar to `pipenv shell`), then launch jupyter notebook.

```bash
poetry shell
jupyter-notebook

```

### Poetry Cheat Sheet
To create environment

```bash
    poetry config virtualenvs.in-project true
    poetry install
 ```

 
To add dependencies

```bash
poetry add <name-of-dependency>
```


e.g.
```bash
poetry add pandas
```


or

```bash
poetry update click
poetry add click^7.0

```

To remove packages

```bash
poetry remove pandas
```

 

