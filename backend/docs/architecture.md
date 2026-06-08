# Backend Architecture

The backend is a small Flask JSON API with a layered structure:

- `app/api`: HTTP routes, JSON parsing, CORS headers and error responses.
- `app/services`: business rules and input validation.
- `app/repositories`: PostgreSQL queries using parameterized SQL.
- `app/domain`: dataclasses used by services and repositories.
- `app/infrastructure`: database connection and schema initialization.

The routes do not contain business rules. They receive JSON, call a service and return JSON. The services validate input before creating domain objects. The repositories are the only layer that talks to SQL.

Run the backend with the configured virtual environment:

```bash
cd backend
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql://clinic:clinic@localhost:5432/clinic"
python -m app
```

Initialize the database schema:

```bash
curl -X POST http://localhost:5000/setup
```
