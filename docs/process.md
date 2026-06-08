# Refactor Process

1. The old educational example was separated into two applications: a Flask API in `backend/` and a SvelteKit UI in `frontend/`.
2. Console interaction and Flask server-rendered templates were removed from the new architecture.
3. SQLite persistence was replaced by PostgreSQL SQL designed for Neon.
4. Business validation was kept in service classes so API routes stay simple.
5. Dockerfiles were added for each application and `docker-compose.yml` was added for local development.

Local container workflow:

```bash
docker compose up --build
curl -X POST http://localhost:5000/setup
```

Then open:

```text
http://localhost:4173
```
