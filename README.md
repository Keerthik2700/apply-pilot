# ApplyPilot — AI-Assisted Job Application Tracker (FastAPI + Postgres)

A production-style full-stack web app to track job applications, manage resume versions, and run AI-lite resume-to-JD matching.

## Features
- JWT auth (secure cookie)
- Job application CRUD
- Resume storage + versioning
- AI-lite matching (TF-IDF + cosine similarity)
- Analytics dashboard
- Docker + Alembic migrations
- Pytest + GitHub Actions CI

## Tech Stack
FastAPI, Jinja2, HTMX, PostgreSQL, SQLAlchemy 2.0, Alembic, Pytest, Docker

## Run locally (Docker)
1) Create `.env` from template:
```bash
cp .env.example .env
