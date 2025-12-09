# arXiv Data Dive

The arXiv is the largest online repository of academic information, including over 2.9M research articles
spanning the last four decades on topics like physics, computing, and other sciences.
The **arXiv Data Dive** establishes a robust pipeline for ingesting and normalizing metadata for these articles,
and creates a foundation for conducting in-depth analyses of research trends.

This project is easily deployable to AWS Lambda / AWS RDS,
and is designed with scheduled ingestion (via AWS EventBridge) in mind.

### Project Setup

Project dependencies can be installed with `venv`:

```
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

Exact commands may vary depending on platform. Ensure the `PYTHONPATH` includes the `src/` directory.

The data ingestion portion of the project also requires a connection to a postgres database.
Connection parameters are sourced from the environment ( `ARXIN_DB_URL`,  `ARXIN_DB_USER`, `ARXIN_DB_PASS`).

### Running the tests

Install dev dependencies:

```pip install -r requirements-dev.txt```

Run the tests:

```pytest```

For coverage, instead run:

```
coverage run --source=src -m pytest
coverage report -m
```

### Deploying to AWS

Requires `7z` and `aws` CLI utilities. Run from the project root. Only tested for Windows + Git Bash.
Needs IAM access to deploy to Lambda.

```./deploy/deploy.sh```

The script packages all the necessary files into a zip archive and deploys to AWS.
Most notably, all the Python dependencies are installed into the bundle.