# Financial Research Platform

Research platform for analyzing the impact of news on stock market behavior.
Currently tracking semiconductor sector: NVDA, AMD, INTC.

## Quick Start

Requirements: Docker and Docker Compose

```bash
git clone git@github.com:KNMentorAGH/financial-research-platform.git
cd financial-research-platform
cp .env.example .env
docker compose up
```

Available at:

- API: <http://localhost:8000/docs>
- MLflow: <http://localhost:5000>
- PostgreSQL: localhost:5432

To stop: `docker compose down`
To stop and remove data: `docker compose down -v`

## Database

PostgreSQL 16 runs in Docker (`postgres` service) with a healthcheck - the API starts
only after the database is ready.

```bash
# Start only the database
docker compose up -d postgres

# Check connection through the API
curl http://localhost:8000/health/db

# Open psql shell
docker compose exec postgres psql -U postgres -d financial_research
```

Create tables and seed tracked tickers (safe to re-run):

```bash
python -m services.storage.init_db
```

Schema (`services/storage/models.py`):

| Table | Key | Content |
|---|---|---|
| `assets` | `ticker` | tracked tickers from `configs/settings.yaml` |
| `prices` | `ticker, date, interval` | OHLCV bars |
| `news` | `id`, unique `url` | deduplicated articles |
| `news_tickers` | `news_id, ticker` | which tickers an article is about |

Scripts run on your machine connect to `localhost:5432` (values from `.env`).
Shared connection code lives in `services/storage/database.py`
(`get_engine()`, `session_scope()`, `check_connection()`).

## Running the Pipeline

The pipeline orchestrates service execution in configurable order.

```bash
# Run all pipeline steps
python run_pipeline.py --all

# Run specific steps
python run_pipeline.py --steps ingestion sentiment

# Dry run - show what would execute without running
python run_pipeline.py --all --dry-run

# Show help
python run_pipeline.py --help
```

Available steps:

- `ingestion` - fetch news and prices
- `sentiment` - analyze news sentiment
- `forecasting` - predict price direction
- `backtesting` - evaluate strategy performance

