# Frontend

SvelteKit client for the veterinary clinic API.

```bash
cd frontend
pnpm install
VITE_API_URL=http://localhost:5000 pnpm dev
```

The first screen is the operational app. It includes summary counters, create forms and lists for clients, veterinarians, pets and appointments.

All submitted data is still validated in the Flask backend. Browser validation is only a first usability layer.
