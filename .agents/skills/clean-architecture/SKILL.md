---
name: clean-architecture
description: "Monorepo and project structure organization, codebase cleanup, separation of concerns, and server deployment readiness for full-stack Next.js and Django applications."
---

# Clean Architecture & Project Structure Guide

## 1. Overview & Core Philosophy

This skill governs the directory organization, codebase hygiene, architectural layering, and server deployment readiness for full-stack web applications (Next.js frontend + Django backend + PostgreSQL).

### Core Goals
1. **Zero Clutter:** No temporary test scripts, unorganized documentation, or exploratory prototypes mixed into production code.
2. **Clear Boundaries:** Explicit separation between Presentation (Frontend), Business/Domain Logic (Backend API), Shared Types, and Infrastructure (Deploy/Docker).
3. **Server-Ready Packaging:** Code is structured so deployment scripts and container builds can bundle production assets without carrying development bloat, secret files, or heavy local caches.

---

## 2. Standard Production Project Layout

For a full-stack platform like Pezeshkan, maintain the following directory layout:

```text
├── apps/
│   ├── web/                     # Frontend Application (Next.js 16+, React 19, Tailwind)
│   │   ├── app/                 # Next.js App Router (pages, layouts, routes)
│   │   ├── components/          # Reusable UI & Vital components
│   │   │   ├── ui/              # Primitive design system components (buttons, modals, inputs)
│   │   │   └── vital/           # Healthcare signature components (VitalDial, ECG, StatusBeacon)
│   │   ├── lib/                 # Utility functions, API clients, state stores
│   │   ├── public/              # Static public assets (SVGs, icons, favicons)
│   │   ├── package.json
│   │   └── Dockerfile.prod      # Multi-stage standalone Next.js production build
│   │
│   └── api/                     # Backend Application (Django 5+, DRF, PostgreSQL)
│       ├── config/              # Django project settings (base, dev, prod)
│       ├── apps/                # Pluggable Django domain apps
│       │   ├── accounts/        # Authentication, doctors, staff, RBAC
│       │   ├── appointments/    # Booking engine, queue management, CRM
│       │   ├── clinical/        # EMR, prescriptions, lab results, PHI
│       │   └── telemetry/       # Vital signs, ECG data streams
│       ├── manage.py
│       ├── requirements.txt
│       └── Dockerfile.prod      # Lightweight Python slim + Gunicorn build
│
├── deploy/                      # Server Deployment & DevOps Infrastructure
│   ├── docker-compose.yml       # Local dev orchestration
│   ├── docker-compose.prod.yml  # Production multi-container orchestration
│   ├── nginx/
│   │   ├── default.conf         # Reverse proxy, SSL termination, gzip/brotli, security headers
│   │   └── mime.types
│   └── scripts/
│       ├── deploy.sh            # One-click zero-downtime deploy script
│       └── migrate.sh           # Safe production database migration script
│
├── docs/                        # Architecture decisions (ADRs), API schemas, specs
├── data/                        # Static design charters, brand assets, initial fixtures
├── .gitignore                   # Ignore node_modules, __pycache__, .env, .next, dist
└── .dockerignore                # Prevent copying local git history, docs, and caches into images
```

---

## 3. Server Deployment Readiness Rules

### A. Environment Configuration Hygiene
- **Rule 1:** NEVER commit `.env` or `.env.production` files containing live database passwords, secret keys, or API tokens to version control.
- **Rule 2:** Provide `.env.example` in each application directory documenting all required environment variables with non-sensitive placeholder values.
- **Rule 3:** The application must validate required environment variables on startup and fail fast if critical configs are missing.

### B. Docker Build Hygiene & Multi-Stage Builds
When preparing files for server deployment:
1. Use **multi-stage Docker builds** so build-time tools (compilers, npm packages, python build wheels) are discarded in the final runtime container image.
2. In the Next.js `next.config.js`, configure `output: 'standalone'` to create a self-contained node bundle without requiring all development dependencies on the server.
3. In Django, always run under a non-root system user (`appuser`) with Gunicorn/Uvicorn workers.

### C. Exclusion & Cleanup Discipline
Ensure `.dockerignore` contains:
```text
.git
.agents
node_modules
__pycache__
*.pyc
.next
dist
docs
data/*.docx
data/*.odt
tests
.coverage
```

---

## 4. Pre-Deployment Cleanup Workflow

Before triggering a production build or pushing code to the live server:
1. **Remove Artifacts:** Clean any temporary scratch scripts, debug print statements, or mock JSON files.
2. **Verify Dependencies:** Ensure all packages in `package.json` and `requirements.txt` are pinned to exact or compatible versions.
3. **Static File Collection:** Verify Django `collectstatic` runs smoothly and static assets are correctly served or synced with cloud storage.
4. **Health Check:** Ensure both `/health` (or `/api/health/`) endpoints return HTTP 200 with operational status.
