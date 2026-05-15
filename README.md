# Student Grade Management System

A lightweight Python Flask-based web application for managing student grades and academic records.

## Features

- ✅ Add, edit, and delete students
- ✅ Manage course units and marks per student
- ✅ Auto-calculate grades (A-F) based on Kenyan university grading scale
- ✅ Calculate GPA per student
- ✅ Dashboard with statistics and grade distribution chart
- ✅ Search and filter students by name or registration number
- ✅ Generate academic transcripts/reports
- ✅ Clean, responsive UI with navy blue and white theme

## Grading Scale

- **A** = 70–100 (4.0 GPA points)
- **B** = 60–69 (3.0 GPA points)
- **C** = 50–59 (2.0 GPA points)
- **D** = 40–49 (1.0 GPA points)
- **F** = 0–39 (0.0 GPA points)

## Installation

1. **Clone or download the project**

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

The app comes pre-loaded with 5 sample students and their grades.

## Project Structure

```
.
├── app.py                 # Flask application and API routes
├── requirements.txt       # Python dependencies
├── data.json             # Student data storage (auto-generated)
└── templates/
    ├── base.html         # Base template with navigation
    ├── dashboard.html    # Dashboard with stats and charts
    ├── students.html     # Student management
    ├── grades.html       # Grade entry form
    └── reports.html      # Academic transcripts
```

## Pages

### Dashboard
View key statistics:
- Total number of students
- Class average GPA
- Pass rate
- Grade distribution chart

### Students
- View all students in a table
- Search by name or registration number
- Add new students
- Edit student information
- Delete students

### Grades
- Select a student
- Add/edit/delete course units
- Enter marks (0-100)
- Auto-calculated grade and GPA points

### Reports
- Generate academic transcripts
- View student's academic history
- Printable layout

## Data Storage

Student data is stored in `data.json` in the project root. The file is automatically created on first run with sample data.

## Technologies Used

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Tailwind CSS
- **Charts**: Chart.js
- **Data Storage**: JSON file-based

## License

Free to use and modify.
