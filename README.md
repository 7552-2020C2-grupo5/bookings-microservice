# booking-microservice
![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/7552-2020C2-grupo5/bookings-microservice?style=flat-square) ![Coverage](coverage-badge.svg)[![Tests](https://github.com/7552-2020C2-grupo5/bookings-microservice/actions/workflows/tests.yml/badge.svg)](https://github.com/7552-2020C2-grupo5/bookings-microservice/actions/workflows/tests.yml)[![Linters](https://github.com/7552-2020C2-grupo5/bookings-microservice/actions/workflows/linters.yml/badge.svg)](https://github.com/7552-2020C2-grupo5/bookings-microservice/actions/workflows/linters.yml)[![Bandit](https://github.com/7552-2020C2-grupo5/bookings-microservice/actions/workflows/bandit.yml/badge.svg)](https://github.com/7552-2020C2-grupo5/bookings-microservice/actions/workflows/bandit.yml)![](https://heroku-badge.herokuapp.com/?app=bookbnb5-bookings-microservice)

Booking microservice for BookBNB

# Installing the project
This project was built with [poetry](https://python-poetry.org) in mind as the means to manage dependencies. You can follow their [install guide](https://python-poetry.org/docs/#installation) to install it.

Having poetry installed, the following command will install the project into a new environment.

```bash
poetry install
```

Keep in mind that this will by default install the base requirements as well as the dev requirements.

To install the `testing` extras, run:

```bash
poetry install -E testing
```

Remember to commit to the repo the `poetry.lock` file generated by `poetry install`.

# Dev

## Installing pre-commit hooks
We use [pre-commit](https://pre-commit.com) to run several code scans and hooks that make the development cycle easier.
```bash
pre-commit install
pre-commit install -t push
```

## Adding new dependencies
Check the full [poetry](https://python-poetry.org) docs, but here goes a quick reminder,

```bash
poetry add <dependency> [--dev]
```

*Always* remember to commit changes to `poetry.lock`!

## Bumping SemVer version
We use [SemVer](https://semver.org). To keep things easy, dev dependencies include [bump2version](https://pypi.org/project/bump2version/) . Running `poetry run bump2version minor` will bump the minor version.

```bash
poetry run bump2version <part>
```

## Running nox sessions
In order to bootstrap dependencies and run several actions, we are using [nox](https://nox.thea.codes/en/stable/). This way, dependencies are isolated and you get environment replicability.

To run all sessions,
```bash
nox
```

To run tests session,
```bash
nox --sessions tests [-- pylint arguments]
```

To run linting session,
```bash
nox --sessions cop
```

To run bandit session,
```bash
nox --sessions bandit
```

To run pyreverse session,
```bash
nox --sessions pyreverse
```

## Style guide
booking_microservice follows [PEP8](https://www.python.org/dev/peps/pep-0008/).

If you installed the [pre-commit hooks](#installing-pre-commit-hooks) you shouldn't worry too much about style, since they will fix it for you or warn you about styling errors. We use the following hooks:

- [black](https://github.com/psf/black): An opinionated code formatting tool that ensures consistency across all projects using it
- [flake8](https://github.com/PyCQA/flake8): a tool to enforce style guide
- [mypy](https://github.com/python/mypy): a static type checker for Python
- [pylint](https://github.com/PyCQA/pylint): a source code, bug and quality checker

## Docstrings
We use either [numpy style](https://numpydoc.readthedocs.io/en/latest/format.html) or [google style](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings) docstring formatting. It's usually good to include the following docstrings:
- module level docstring giving a general overview of what it does.
- class dosctrings explaining what it is
- method/functions to explain what it does and what it's parameters are

## Testing
We use the [pytest framework](https://docs.pytest.org/en/latest/) to test booking_microservice. The easiest way to run tests it through `nox` with `nox --sessions tests`.

# Docker

Get everything up and running.

```bash
cd docker-compose
docker-compose build
docker-compose up
```

# Deploy to heroku
You will need to have the [heroku cli](https://devcenter.heroku.com/articles/heroku-cli) installed and correctly configured for the following steps.

Prior to the actual deploy, **make sure to commit your changes**.

```bash
heroku create booking_microservice
heroku addons:create heroku-postgresql:hobby-dev
heroku stack:set container
git push heroku master
```

1. The first step [initializes](https://devcenter.heroku.com/articles/creating-apps) a new heroku app
2. The second step provisions a [postgres addon](https://www.heroku.com/postgres)
3. The third step sets the app to use [a docker image](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml). Instead of using a [Procfile](https://devcenter.heroku.com/articles/procfile), we will use a `heroku.yml`. Heroku does not yet support a [poetry buildpack](https://github.com/python-poetry/poetry/issues/403) and exporting a `requirements.txt` from poetry is pretty cumbersome.
4. Deploy 🚀

## Diagnosing errors
You can fetch logs from the app using `heroku logs --tail`.

## CD
Go to the app on the [Heroku Dashboard](https://dashboard.heroku.com). On the deploy tab, select "Connect to github" under the "Deployment method" section. Select your repo and you're good to go. Pushes to master will deploy a new version.

## Is the app running?
Free dynos sleep after [30 min](https://devcenter.heroku.com/articles/free-dyno-hours#dyno-sleeping) if no incoming web traffic is received. It might take a while, but you should be able to see the app's swagger the root URL. Use the "Open App" button on the dashboard.

## DataDog
The heroku Dockerfile includes the DataDog agent.
Create a new DataDog API Key from [here](https://app.datadoghq.com/account/settings#api).
Remember to set the following config vars:
```bash
heroku config:set DD_API_KEY=<your_api_key>
heroku config:set DD_DYNO_HOST=false
heroku config:set HEROKU_APP_NAME=bookbnb5-bookings
heroku config:set DD_TAGS=service:booking_microservice
```

# GitHub Actions
A few pipelines have been set to run on github actions to ensure code quality.

## `sessions.yml`
This workflow runs linters and tests.

# Documentation

## Swagger
You can visit the swagger docs at `127.0.0.1:5000`.

## Whole project class diagram
![project_classes](docs/images/project_classes.png)

## Packages
![packages](docs/images/packages_dependencies.png)
