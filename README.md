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

## Zarządzanie gałęziami

Stosujemy model Feature Branching. Nazwa każdej gałęzi musi spełniać wzorzec: `<typ>/<krótki-opis-kebab-case>`.

- **Dozwolone typy**: `feat`, `feature`, `fix`, `docs`, `refactor`, `test`, `chore`, `build`, `ci`.
- **Przykład**: `feat/add-user-repository`.

## Automatyzacja i Pull Request

Proces PR jest w pełni zautomatyzowany i wymusza następujące kroki:

1. **Auto-Format**: Po wysłaniu kodu bot automatycznie poprawi formatowanie. Jeśli bot doda commit, wykonaj `git pull` przed dalszą pracą.
2. **Quality Gates**: PR zostanie zablokowany, jeśli nie zaliczy wszystkich bram jakości: `naming`, `format`, `build` oraz `test`.
3. **Etykiety**: Wymagane jest nadanie dokładnie jednej etykiety: `major`, `minor` lub `patch`.
4. **Code Review**:
   - Wymagane zatwierdzenie przez **Code Ownera**.
   - **Stale Reviews**: Nowy commit na gałęzi automatycznie anuluje poprzednie zatwierdzenia — lider musi sprawdzić kod ponownie.
   - **Dyskusje**: Wszystkie wątki Code Review muszą zostać oznaczone jako rozwiązane (`resolved`).
5. **Merge**: Stosujemy metodę **Squash and Merge**. Twoja historia zostanie spłaszczona do jednego, czystego commita na gałęzi `main`.
