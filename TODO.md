# Subscope Project TODO

## Sprint 0: Foundation & Setup

- [ ] **Task 0.1 (All):** Initialize GitHub repo, agree on branching strategy.
- [ ] **Task 0.2 (All):** Setup `.env.example` with initial variables.
- [ ] **Task 0.3 (All):** Setup `docker-compose.yml` for local API (stub) + PostgreSQL.
- [ ] **Task 0.4 (Backend):** Initialize FastAPI project, basic structure, health check endpoint.
- [ ] **Task 0.5 (Backend):** Setup Alembic for migrations.
- [ ] **Task 0.6 (Frontend):** Initialize Next.js project, setup Tailwind CSS, shadcn/ui.
- [ ] **Task 0.7 (Frontend):** Create basic app layout component.
- [ ] **Task 0.8 (CI/DevOps):** Setup GitHub Actions for backend linting & basic tests (pytest).
- [ ] **Task 0.9 (CI/DevOps):** Setup GitHub Actions for frontend linting (ESLint).

## Sprint 1: User Registration & Login API

- [ ] **Task 1.1 (Backend):** `users` table migration (email, password_hash, full_name, plan (default 'free'), currency, created_at, updated_at).
- [ ] **Task 1.2 (Backend):** User Pydantic schemas (UserCreate, UserResponse, UserInDB).
- [ ] **Task 1.3 (Backend):** Implement `/auth/register` endpoint (hash password with passlib).
- [ ] **Task 1.4 (Backend):** Implement `/auth/login` endpoint (verify password, issue JWT).
- [ ] **Task 1.5 (Frontend):** Design and implement Registration page UI form.
- [ ] **Task 1.6 (Frontend):** Design and implement Login page UI form.
- [ ] **Task 1.7 (Full-Stack/Testing):** Implement JWT utilities (create_access_token, decode_token).
- [ ] **Task 1.8 (Full-Stack/Testing):** Implement basic auth middleware and a protected `/users/me` endpoint (returns current user).
- [ ] **Task 1.9 (Full-Stack/Testing):** Write unit/integration tests for registration and login APIs (using httpx).

## Sprint 2: Frontend Auth & Welcome Email

- [ ] **Task 2.1 (Backend):** Setup AWS SES integration (boto3 client, config).
- [ ] **Task 2.2 (Backend):** Create welcome email template and sending logic.
- [ ] **Task 2.3 (Backend):** Integrate welcome email sending into `/auth/register` flow (as a background task).
- [ ] **Task 2.4 (Frontend):** Implement API calls from Registration/Login pages to backend.
- [ ] **Task 2.5 (Frontend):** Setup global auth state management (e.g., React Context) for storing JWT and user info.
- [ ] **Task 2.6 (Frontend):** Implement protected route mechanism in Next.js (redirect if not logged in).
- [ ] **Task 2.7 (Frontend):** Implement Logout functionality.
- [ ] **Task 2.8 (Full-Stack/CI):** Configure `.env` for local SES testing (e.g., using MailHog or actual SES sandbox).
- [ ] **Task 2.9 (Full-Stack/CI):** Add `Dockerfile` for the FastAPI application.
- [ ] **Task 2.10 (Full-Stack/CI):** Update GitHub Actions to build the Docker image on push/PR to `develop`.

## Sprint 3: Subscription Backend (Free Tier)

- [ ] **Task 3.1 (Backend):** `subscriptions` table migration (user_id, name, amount, currency, billing_cycle, next_due_date, etc.).
- [ ] **Task 3.2 (Backend):** Subscription Pydantic schemas.
- [ ] **Task 3.3 (Backend):** Implement POST `/subscriptions` endpoint (link to user, enforce max 5 for 'free' plan).
- [ ] **Task 3.4 (Backend):** Implement GET `/subscriptions` (list for user) and GET `/subscriptions/{id}` endpoints.
- [ ] **Task 3.5 (Frontend):** Design basic Dashboard page layout (will show subscriptions).
- [ ] **Task 3.6 (Frontend):** Design UI for "Create Subscription" modal/form.
- [ ] **Task 3.7 (Full-Stack/Testing):** Implement PUT `/subscriptions/{id}` and DELETE `/subscriptions/{id}` endpoints.
- [ ] **Task 3.8 (Full-Stack/Testing):** Write API tests for all subscription CRUD endpoints.
- [ ] **Task 3.9 (Full-Stack/Testing):** Refactor API routes into routers/modules for better organization.

## Sprint 4: Subscription Frontend (Free Tier)

- [ ] **Task 4.1 (Backend):** Refine subscription validation logic (e.g., date formats, amount constraints).
- [ ] **Task 4.2 (Backend):** Ensure user authorization on all subscription endpoints (user can only access their own).
- [ ] **Task 4.3 (Frontend):** Implement API calls from frontend to fetch and display subscriptions on Dashboard.
- [ ] **Task 4.4 (Frontend):** Implement "Create Subscription" form functionality.
- [ ] **Task 4.5 (Frontend):** Implement "Edit Subscription" form functionality.
- [ ] **Task 4.6 (Frontend):** Implement "Delete Subscription" functionality with confirmation.
- [ ] **Task 4.7 (Frontend):** Display subscription count and limit for free users.
- [ ] **Task 4.8 (Full-Stack/DB):** Set up initial AWS RDS PostgreSQL instance (Free Tier).
- [ ] **Task 4.9 (Full-Stack/DB):** Document DB connection strings and access for dev/prod.
- [ ] **Task 4.10 (Full-Stack/DB):** Review database indexing for `users` and `subscriptions` tables.

## Sprint 5: Reminder Backend Logic & Scheduling

- [ ] **Task 5.1 (Backend):** `reminders` table migration (subscription_id, remind_at, is_recurring, sent).
- [ ] **Task 5.2 (Backend):** `notification_logs` table migration (reminder_id, channel, status, message, error, sent_at).
- [ ] **Task 5.3 (Backend):** Pydantic schemas for Reminder and NotificationLog.
- [ ] **Task 5.4 (Backend):** Implement logic to automatically create initial `reminders` when a `subscription` is created/updated (e.g., 7 days before `next_due_date`).
- [ ] **Task 5.5 (Frontend):** (Placeholder/Design) Design how reminders might be subtly indicated on the subscription list or dashboard.
- [ ] **Task 5.6 (Frontend):** Refine subscription forms based on any new fields or user feedback.
- [ ] **Task 5.7 (Full-Stack/Scheduler):** Integrate APScheduler into FastAPI (lifespan event or separate process).
- [ ] **Task 5.8 (Full-Stack/Scheduler):** Create APScheduler job: Periodically scan `reminders` for due items.
- [ ] **Task 5.9 (Full-Stack/Scheduler):** Create APScheduler job: After a subscription's `next_due_date` passes, update it for the next cycle and create new `reminders` if recurring.

## Sprint 6: Reminder Email Sending & Logging

- [ ] **Task 6.1 (Backend):** Implement email composition service for reminder emails (use templates).
- [ ] **Task 6.2 (Backend):** Integrate SES sending into the APScheduler job for due reminders.
- [ ] **Task 6.3 (Backend):** Log every send attempt (success/failure) into `notification_logs`.
- [ ] **Task 6.4 (Frontend):** (Optional UI) If decided, implement UI to show upcoming/sent reminders.
- [ ] **Task 6.5 (Frontend):** General UI polish and bug fixes from previous sprints.
- [ ] **Task 6.6 (Full-Stack/Testing):** Thoroughly test the reminder creation and sending flow. Use mocks for APScheduler and SES in unit tests.
- [ ] **Task 6.7 (Full-Stack/Testing):** Manually test reminder scheduling and email delivery with a few test subscriptions and local email catcher (MailHog).

## Sprint 7: Basic Analytics (Free Tier)

- [ ] **Task 7.1 (Backend):** Design and implement API endpoint `/analytics/summary`.
- [ ] **Task 7.2 (Backend):** Implement logic to calculate total monthly/yearly spending and breakdown by subscription.
- [ ] **Task 7.3 (Frontend):** Create a new "Analytics" page.
- [ ] **Task 7.4 (Frontend):** Implement UI to display basic spending summary (e.g., total monthly/yearly).
- [ ] **Task 7.5 (Frontend):** Integrate a simple charting library (e.g., Chart.js) to show spending breakdown by subscription.
- [ ] **Task 7.6 (Full-Stack/DevOps):** Setup AWS Lightsail instance (Ubuntu + Docker). Configure basic firewall.
- [ ] **Task 7.7 (Full-Stack/DevOps):** Practice manual deployment of the current Docker image to Lightsail. Test connection to RDS.

## Sprint 8: Stripe Setup & Checkout Backend

- [ ] **Task 8.1 (Backend):** `billing_events` table migration.
- [ ] **Task 8.2 (Backend):** Add `stripe_customer_id` (nullable TEXT) and `valid_until` (nullable TIMESTAMP) to `users` table, migrate.
- [ ] **Task 8.3 (Backend):** Integrate Stripe Python library. Configure Stripe API keys in `.env`.
- [ ] **Task 8.4 (Backend):** Implement `/billing/create-checkout-session` endpoint for Pro Plan upgrade. Redirect to Stripe Checkout.
- [ ] **Task 8.5 (Frontend):** Design UI elements for "Upgrade to Pro" (e.g., in navbar, on dashboard if at limit).
- [ ] **Task 8.6 (Frontend):** Implement button/link to call `create-checkout-session` and redirect user to Stripe.
- [ ] **Task 8.7 (Full-Stack/Stripe Admin):** Create Stripe account, set up "Pro Plan" product and price in Stripe Dashboard.
- [ ] **Task 8.8 (Full-Stack/Stripe Admin):** Configure Stripe CLI for local webhook testing.

## Sprint 9: Stripe Webhooks & Plan Management

- [ ] **Task 9.1 (Backend):** Implement `/billing/webhook` endpoint to handle Stripe events.
- [ ] **Task 9.2 (Backend):** Handle `checkout.session.completed`: Create Stripe customer if not exists, store `stripe_customer_id`, update user `plan` to 'pro', set `valid_until`. Log in `billing_events`.
- [ ] **Task 9.3 (Backend):** Handle `invoice.payment_succeeded`: Extend `valid_until`. Log in `billing_events`.
- [ ] **Task 9.4 (Backend):** Handle `customer.subscription.deleted` / `invoice.payment_failed`: If `valid_until` passed, revert `plan` to 'free'. Log in `billing_events`.
- [ ] **Task 9.5 (Frontend):** Display current plan status (`Free`/`Pro`) and `valid_until` if Pro.
- [ ] **Task 9.6 (Frontend):** Implement a "Manage Billing" button that redirects to Stripe Customer Portal (configure in Stripe).
- [ ] **Task 9.7 (Full-Stack/Testing):** Test webhook handling thoroughly using Stripe CLI and mock events.
- [ ] **Task 9.8 (Full-Stack/Testing):** Implement backend middleware to check `user.plan == 'pro'` for premium features (stub for now).

## Sprint 10: Pro Plan Enforcement & UI Polish

- [ ] **Task 10.1 (Backend):** Apply Pro plan middleware to subscription creation (unlimited for Pro).
- [ ] **Task 10.2 (Backend):** (Future-proofing) Consider how other Pro features will be gated.
- [ ] **Task 10.3 (Frontend):** Update subscription creation UI: remove limit display if Pro.
- [ ] **Task 10.4 (Frontend):** Ensure "Upgrade" prompts are hidden for Pro users.
- [ ] **Task 10.5 (Frontend):** General UI/UX review and consistency check for billing flow.
- [ ] **Task 10.6 (Full-Stack/Deployment Prep):** Set up AWS Parameter Store for production secrets.
- [ ] **Task 10.7 (Full-Stack/Deployment Prep):** Refine `Dockerfile` for production (e.g., multi-stage builds, non-root user).

## Sprint 11: Custom Tags (Pro Feature)

- [ ] **Task 11.1 (Backend):** `tags` and `subscription_tags` table migrations. Define UNIQUE constraint for `tags(user_id, name)`.
- [ ] **Task 11.2 (Backend):** Pydantic schemas for Tag.
- [ ] **Task 11.3 (Backend):** CRUD API endpoints for `tags` (user-specific, Pro plan gated).
- [ ] **Task 11.4 (Backend):** API endpoints to associate/disassociate tags with subscriptions (Pro plan gated).
- [ ] **Task 11.5 (Frontend):** UI for managing tags (create, list, delete) - visible only for Pro users.
- [ ] **Task 11.6 (Frontend):** UI on subscription form/details to add/remove tags.
- [ ] **Task 11.7 (Frontend):** Implement filtering subscriptions by tags on the dashboard.
- [ ] **Task 11.8 (Full-Stack/Testing):** Write API tests for tag management and association.
- [ ] **Task 11.9 (Full-Stack/Testing):** Update subscription list endpoint to optionally include/filter by tags.

## Sprint 12: Export & Advanced Analytics (Pro Features)

- [ ] **Task 12.1 (Backend):** API endpoint for CSV export of subscriptions (Pro plan gated).
- [ ] **Task 12.2 (Backend):** API endpoint for PDF export of subscriptions (Pro plan gated, use WeasyPrint or ReportLab).
- [ ] **Task 12.3 (Backend):** API endpoint for advanced analytics (e.g., spending by tag) (Pro plan gated).
- [ ] **Task 12.4 (Frontend):** Add "Export CSV/PDF" buttons on dashboard/analytics page (visible for Pro).
- [ ] **Task 12.5 (Frontend):** Enhance Analytics page with new charts/tables for advanced analytics (e.g., spending by tag).
- [ ] **Task 12.6 (Full-Stack/Monitoring Setup):** Sign up for PostHog (cloud or decide on self-host).
- [ ] **Task 12.7 (Full-Stack/Monitoring Setup):** Integrate PostHog SDK in Next.js for basic page views and user identification.

## Sprint 13: Testing, Monitoring & CI/CD Finalization

- [ ] **Task 13.1 (Backend):** Integrate PostHog SDK in FastAPI for tracking key backend events (e.g., registrations, subscription creations, upgrades).
- [ ] **Task 13.2 (Backend):** Increase unit/integration test coverage, focusing on edge cases and Pro features.
- [ ] **Task 13.3 (Frontend):** Add PostHog event tracking for key frontend interactions (button clicks, form submissions).
- [ ] **Task 13.4 (Frontend):** Final UI/UX review and polish across the application.
- [ ] **Task 13.5 (CI/CD & DevOps):** Finalize GitHub Actions workflow for CI: lint, test, build Docker, push to registry (ECR or Docker Hub).
- [ ] **Task 13.6 (CI/CD & DevOps):** Create GitHub Actions workflow for CD: deploy to Lightsail (e.g., SSH to run `docker pull` and `docker run`, or setup Watchtower on Lightsail).

## Sprint 14: Production Deployment & Go-Live Prep

- [ ] **Task 14.0 (All):** Pre-Go-Live UAT (User Acceptance Testing) with test accounts.
- [ ] **Task 14.1 (Backend):** Final check of all environment variables for production.
- [ ] **Task 14.2 (Backend):** Run Alembic migrations on production RDS.
- [ ] **Task 14.3 (Frontend):** Build production version of Next.js app.
- [ ] **Task 14.4 (Frontend):** Ensure all frontend assets are optimized.
- [ ] **Task 14.5 (DevOps/Full-Stack):** Configure Nginx/Caddy on Lightsail as reverse proxy (SSL with Let's Encrypt, serve static Next.js build, proxy API requests to FastAPI).
- [ ] **Task 14.6 (DevOps/Full-Stack):** Perform full deployment using the CD pipeline.
- [ ] **Task 14.7 (DevOps/Full-Stack):** Final checks (DNS, SSL, application functionality on production).
- [ ] **Task 14.8 (DevOps/Full-Stack):** Create basic README, dev onboarding docs.

## Post-Launch

- [ ] Monitor PostHog for user behavior and errors.
- [ ] Monitor AWS CloudWatch for RDS and Lightsail performance.
- [ ] Collect user feedback.
- [ ] Plan for Sprint 15: Bug fixes, minor improvements, v1.1 features.
