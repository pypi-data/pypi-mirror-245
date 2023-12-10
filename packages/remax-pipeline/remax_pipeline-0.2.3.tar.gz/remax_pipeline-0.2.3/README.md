# Data Pipeline for Real Estate Analytics


## Project Overview

This project is `python library` used to implement an efficient `web scraping` `ETL` (Extract, Transform, Load) solution. 

This project is published as a  package in `PyPI` to pip install and use to automate the ETL process via scheduled job and deploying celery workers.

Click [here](https://pypi.org/project/remax-pipeline/) to view package.

The library uses `Celery`, an `asynchronous task queue`, in conjunction with `RabbitMQ` as a message broker. The workers, implemented with `multithreaded` selenium web drivers, allow for parallel celery workers running multithreaded scraping of listings from the REMAX website. The extracted data undergoes transformation and validation based on a predefined `data contract` before being stored in an `SQL database` for long term analytics. 


## Project Diagram


<img src="https://github.com/AymenRumi/remax-data-pipeline/blob/main/assets/diagram.png">


## Installation

```bash
pip install remax_pipeline
```

### Environment Variables 
```bash
# These must be set before importing from the module (can also be set with .env file)

export POSTGRES_DBNAME="remaxpipeline"
export POSTGRES_USER="myuser"
export POSTGRES_PASSWORD="mypassword"
export POSTGRES_HOST="localhost"
export POSTGRES_PORT="5432"

export CELERY_RABBITMQ_BROKER="amqp://myuser:mypassword@localhost:5672/"
export CELERY_APP_NAME="celery_app"

```

<!-- 
##  Key Features:

> This projects is an end-to-end deployed ETL pipeline using Data Engineering and DevOps best practice with considerations for efficiency and scalability. Thousands of listings are scraped from the web daily and modelled & stored for long term analytics.

* **Multithreaded Scraping** Utilizes multiple threads to scrape home listings concurrently, significantly speeding up the process.
* **Parallel Processing**: Employs Airflow's Celery Executor with Redis to scrape chunks of pages in parallel.
* **Data Contract**: Implements a `data contract` using `Pydantic` for validating scraped data before storage.
* **PostgreSQL Integration**: Stores validated data in a `PostgreSQL` database.
* **Slowly Changing Dimensions (SCD) Modeling**: Executes a subsequent job to model `SCD`s in the database.
* **AWS Deployment**: The entire pipeline is deployed on `AWS`.
* **CD with GitHub Actions**: Automated deployment and integration using `GitHub Actions`.
* **Infrastructure as Code**: Uses `Terraform` for creating and managing infrastructure.


## Folder Structure

    .
    ├── build                   # Compiled files (alternatively `dist`)
    ├── docs                    # Documentation files (alternatively `doc`)
    ├── src                     # Source files (alternatively `lib` or `app`)
    ├── test                    # Automated tests (alternatively `spec` or `tests`)
    ├── tools                   # Tools and utilities
    ├── LICENSE
    └── README.md


 -->
