# CSR Blog API

A small Flask project for managing blog posts through a REST API. It includes a simple frontend and interactive API documentation powered by Swagger UI.

## Setup

Install the required packages:

```powershell
python -m pip install flask flask-cors flask-swagger-ui
```

## Run the project

Start the backend:

```powershell
python backend/backend_app.py
```

Optionally, start the frontend in a second terminal:

```powershell
python frontend/frontend_app.py
```

- Frontend: <http://127.0.0.1:5001>
- Swagger documentation: <http://127.0.0.1:5002/api/docs/>

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/posts` | List and sort posts |
| `POST` | `/api/posts` | Create a post |
| `GET` | `/api/posts/search` | Search posts |
| `PUT` | `/api/posts/{post_id}` | Update a post |
| `DELETE` | `/api/posts/{post_id}` | Delete a post |

The Swagger definition is stored in `backend/static/csr_api.json`.
