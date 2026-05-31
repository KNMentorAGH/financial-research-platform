# Financial Research Platform

Research platform for analyzing the impact of news on stock market behavior.
Currently tracking semiconductor sector: NVDA, AMD, INTC.

## Working Standards

This project follows organization-wide standards. Before you start, please review:

- [Contributing Guidelines](https://github.com/KNMentorAGH/.github/blob/main/.github/CONTRIBUTING.md)
- [Knowledge Base (SOLID, VSA, Naming)](https://github.com/KNMentorAGH/.github/tree/main/compendium)

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
