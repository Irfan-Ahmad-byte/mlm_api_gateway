# 🚪 Gateway API (FastAPI + Redis + Docker)

The **Gateway API** serves as the central entry point to multiple microservices including:
- 🔐 Authentication Service
- 💱 Exchange Rate Service
- 🔗 URL Shortener Service

This gateway handles:
- Centralized routing
- Authorization via JWT
- Rate limiting using Redis
- Service-to-service communication via secure API keys

---

## 🧠 Purpose

This project demonstrates:
- Scalable microservices architecture
- Secure API design with multiple authentication levels
- Centralized traffic and rate control
- Practical DevOps via Docker, health checks, and service isolation

---

## 🧱 Tech Stack

- ⚡ FastAPI
- 🐳 Docker + Docker Compose
- 💾 Redis (rate limiting & caching)
- 🔐 JWT-based Auth (via external service)
- 🔄 Async communication with `httpx`
- ⚙️ GitHub Actions (CI/CD ready)

---

## 🔐 Secure Communication

Each connected microservice follows different security policies:

| Service         | Security       |
|----------------|----------------|
| Auth Service    | Public (Bearer Token) |
| Exchange Service| Secured (X-API-Key + JWT) |
| URL Shortener   | Public         |

---

## 🔁 Connected Services

- `/auth/*` → Forwards to **Authentication Service**
- `/exchange/rate/{currency}` → Forwards to **Exchange API** with `Authorization` and API keys
- `/shorten` & `/{short_code}` → Forwards to **URL Shortener**

---

## 📦 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/gateway_service.git
cd gateway_service
```

### 2. Create `.env` file 
Follow `.env.example` file to add Environment Variables.


### 3. Build and run with Docker
```bash
docker-compose up --build
```

API will be available at: http://localhost:8000


## 🔍 API Endpoints
### 🔐 Auth Routes

- POST /auth/login

- GET /auth/me

- POST /auth/logout

- GET /auth/login-history

- POST /auth/refresh

### 💱 Exchange Routes

- GET /exchange/rate/{currency} → Auth + API Key protected

### 🔗 URL Shortener

- POST /shorten → Shortens a URL

- GET /{short_code} → Redirect to original URL


## 🧪 Testing
You can use:

- Postman
- cURL
- Or simple browser for redirection

## 📌 Possible Feature Improvements
- Add OpenTelemetry-based request tracing

- Admin dashboard to monitor services

- JWT signature validation inside gateway

- Multi-tenant support

## 👨‍💻 Author
Built with ❤️ by [Irfan Ahmad](!https://github.com/irfan-ahmad-byte)