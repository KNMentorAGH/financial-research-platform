# Financial Research Platform

Research platform for analyzing the impact of news on stock market behavior.
Currently tracking semiconductor sector: NVDA, AMD, INTC.

## 🛠️ Standardy pracy

Projekt korzysta z globalnych standardów. Zanim zaczniesz, zapoznaj się z:

- [Zasady współpracy (Contributing)](https://github.com/KNMentorAGH/.github/blob/main/.github/CONTRIBUTING.md)
- [Baza wiedzy (SOLID, VSA, Naming)](https://github.com/KNMentorAGH/.github/tree/main/compendium)

## 🚀 Quick Start

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
