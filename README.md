# Server Inventory Manager

A command-line server inventory management application built with **Python and SQLite**, with automated testing, GitHub Actions CI, Docker containerization, Docker Compose, and persistent database storage.

## Overview

The Server Inventory Manager provides a simple way to maintain information about servers in an infrastructure environment.

The application allows users to:

* Add servers
* View server inventory
* Search for servers
* Update server information
* Change server status
* Delete servers
* Generate inventory reports
* Import server data from JSON
* Export server data to JSON

The project also demonstrates basic DevOps practices including automated testing, continuous integration, containerization, and persistent container storage.

---

## Features

### Server Management

* Add new server records
* Validate server information
* Prevent duplicate hostnames
* Search servers by hostname
* Update server information
* Change server status
* Delete servers
* Display inventory reports

### Data Management

* SQLite database for persistent application data
* JSON import and export
* Configurable database path through the `DB_PATH` environment variable

### Testing

* Automated tests using `pytest`
* **19 automated tests**
* Test coverage analysis using `pytest-cov`
* Isolated test database using pytest fixtures

### DevOps

* Git version control
* GitHub repository
* GitHub Actions continuous integration
* Docker containerization
* Docker Compose
* Persistent Docker named volume
* Configurable database location

---

## Technology Stack

| Technology     | Purpose                                |
| -------------- | -------------------------------------- |
| Python         | Application development                |
| SQLite         | Database                               |
| pytest         | Automated testing                      |
| pytest-cov     | Test coverage                          |
| Git            | Version control                        |
| GitHub         | Source code hosting                    |
| GitHub Actions | Continuous integration                 |
| Docker         | Containerization                       |
| Docker Compose | Container configuration and management |
| Docker Volume  | Persistent database storage            |
| Linux          | Development environment                |

---

## Architecture

### Application Architecture

```text
                  User
                   │
                   ▼
             CLI Application
                   │
                   ▼
              Inventory
                   │
             ┌─────┴─────┐
             │           │
             ▼           ▼
        Server Logic   Database
                         │
                         ▼
                       SQLite
```

### DevOps Architecture

```text
Developer
    │
    │ git push
    ▼
 GitHub Repository
    │
    ▼
GitHub Actions
    │
    ├── Install dependencies
    │
    └── Run pytest
            │
            ▼
       PASS / FAIL

Local Deployment
       │
       ▼
     Docker
       │
       ▼
Docker Compose
       │
       ▼
Server Inventory
       │
       ▼
 Docker Volume
       │
       ▼
   SQLite Database
```

---

## Project Structure

```text
serverclass/
│
├── server.py
├── database.py
├── main.py
├── server.json
├── requirements.txt
│
├── Dockerfile
├── compose.yaml
├── .dockerignore
├── .gitignore
│
├── tests/
│   └── test_server.py
│
└── .github/
    └── workflows/
        └── ci.yml
```

### Main files

**`server.py`**

Contains the `Server` and `Inventory` classes and the main inventory management logic.

**`database.py`**

Provides the SQLite database layer and database operations.

**`main.py`**

Provides the command-line interface and application menu.

**`server.json`**

Used for JSON server data import/export.

**`tests/test_server.py`**

Contains the automated pytest test suite.

**`Dockerfile`**

Defines the Docker image used to package the application.

**`compose.yaml`**

Defines the Docker Compose service, environment configuration, and persistent volume.

**`.github/workflows/ci.yml`**

Defines the GitHub Actions continuous integration workflow.

---

# Installation

## Prerequisites

You need:

* Python 3
* Git
* Docker
* Docker Compose

The project was developed on Linux.

---

## Running Locally

Clone the repository:

```bash
git clone <repository-url>
```

Move into the project directory:

```bash
cd serverclass
```

Create a virtual environment:

```bash
python3 -m venv fol_venv
```

Activate it:

```bash
source fol_venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

---

# Testing

Run the complete test suite:

```bash
python -m pytest -v
```

The project currently contains:

```text
19 tests
```

The tests cover server creation, inventory operations, database operations, searching, updating, deleting, status management, reporting, and JSON-related functionality.

---

# Test Coverage

Install the coverage package through the project requirements:

```bash
pip install -r requirements.txt
```

Run the tests with coverage:

```bash
python -m pytest --cov=. --cov-report=term-missing
```

`pytest` verifies application behavior, while `pytest-cov` reports which parts of the code are exercised by the tests.

Coverage is used as a measurement tool and does not by itself guarantee that the application is free of bugs.

---

# Docker

## Build the Docker Image

From the project root:

```bash
docker build -t server-inventory:1.0 .
```

Run the container:

```bash
docker run -it server-inventory:1.0
```

The Docker image packages the Python application and its required dependencies into a reproducible environment.

---

# Docker Compose

The project includes a `compose.yaml` file for running the application with Docker Compose.

Run the application interactively:

```bash
docker compose run --rm server-inventory
```

The `--rm` option automatically removes the temporary container after the application exits.

---

# Database Persistence

The application supports a configurable database path through the `DB_PATH` environment variable.

The Docker Compose configuration uses:

```yaml
environment:
  DB_PATH: /app/data/inventory.db
```

and mounts a named Docker volume:

```yaml
volumes:
  - server_inventory_data:/app/data
```

The storage architecture is:

```text
Container
    │
    ▼
/app/data/inventory.db
    │
    ▼
Docker Named Volume
server_inventory_data
```

The database is therefore stored in a Docker-managed persistent volume rather than only inside the container's writable filesystem.

This means removing and recreating the application container does not normally remove the database.

To inspect Docker volumes:

```bash
docker volume ls
```

To inspect the specific volume:

```bash
docker volume inspect serverclass_server_inventory_data
```

> **Warning:** Removing the volume deletes the persistent database data.

For example:

```bash
docker compose down -v
```

should only be used when intentionally removing the persistent volume.

---

# Configuration

The application supports the following environment variable:

```text
DB_PATH
```

### Default

When `DB_PATH` is not provided:

```text
inventory.db
```

### Docker

Docker Compose configures:

```text
/app/data/inventory.db
```

This allows the application code to remain unchanged while the database location can be changed depending on the environment.

---

# Continuous Integration

GitHub Actions is used to automatically run the Python test suite.

The workflow performs the following:

```text
Git push / Pull Request
        │
        ▼
GitHub Actions
        │
        ▼
Setup Python
        │
        ▼
Install dependencies
        │
        ▼
Run pytest
        │
        ▼
PASS / FAIL
```

The CI workflow runs the automated tests using Python 3.12.

Docker is currently used for local containerization and Docker Compose deployment. The GitHub Actions workflow does **not** currently publish Docker images to a container registry.

---

# Docker Ignore

`.dockerignore` prevents unnecessary files from being included in the Docker build context.

Examples include:

```text
.venv/
fol_venv/
*.db
__pycache__/
.pytest_cache/
.git/
.github/
tests
```

The local SQLite database is excluded because database persistence is handled through the Docker volume.

The virtual environment and test-related files are also unnecessary in the runtime image.

---

# Security Considerations

* Do not commit passwords, API keys, or access tokens to Git.
* Keep credentials outside source code.
* Use GitHub Secrets for CI/CD credentials when required.
* Local virtual environments are excluded from version control.
* Database files are excluded from the Docker build context.
* `.env` files are excluded from the Docker build context.
* GitHub Actions workflow files are version controlled as part of the project.

---

# Current Limitations

This project is intentionally kept as a small infrastructure-management application.

Current limitations include:

* Command-line interface only
* SQLite is intended for lightweight/local use
* No authentication or authorization
* No web interface
* Docker images are not currently published to a container registry
* Docker image building is not currently part of the GitHub Actions workflow
* Deployment to a remote Linux server is not automated
* No dedicated monitoring system

---

# Future Improvements

Possible future extensions include:

* Add a REST API
* Add a web interface
* Add authentication and authorization
* Publish Docker images to GitHub Container Registry
* Add Docker image building to CI
* Automate deployment to a Linux server
* Add application health checks
* Add dependency and container security scanning
* Replace SQLite with PostgreSQL for larger deployments
* Add monitoring with Prometheus and Grafana

These are future improvements and are not currently part of the implemented system.

---

# Learning Outcomes

This project provided practical experience with:

* Python object-oriented programming
* SQLite database management
* CRUD operations
* JSON data handling
* Input validation
* Automated testing
* Test coverage
* Git version control
* GitHub workflows
* Continuous integration
* Docker image creation
* Docker containers
* Docker Compose
* Docker volumes
* Persistent container storage
* Linux-based development

---

# Author

**Kanishk M**

Final-year Mechanical Engineering student transitioning into software and DevOps engineering.

**Project focus:** Python automation, Linux, Docker, testing, Git, and CI/CD fundamentals.
