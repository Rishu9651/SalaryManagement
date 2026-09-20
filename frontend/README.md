# ACME Salary Management Frontend

## Setup

Install dependencies:

```bash
npm install
```

Copy `.env.example` to `.env` and configure the backend URL:

```bash
VITE_API_BASE_URL=http://localhost:8000
```

Run the frontend:

```bash
npm run dev
```

The initial page calls `GET /health` and displays loading, success, or error status.

## Checks

```bash
npm run build
npm run lint
```

No frontend test runner was configured in the existing Vite setup, so tests were not added for this foundation step.
