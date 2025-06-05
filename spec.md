# Subscope SaaS - Developer Specification (Monolith Edition - AWS Lightsail Optimized)

## 🧠 Overview

**Subscope** is a subscription and bill reminder SaaS application for individuals. It enables users to manage recurring expenses, receive reminder emails, and visualize their spending.

- **Target Users:** Individuals
- **Platform:** Web-based SaaS
- **Architecture:** FastAPI
- **Deployment:** Docker + AWS Lightsail (Cost-Optimized)

---

## 🧩 Tech Stack

| Layer              | Technology                                     |
| ------------------ | ---------------------------------------------- |
| Frontend           | Next.js + Tailwind CSS + shadcn/ui             |
| Backend API        | FastAPI (Python)                               |
| Database           | Amazon RDS PostgreSQL (Free Tier or T4g.micro) |
| Email Delivery     | AWS SES (free tier)                            |
| Billing & Payments | Stripe (free dev plan)                         |
| Auth               | JWT (email/password)                           |
| Monitoring         | PostHog (free plan)                            |
| CI/CD              | GitHub Actions                                 |
| Deployment         | AWS Lightsail (Ubuntu + Docker)                |

---

## 📦 Core Features

| Feature            | Free Plan | Pro Plan    |
| ------------------ | --------- | ----------- |
| Max Subscriptions  | 5         | Unlimited   |
| Email Reminders    | ✅        | ✅          |
| Spending Analytics | ✅ Basic  | ✅ Advanced |
| CSV/PDF Export     | ❌        | ✅          |
| Custom Tags        | ❌        | ✅          |
| Welcome Email      | ✅        | ✅          |

---

## 🔐 Auth Model

- JWT-based authentication
- Email/password login only
- Middleware to enforce `plan == 'pro'` for premium features

```sql
users (
  id UUID PRIMARY KEY,
  email TEXT UNIQUE,
  password_hash TEXT,
  full_name TEXT,
  plan TEXT CHECK (plan IN ('free', 'pro')),
  currency TEXT DEFAULT 'USD',
  valid_until TIMESTAMP,
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

## 💳 Billing Model

- Uses Stripe Checkout
- Webhooks handled by unified FastAPI route
- Cancellation via `cancel_at_period_end = true`

```sql
billing_events (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  event_type TEXT,
  stripe_event_id TEXT UNIQUE,
  receipt_url TEXT,
  raw_payload JSONB,
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

## 🧪 Testing Plan

- Unit Testing: `pytest`, `pytest-asyncio`
- HTTP Testing: `httpx`
- Background Jobs: Use APScheduler mocks
- Integration tests: `pytest` + `docker-compose`

---

## ⚙️ CI/CD and Deployment

- GitHub Actions pipeline: lint, test, build
- Docker-based deployment to:
  - AWS Lightsail instance (Ubuntu + Docker preinstalled)
- PostgreSQL via Amazon RDS (Free Tier)
- Environment variables via `.env` for local and AWS Parameter Store for production
- PostHog hosted or self-managed on Lightsail (optional)

---

## 📘 Dev Onboarding

- Single repo
- `.env.example` and Dockerfile
- Local Dev: docker compose setup
- Use Stripe CLI for local webhook testing

---
