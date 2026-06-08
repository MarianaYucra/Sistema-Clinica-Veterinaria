# Project Architecture

The repository is organized around two applications:

```text
backend/
  app/
    api/
    domain/
    infrastructure/
    repositories/
    services/
frontend/
  src/
    routes/
    app.css
docs/
```

The frontend calls the backend through `VITE_API_URL`. The backend calls PostgreSQL through `DATABASE_URL`.

This keeps the example simple:

- Flask owns HTTP and validation-backed use cases.
- Svelte owns the user interface.
- PostgreSQL owns persistence.
- Docker owns runtime packaging.
