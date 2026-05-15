from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Data file for persistence
DATA_FILE = 'data.json'

def load_data():
    """Load data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'students': []}

def save_data(data):
    """Save data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def calculate_grade(marks):
    """Calculate letter grade based on marks"""
    if marks >= 70:
        return 'A'
    elif marks >= 60:
        return 'B'
    elif marks >= 50:
        return 'C'
    elif marks >= 40:
        return 'D'
    else:
        return 'F'

def calculate_gpa_points(marks):
    """Calculate GPA points based on marks"""
    if marks >= 70:
        return 4.0
    elif marks >= 60:
        return 3.0
    elif marks >= 50:
        return 2.0
    elif marks >= 40:
        return 1.0
    else:
        return 0.0

def calculate_student_gpa(units):
    """Calculate average GPA from units"""
    if not units:
        return 0.0
    total_points = sum(unit.get('gpa_points', 0) for unit in units)
    return round(total_points / len(units), 2)

@app.route('/')
def dashboard():
    """Dashboard page"""
    data = load_data()
    students = data['students']
    
    stats = {
        'total_students': len(students),
        'class_average_gpa': 0,
        'pass_rate': 0,
        'grade_distribution': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    }
    
    if students:
        gpas = [s.get('gpa', 0) for s in students if s.get('units')]
        stats['class_average_gpa'] = round(sum(gpas) / len(gpas), 2) if gpas else 0
        
        total_grades = 0
        passed = 0
        for student in students:
            for unit in student.get('units', []):
                grade = unit.get('grade', 'F')
                stats['grade_distribution'][grade] += 1
                total_grades += 1
                if grade in ['A', 'B', 'C', 'D']:
                    passed += 1
        
        stats['pass_rate'] = round((passed / total_grades * 100), 1) if total_grades > 0 else 0
    
    return render_template('dashboard.html', stats=stats)

@app.route('/students')
def students():
    """Students page"""
    data = load_data()
    return render_template('students.html', students=data['students'])

@app.route('/grades')
def grades():
    """Grades page"""
    data = load_data()
    return render_template('grades.html', students=data['students'])

@app.route('/reports')
def reports():
    """Reports page"""
    data = load_data()
    return render_template('reports.html', students=data['students'])

@app.route('/api/students', methods=['GET', 'POST'])
def api_students():
    """API endpoint for students"""
    data = load_data()
    
    if request.method == 'GET':
        return jsonify(data['students'])
    
    elif request.method == 'POST':
        new_student = request.json
        new_student['id'] = str(len(data['students']) + 1)
        new_student['units'] = new_student.get('units', [])
        data['students'].append(new_student)
        save_data(data)
        return jsonify(new_student), 201

@app.route('/api/students/<student_id>', methods=['GET', 'PUT', 'DELETE'])
def api_student(student_id):
    """API endpoint for individual student"""
    data = load_data()
    
    student = next((s for s in data['students'] if s['id'] == student_id), None)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    if request.method == 'GET':
        return jsonify(student)
    
    elif request.method == 'PUT':
        updated = request.json
        student.update(updated)
        save_data(data)
        return jsonify(student)
    
    elif request.method == 'DELETE':
        data['students'].remove(student)
        save_data(data)
        return '', 204

@app.route('/api/students/<student_id>/units', methods=['POST'])
def add_unit(student_id):
    """Add or update unit marks for a student"""
    data = load_data()
    student = next((s for s in data['students'] if s['id'] == student_id), None)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    unit_data = request.json
    marks = unit_data.get('marks', 0)
    
    unit = {
        'name': unit_data.get('name'),
        'marks': marks,
        'grade': calculate_grade(marks),
        'gpa_points': calculate_gpa_points(marks)
    }
    
    # Update or add unit
    existing_unit = next((u for u in student.get('units', []) if u['name'] == unit['name']), None)
    if existing_unit:
        existing_unit.update(unit)
    else:
        if 'units' not in student:
            student['units'] = []
        student['units'].append(unit)
    
    # Recalculate GPA
    student['gpa'] = calculate_student_gpa(student.get('units', []))
    
    save_data(data)
    return jsonify(student)

@app.route('/api/init-sample-data', methods=['POST'])
def init_sample_data():
    """Initialize with sample data"""
    sample_data = {
        'students': [
            {
                'id': '1',
                'name': 'Alice Johnson',
                'registration_number': 'STU001',
                'units': [
                    {'name': 'Mathematics', 'marks': 85, 'grade': 'A', 'gpa_points': 4.0},
                    {'name': 'Physics', 'marks': 78, 'grade': 'A', 'gpa_points': 4.0},
                    {'name': 'Chemistry', 'marks': 92, 'grade': 'A', 'gpa_points': 4.0},
                    {'name': 'Biology', 'marks': 88, 'grade': 'A', 'gpa_points': 4.0}
                ],
                'gpa': 4.0
            },
            {
                'id': '2',
                'name': 'Bob Smith',
                'registration_number': 'STU002',
                'units': [
                    {'name': 'Mathematics', 'marks': 72, 'grade': 'A', 'gpa_points': 4.0},
                    {'name': 'Physics', 'marks': 65, 'grade': 'B', 'gpa_points': 3.0},
                    {'name': 'Chemistry', 'marks': 68, 'grade': 'B', 'gpa_points': 3.0},
                    {'name': 'Biology', 'marks': 74, 'grade': 'A', 'gpa_points': 4.0}
                ],
                'gpa': 3.5
            },
            {
                'id': '3',
                'name': 'Carol Davis',
                'registration_number': 'STU003',
                'units': [
                    {'name': 'Mathematics', 'marks': 58, 'grade': 'C', 'gpa_points': 2.0},
                    {'name': 'Physics', 'marks': 62, 'grade': 'B', 'gpa_points': 3.0},
                    {'name': 'Chemistry', 'marks': 55, 'grade': 'C', 'gpa_points': 2.0},
                    {'name': 'Biology', 'marks': 60, 'grade': 'B', 'gpa_points': 3.0}
                ],
                'gpa': 2.5
            },
            {
                'id': '4',
                'name': 'David Wilson',
                'registration_number': 'STU004',
                'units': [
                    {'name': 'Mathematics', 'marks': 45, 'grade': 'D', 'gpa_points': 1.0},
                    {'name': 'Physics', 'marks': 52, 'grade': 'C', 'gpa_points': 2.0},
                    {'name': 'Chemistry', 'marks': 48, 'grade': 'D', 'gpa_points': 1.0},
                    {'name': 'Biology', 'marks': 50, 'grade': 'C', 'gpa_points': 2.0}
                ],
                'gpa': 1.5
            },
            {
                'id': '5',
                'name': 'Eve Martinez',
                'registration_number': 'STU005',
                'units': [
                    {'name': 'Mathematics', 'marks': 90, 'grade': 'A', 'gpa_points': 4.0},
                    {'name': 'Physics', 'marks': 84, 'grade': 'A', 'gpa_points': 4.0},
                    {'name': 'Chemistry', 'marks': 87, 'grade': 'A', 'gpa_points': 4.0},
                    {'name': 'Biology', 'marks': 95, 'grade': 'A', 'gpa_points': 4.0}
                ],
                'gpa': 4.0
            }
        ]
    }
    save_data(sample_data)
    return jsonify({'message': 'Sample data loaded'}), 200

if __name__ == '__main__':
    # Initialize with sample data if no data file exists
    if not os.path.exists(DATA_FILE):
        sample_data = {
            'students': [
                {
                    'id': '1',
                    'name': 'Alice Johnson',
                    'registration_number': 'STU001',
                    'units': [
                        {'name': 'Mathematics', 'marks': 85, 'grade': 'A', 'gpa_points': 4.0},
                        {'name': 'Physics', 'marks': 78, 'grade': 'A', 'gpa_points': 4.0},
                        {'name': 'Chemistry', 'marks': 92, 'grade': 'A', 'gpa_points': 4.0},
                        {'name': 'Biology', 'marks': 88, 'grade': 'A', 'gpa_points': 4.0}
                    ],
                    'gpa': 4.0
                },
                {
                    'id': '2',
                    'name': 'Bob Smith',
                    'registration_number': 'STU002',
                    'units': [
                        {'name': 'Mathematics', 'marks': 72, 'grade': 'A', 'gpa_points': 4.0},
                        {'name': 'Physics', 'marks': 65, 'grade': 'B', 'gpa_points': 3.0},
                        {'name': 'Chemistry', 'marks': 68, 'grade': 'B', 'gpa_points': 3.0},
                        {'name': 'Biology', 'marks': 74, 'grade': 'A', 'gpa_points': 4.0}
                    ],
                    'gpa': 3.5
                },
                {
                    'id': '3',
                    'name': 'Carol Davis',
                    'registration_number': 'STU003',
                    'units': [
                        {'name': 'Mathematics', 'marks': 58, 'grade': 'C', 'gpa_points': 2.0},
                        {'name': 'Physics', 'marks': 62, 'grade': 'B', 'gpa_points': 3.0},
                        {'name': 'Chemistry', 'marks': 55, 'grade': 'C', 'gpa_points': 2.0},
                        {'name': 'Biology', 'marks': 60, 'grade': 'B', 'gpa_points': 3.0}
                    ],
                    'gpa': 2.5
                },
                {
                    'id': '4',
                    'name': 'David Wilson',
                    'registration_number': 'STU004',
                    'units': [
                        {'name': 'Mathematics', 'marks': 45, 'grade': 'D', 'gpa_points': 1.0},
                        {'name': 'Physics', 'marks': 52, 'grade': 'C', 'gpa_points': 2.0},
                        {'name': 'Chemistry', 'marks': 48, 'grade': 'D', 'gpa_points': 1.0},
                        {'name': 'Biology', 'marks': 50, 'grade': 'C', 'gpa_points': 2.0}
                    ],
                    'gpa': 1.5
                },
                {
                    'id': '5',
                    'name': 'Eve Martinez',
                    'registration_number': 'STU005',
                    'units': [
                        {'name': 'Mathematics', 'marks': 90, 'grade': 'A', 'gpa_points': 4.0},
                        {'name': 'Physics', 'marks': 84, 'grade': 'A', 'gpa_points': 4.0},
                        {'name': 'Chemistry', 'marks': 87, 'grade': 'A', 'gpa_points': 4.0},
                        {'name': 'Biology', 'marks': 95, 'grade': 'A', 'gpa_points': 4.0}
                    ],
                    'gpa': 4.0
                }
            ]
        }
        save_data(sample_data)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
