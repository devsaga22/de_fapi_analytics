Time-Series Analytics Pipeline (FastAPI + TimescaleDB)
Developed by: devsaga22

A high-performance data engineering pipeline designed to ingest, store, and analyze web traffic clickstream data in real-time. This project demonstrates a transition from traditional Relational DB logic to specialized Time-Series Analysis.
We are trying to simulate a live website/app with many users like amazon,swiggy,netflix etc and this is the pipeline that catches the user interaction and time spent data into db so the ML/DS/DA team can further process to get insights.

🏗️ Architecture & Stack
Language: Python 3.13

API Framework: FastAPI (Asynchronous ingestion)

Database: TimescaleDB (PostgreSQL extension for time-series)

ORM: SQLModel (Pydantic + SQLAlchemy)

Infrastructure: Docker & Docker Compose

Tools: Jupyter Notebooks (for analytical prototyping), Python-Decouple (Environment management)

🌟 Key Features
Hypertable Integration: Optimized EventModel using TimescaleDB Hypertables for efficient partitioning by time.

Analytical Ingestion: A custom seeding engine that simulates real-world traffic with varied timestamps.

Advanced Time-Series Queries: \* time_bucket aggregation for daily/hourly reporting.

variable hours sliding window lookbacks using Python timedelta.

Containerized Environment: Fully orchestrated via Docker for consistent "One-Command" deployment.

🛠️ How to Run Locally

1. Clone & Setup Environment
   Bash
   git clone https://github.com/devsaga22/de_fapi_analytics.git
   cd de_fapi_analytics

# Create a .env file like .env.compose

    PORT=
    DATABASE_URL=
    to  be used in the docker-compose.yml file so the docker container communicate over the container network

2. Launch with Docker
   docker compose up --build
3. Seed & Analyze
   Open the notebook to test and seed the dbs
   3-send-data-to-the-api.ipynb
   Generate mock traffic data when u need so its not very old

Run the SQLModel aggregation queries in 4-tdb-queries.ipynb

NOTE: when u use ipynb and wanna interact with db directly without apis inside the container u need to use the localhost in db_url
to identify the service as per the port u matched in the compose.

Have fun
