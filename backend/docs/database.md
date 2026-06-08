# Database

The application uses PostgreSQL-compatible SQL, suitable for Neon.

Required environment variable:

```bash
DATABASE_URL="postgresql://USER:PASSWORD@HOST:PORT/DATABASE?sslmode=require"
```

Main tables:

- `clientes`: client identity, phone and unique email.
- `veterinarios`: veterinarian identity and specialty.
- `mascotas`: pets linked to `clientes`.
- `citas`: appointments linked to `mascotas` and `veterinarios`.
- `registros_clinicos`: clinical records created when an appointment is completed.

Important constraints:

- Primary keys protect identity fields.
- `clientes.email` is unique.
- Foreign keys keep pets, appointments and clinical records consistent.
- `mascotas.edad` and `mascotas.peso` have range checks.
- A partial unique index prevents two active appointments for the same veterinarian at the same date and time.

The schema is created by `POST /setup`, defined in `app/infrastructure/database.py`.
