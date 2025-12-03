# Team 5 Inventory Asset Tracker

**Course:** EECE-4081-002 Software Engineering Fall Term 2025  
**Team Members:** Matthew J., Carlin W., Rohith R.  
**Assignment:** Sprint Results - MVP Implementation

---

## Project Overview

Django-based Inventory Asset Management System tracking physical and digital assets with role-based access control, audit logging, and support ticketing.

**Phase 2 Complete:** Fully functional application with connected frontend and backend via REST APIs.

---

## Features

### ✅ Functional Web Application
- Login with role-based access (Admin, Technician, User)
- Add, edit, delete assets through web interface
- Real-time database updates
- Asset status management (In Service / Out for Repair)
- Repair notes and tracking
- "Who Has What" reporting
- Search and filter capabilities

### ✅ Backend API
- RESTful API endpoints for all operations
- Login authentication
- CRUD operations for assets
- User management
- Role-based permissions

### ✅ Admin Interface
- Django admin panel at `/admin/`
- Custom displays for all models
- Bulk operations
- Search and filtering

---

## Technology Stack

- **Backend:** Django 5.2.6
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Database:** SQLite3
- **Python:** 3.13.5

---

## Test Results

✅ **All 27 unit tests passing!**

- **Epic 1:** Asset Lifecycle (6 tests) - Matthew J.
- **Epic 2:** User Permissions (4 tests) - Carlin W.
- **Epic 3:** Search & Reporting (5 tests) - Rohith R.
- **Epic 4:** Support Ticketing (4 tests) - Matthew J.
- **Epic 5:** Audit Logging (4 tests) - Carlin W.
- **Epic 6:** Data Onboarding (4 tests) - Rohith R.

**Run tests:** `python manage.py test`

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/eece-4081-fall-2025/team5-inventory-tracker.git
cd team5-inventory-tracker
```

### 2. Create Virtual Environment
```bash
python -m venv .venv

# Windows:
.venv\Scripts\activate

# Mac/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```
Follow prompts to create admin account.

### 6. Create Demo Users (Optional)
```bash
python manage.py shell
```
Then run:
```python
from django.contrib.auth.models import User
User.objects.get_or_create(id=3, username='johndoe', defaults={'first_name': 'John', 'last_name': 'Doe'})
User.objects.get_or_create(id=4, username='janesmith', defaults={'first_name': 'Jane', 'last_name': 'Smith'})
exit()
```

### 7. Run Development Server
```bash
python manage.py runserver
```

### 8. Access Application
- **Main App:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/

---

## How to Use

### Login Credentials (Demo)
- **Admin:** `admin` / any password
- **Technician:** `tech` / any password  
- **User:** `johndoe` / any password

*Note: Demo authentication accepts any password. Use superuser for admin panel.*

### Adding Assets
1. Login as admin or technician
2. Click **"+ Add Asset"** button
3. Select asset type (Physical or Digital)
4. Fill in required fields
5. Assign to a user
6. Click **"Add Asset"**

### Managing Assets
1. Click **"View Details"** on any asset
2. Admin/Tech can:
   - Mark as "Out for Repair"
   - Return to "In Service"
   - Delete asset
3. Users can only view their assigned assets

### Reports
Click **"Reports"** tab to see "Who Has What" report showing all users and their assigned assets.

---

## API Endpoints

### Authentication
- `POST /api/login/` - User login

### Assets
- `GET /api/assets/` - List all assets
- `POST /api/assets/` - Create new asset
- `PUT /api/assets/<id>/` - Update asset
- `DELETE /api/assets/<id>/` - Delete asset

### Users
- `GET /api/users/` - List users for assignment

---

## Database Models

### Asset
- Tracks physical and digital assets
- Fields: type, manufacturer, model, serial number, status, location, assigned user, etc.
- Status: In Service, Out for Repair, Decommissioned

### UserProfile
- Extends Django User with role field
- Roles: admin, technician, user

### AuditLog
- Immutable audit trail of asset changes
- Tracks: action, timestamp, user, details

### SupportTicket
- Links assets to support tickets
- Status: open, in_progress, resolved, closed

---

## Project Structure
```
team5-inventory-tracker/
├── .venv/                  # Virtual environment (not in repo)
├── assets/                 # Main Django app
│   ├── migrations/         # Database migrations
│   ├── admin.py           # Admin interface configuration
│   ├── models.py          # Database models
│   ├── tests.py           # Unit tests (27 tests)
│   ├── urls.py            # URL routing
│   └── views.py           # API endpoints
├── inventory_project/      # Django project settings
│   ├── settings.py        # Project configuration
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── templates/              # HTML templates
│   └── index.html         # Main application interface
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── PHASE2_CHANGES.md     # Detailed changelog

Contribution Files:
├── MATTHEW_CONTRIBUTION.md
├── CARLIN_CONTRIBUTION.md
└── ROHITH_CONTRIBUTION.md
```

---

## Development History

### Phase 1 (November 12, 2025)
- Created Django project and models
- Implemented 27 comprehensive unit tests
- Set up GitHub with team branches and pull requests
- All tests passing

### Phase 2 (December 3, 2025)
- Fixed professor feedback issues
- Created REST API endpoints
- Connected frontend to backend
- Implemented full CRUD operations
- Added role-based access control
- Enhanced admin interface
- All features fully functional

See `PHASE2_CHANGES.md` for detailed changelog.

---

## Team Contributions

**Matthew J.**
- Epic 1: Asset Lifecycle Management (6 tests)
- Epic 4: Support Ticketing Integration (4 tests)
- API endpoint implementation
- Frontend integration

**Carlin W.**
- Epic 2: User Permissions & Access Control (4 tests)
- Epic 5: Data Integrity & Auditing (4 tests)
- Admin interface configuration
- Database model design

**Rohith R.**
- Epic 3: Search, Reporting & Analytics (5 tests)
- Epic 6: System Setup & Data Onboarding (4 tests)
- Documentation
- URL routing

---

## Assignment Compliance

✅ Working software in GitHub repo  
✅ Multiple pull requests from each member (3 PRs)  
✅ At least 1 test per epic (27 tests total - 450% over requirement)  
✅ Evidence each member wrote tests (clear attribution)  
✅ Fully functional web application  
✅ Role-based access control  
✅ Admin interface for management  

---

## Known Limitations

- Demo authentication (production would use real authentication)
- Basic error handling (would add comprehensive validation)
- No file uploads for asset photos
- No email notifications
- Simple reporting (could add charts/graphs)

These are acceptable for MVP scope and can be enhanced in future sprints.

---

## Future Enhancements

- Real authentication with password hashing
- User registration through web
- File attachments and photos
- Advanced search and filtering
- Export reports to PDF/CSV
- Email notifications
- Barcode/QR code generation
- Mobile responsive design improvements
- Asset depreciation tracking
- Multi-tenancy support

---

## Repository

**GitHub:** https://github.com/eece-4081-fall-2025/team5-inventory-tracker

---

## License

Educational project for EECE-4081 Software Engineering course.

---

**Status:** ✅ Completed - Ready for submission  
**Last Updated:** December 3, 2025