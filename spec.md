# Subscope SaaS - Developer Specification

## 🧠 Overview

**Subscope** is a subscription and bill reminder application for individuals. It enables users to manage recurring expenses, receive reminder emails, and visualize their spending. The backend is built as a unified **monolithic FastAPI application**.

- **Architecture:** Monolith (FastAPI), NextJS
- **Deployment:** Docker + AWS Lightsail (Cost-Optimized)

---

## 🧩 Tech Stack

| Layer            | Technology                              |
|------------------|------------------------------------------|
| Frontend         | Next.js + Tailwind CSS + shadcn/ui       |
| Backend API      | FastAPI (Python)                         |
| Database         | Amazon RDS PostgreSQL (Free Tier or T4g.micro) |
| Email Delivery   | AWS SES (free tier)                      |
| Auth             | JWT (email/password)                     |
| CI/CD            | GitHub Actions                           |
| Deployment       | AWS Lightsail (Ubuntu + Docker)          |

---

## 📦 Core Features

Feature
| Subscriptions
| Email Reminders
| Spending Analytics
| CSV/PDF Export
| Custom Tags
| Welcome Email

---

## 🔐 Auth Model

- JWT-based authentication
- Email/password login only

```sql
users (
  id UUID PRIMARY KEY,
  email TEXT UNIQUE,
  password_hash TEXT,
  full_name TEXT,
  currency TEXT DEFAULT 'USD',
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
```

---

## 📊 Subscription Model

```sql
subscriptions (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  amount NUMERIC(10, 2),
  currency TEXT DEFAULT 'USD',
  billing_cycle TEXT CHECK (billing_cycle IN ('monthly', 'yearly')),
  next_due_date DATE NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)

tags (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  UNIQUE (user_id, name)
)

subscription_tags (
  subscription_id UUID REFERENCES subscriptions(id),
  tag_id UUID REFERENCES tags(id),
  PRIMARY KEY (subscription_id, tag_id)
)

reminders (
  id UUID PRIMARY KEY,
  subscription_id UUID REFERENCES subscriptions(id) ON DELETE CASCADE,
  remind_at TIMESTAMP NOT NULL,
  is_recurring BOOLEAN DEFAULT TRUE,
  sent BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT now()
)
```

---

## 📬 Reminder Emails

- Handled by internal background task scheduler (APScheduler or FastAPI lifespan task)
- Periodically scans upcoming reminders
- Sends via AWS SES (free tier)
- Logs each attempt:

```sql
notification_logs (
  id UUID PRIMARY KEY,
  reminder_id UUID REFERENCES reminders(id) ON DELETE CASCADE,
  channel TEXT CHECK (channel IN ('email')),
  status TEXT CHECK (status IN ('sent', 'failed')),
  message TEXT,
  error TEXT,
  sent_at TIMESTAMP
)
```

---

## 📤 Data Export

- `/export?format=csv|pdf`

---

## 🧪 Testing Plan

- Unit Testing: `pytest`, `pytest-asyncio`
- HTTP Testing: `httpx`
- Background Jobs: Use APScheduler mocks
- Integration tests: `pytest` + `docker-compose`
- Coverage: Enforce >90%

---

## 📡 API Endpoints (JSON Contracts)

### Auth

- `POST /auth/register` → { email, password, full_name }
- `POST /auth/login` → { email, password } → { access_token }
- `GET /auth/me` → Authenticated User Info

### Subscriptions

- `GET /subscriptions/` → List
- `POST /subscriptions/` → Create
- `GET /subscriptions/{id}` → Retrieve
- `PUT /subscriptions/{id}` → Update
- `DELETE /subscriptions/{id}` → Delete

### Tags

- `GET /tags/` → List
- `POST /tags/` → Create
- `DELETE /tags/{id}` → Delete

### Reminders

- Auto-generated from subscription settings
- Internal use only: `POST /reminders/schedule`

### Export

- `GET /export?format=csv|pdf`

---

## ⚙️ CI/CD and Deployment

- GitHub Actions pipeline: lint, test, build
- Docker-based deployment to:
  - AWS Lightsail instance (Ubuntu + Docker preinstalled)
- PostgreSQL via Amazon RDS (Free Tier)
- Environment variables via `.env`(local) or AWS Parameter Store(production)

---

## 📘 Dev Onboarding

- Single repo
- `.env.example` and Dockerfile
- Local Dev: `uvicorn main:app --reload`
- Setup instructions in `README.md`

---

## ✅ Summary

Subscope is now structured as a **single production-grade FastAPI monolith** optimized for **easy and low-cost AWS Lightsail deployment**. It relies on SES, RDS with GitHub CI/CD for an efficient MVP launch.
