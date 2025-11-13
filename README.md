# Team 5 Inventory Asset Tracker

**Course:** EECE-4081-002 Software Engineering Fall Term 2025  
**Team Members:** Matthew J., Carlin W., Rohith R.  
**Assignment:** Sprint Results - MVP Implementation

## Project Overview

Django-based Inventory Asset Management System tracking physical and digital assets with role-based access control, audit logging, and support ticketing.

## Test Results

✅ **All 27 unit tests passing!**

- Epic 1: Asset Lifecycle (6 tests) - Matthew J.
- Epic 2: User Permissions (4 tests) - Carlin W.
- Epic 3: Search & Reporting (5 tests) - Rohith R.
- Epic 4: Support Ticketing (4 tests) - Matthew J.
- Epic 5: Audit Logging (4 tests) - Carlin W.
- Epic 6: Data Onboarding (4 tests) - Rohith R.

## Setup Instructions

1. Create virtual environment: `py -m venv .venv`
2. Activate: `.venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `py manage.py migrate`
5. Run tests: `py manage.py test`
6. Run server: `py manage.py runserver`

## Technology Stack

- Django 5.2.6
- Python 3.13.5
- SQLite3 database