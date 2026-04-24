# Governance, Security, and Ethics

## Data Classification

This project uses public movie data only.

| Data Field | Classification |
|---|---|
| Movie title | Public |
| Release year | Public |
| Revenue | Public |
| Rating | Public |
| Popularity | Public |
| Distributor | Public |

No personal data or sensitive customer information is used.

---

## Access Control

For a production version of this system:

- Data engineers should have write access to raw and processed data.
- Analysts should have read-only access to analytical tables and views.
- Admin users should manage database credentials and API keys.

---

## API Key Management

API keys should not be hard-coded in scripts or notebooks.

Recommended approach:

```python
import os
api_key = os.getenv("TMDB_API_KEY")