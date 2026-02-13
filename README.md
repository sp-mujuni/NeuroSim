# NeuroSim - Hospital Records Management System

A comprehensive hospital records management system built for **Namulundu Hospital** to efficiently manage patient records, medical books, billing, and data exports with intelligent search capabilities.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4.47-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Backup System](#backup-system)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## Features

### Core Features

- **Patient Management**: Add, search, and manage patient records with detailed medical information
- **Book/File Management**: Organize patient records by book numbers with contact information and billing
- **Billing System**: Track consultation fees and cumulative book balances
- **Search Functionality**: Search patients by name or book number with reinforcement-based ranking
- **Authentication**: Secure session-based login system

### Data Export

- **CSV Export**: Export all patient records to CSV format
- **PDF Export**: Generate professional PDF reports with hospital branding

### Intelligent Features

- **Similarity Scoring**: TF-IDF based similarity search using scikit-learn
- **Reinforcement Learning**: Memory reinforcement engine that improves search relevance over time

### Backup & Cloud

- **Automated Backups**: Daily backup generation in CSV and PDF formats
- **Google Drive Integration**: Automatic upload of backups to Google Drive

---

## Tech Stack

| Component             | Technology                               |
| --------------------- | ---------------------------------------- |
| **Backend**           | Python 3.10, Flask 2.3.3                 |
| **Database**          | SQLAlchemy ORM (SQLite/PostgreSQL)       |
| **Frontend**          | HTML5, Bootstrap 5.3, Jinja2 Templates   |
| **ML/Search**         | scikit-learn (TF-IDF, Cosine Similarity) |
| **PDF Generation**    | ReportLab                                |
| **Cloud Backup**      | PyDrive (Google Drive API)               |
| **Production Server** | Gunicorn                                 |

---

## Project Structure

```
NeuroSim/
├── app.py                    # Main Flask application
├── auth.py                   # Authentication blueprint
├── backup.py                 # Automated backup system with Google Drive
├── requirements.txt          # Python dependencies
├── Procfile                  # Heroku deployment configuration
├── runtime.txt               # Python version specification
│
├── db/
│   └── orm.py                # SQLAlchemy ORM models and database operations
│
├── engine/
│   ├── memory_engine.py      # Core memory/record management engine
│   ├── similarity.py         # TF-IDF similarity scoring
│   └── reinforcement.py      # Reinforcement learning for search ranking
│
├── utils/
│   ├── csv_export.py         # CSV export functionality
│   └── pdf_export.py         # PDF report generation
│
├── templates/
│   ├── index.html            # Home page/dashboard
│   ├── login.html            # Login page
│   ├── patients.html         # Patient data entry form
│   ├── books.html            # Books listing and management
│   ├── search.html           # Patient search results
│   └── edit_bill.html        # Bill editing interface
│
├── backups/                  # Local backup storage
└── archive/                  # Archived records
```

---

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

### Local Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/sp-mujuni/NeuroSim.git
   cd NeuroSim
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**

   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:5000`

---

## Configuration

### Environment Variables

| Variable       | Description                | Default                  |
| -------------- | -------------------------- | ------------------------ |
| `DATABASE_URL` | Database connection string | `sqlite:///namulundu.db` |
| `SECRET_KEY`   | Flask session secret key   | `your-secret-key`        |

### Database Configuration

The application supports both SQLite (development) and PostgreSQL (production):

```python
# SQLite (default for development)
DATABASE_URL=sqlite:///namulundu.db

# PostgreSQL (production)
DATABASE_URL=postgresql://user:password@host:port/database
```

### Google Drive Backup (Optional)

To enable Google Drive backup:

1. Create a Google Cloud project and enable the Drive API
2. Download OAuth credentials as `client_secrets.json`
3. Create a `settings.yaml` file for PyDrive configuration
4. Run `backup.py` for first-time authentication

---

## Usage

### Default Login Credentials

| Username | Password      |
| -------- | ------------- |
| `admin`  | `neurosim123` |

> ⚠️ **Important**: Change these credentials in production by modifying `auth.py`

### Adding a Patient Record

1. Navigate to **Patients** from the home page
2. Fill in the required fields:
   - **Book Number**: Unique identifier for the patient's record book
   - **Book Contact**: Contact number associated with the book
   - **Patient Name**: Full name of the patient
   - **Condition**: Medical condition or diagnosis
   - **Notes**: Detailed medical notes
   - **Prescription**: Prescribed medications and treatments
   - **Consultation Fee**: Fee for the current visit (UGX)
   - **Doctor**: Attending physician's name
   - **Doctor's Contact**: Physician's contact number
3. Click **Save** to add the record

### Managing Books

1. Navigate to **Books** from the home page
2. View all book records with their current balances
3. Search for specific books using the search bar
4. Click **Update Bill** to modify a book's balance

### Searching Records

1. Navigate to **Search Patients** from the patients page
2. Enter a patient name or book number
3. View matching results with full medical details
4. Print results directly from the browser

### Exporting Data

From the Books page:

- Click **Export All (CSV)** for spreadsheet format
- Click **Export All (PDF)** for printable reports

---

## API Endpoints

| Method | Endpoint          | Description            | Auth Required |
| ------ | ----------------- | ---------------------- | ------------- |
| `GET`  | `/`               | Home dashboard         | ✅            |
| `GET`  | `/login`          | Login page             | ❌            |
| `POST` | `/login`          | Process login          | ❌            |
| `GET`  | `/logout`         | Logout user            | ❌            |
| `GET`  | `/patients`       | Patient entry form     | ✅            |
| `POST` | `/add`            | Add new patient record | ✅            |
| `GET`  | `/books`          | List all books         | ✅            |
| `GET`  | `/bill/<book_id>` | Edit bill form         | ✅            |
| `POST` | `/bill/<book_id>` | Update bill            | ✅            |
| `GET`  | `/search?query=`  | Search patients        | ✅            |
| `GET`  | `/export/all/csv` | Export CSV             | ✅            |
| `GET`  | `/export/all/pdf` | Export PDF             | ✅            |

---

## Database Schema

### MemoryRecord Table

| Column           | Type        | Description                            |
| ---------------- | ----------- | -------------------------------------- |
| `id`             | String (PK) | Unique UUID identifier                 |
| `book_id`        | String      | Book/file number                       |
| `name`           | String      | Patient name                           |
| `condition`      | String      | Medical condition                      |
| `content`        | Text        | Full medical notes, prescription, fees |
| `book_balance`   | Float       | Cumulative balance (default: 0.0)      |
| `book_contact`   | String      | Contact number for the book            |
| `doctor`         | String      | Attending doctor's name                |
| `doctor_contact` | String      | Doctor's contact number                |
| `timestamp`      | DateTime    | Record creation/update timestamp       |

---

## Backup System

The backup system (`backup.py`) provides:

### Automatic Backup Features

- Daily CSV and PDF backup generation
- Timestamped filenames: `backup_records_YYYY-MM-DD.csv/pdf`
- Automatic Google Drive upload to "Namulundu" folder

### Running Manual Backup

```bash
python backup.py
```

### Scheduling Automated Backups

**Windows (Task Scheduler)**:

```cmd
schtasks /create /tn "NamulunduBackup" /tr "python C:\path\to\backup.py" /sc daily /st 23:00
```

**Linux/macOS (Cron)**:

```bash
# Add to crontab (crontab -e)
0 23 * * * /path/to/venv/bin/python /path/to/backup.py
```

---

## Deployment

### Heroku Deployment

The application is configured for Heroku deployment:

1. **Procfile**: Configured to use Gunicorn

   ```
   web: gunicorn app:app
   ```

2. **Runtime**: Python 3.10.13

   ```
   python-3.10.13
   ```

3. **Deploy to Heroku**:
   ```bash
   heroku create namulundu-hospital
   heroku addons:create heroku-postgresql:mini
   git push heroku main
   ```

### Environment Variables for Production

Set these in your production environment:

```bash
DATABASE_URL=postgresql://...
SECRET_KEY=<secure-random-key>
```

---

## Engine Components

### Memory Engine (`engine/memory_engine.py`)

Core engine for CRUD operations on patient records with in-memory caching and database persistence.

### Similarity Scorer (`engine/similarity.py`)

Uses TF-IDF vectorization and cosine similarity to find the most relevant patient records based on search queries. Returns top 5 matching results.

### Reinforcement Engine (`engine/reinforcement.py`)

Implements a reinforcement learning mechanism that increases the "strength" of frequently accessed records, improving search relevance over time.

```python
# Learning formula
new_strength = old_strength + learning_rate * (1.0 - old_strength)
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Support

For support, please contact the development team or open an issue on GitHub.

**Namulundu Hospital** - _"Comprehensive Care for All"_

---

_Built with ❤️ for healthcare management_
