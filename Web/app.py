DATABASE_FILE = '../data/data.db'
ATTENDANCE_TABLE = 'attendance'
STUDENTS_TABLE = 'student'

import csv, io, datetime, sqlite3, base64
from flask import Flask, request, jsonify, make_response, render_template
import cv2
import numpy as np

from service import Service

print('Launching service...')
service_instance = Service()
service_instance.get_trained_model()
print('Service successfully launched.')

app = Flask(__name__)

# for website

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students')
def form():
    return render_template('marked.html', students = service_instance.class_labels)

# for all API calls

@app.route('/api/students')
def list_students():
    return jsonify(
        [{"name": name} for name in service_instance.class_labels]
    )
    
@app.route('/api/attendance/mark', methods = ['POST'])
def mark_attendance():
    db = sqlite3.connect(DATABASE_FILE)
    cursor = db.cursor()
    sql_query = "INSERT INTO %s VALUES (?, ?)" % ATTENDANCE_TABLE

    content = request.json
    current_time = datetime.datetime.now()
    f_time = '{y}-{m}-{d} {hh}:{mm}:{ss}'.format(
        y = current_time.year,
        m = current_time.month,
        d = current_time.day,
        hh = current_time.hour,
        mm = current_time.minute,
        ss = current_time.second
    )

    try:
        image_bytes = base64.b64decode(content['image'])
        img_array = np.frombuffer(image_bytes, dtype = 'uint8')
        image = cv2.imdecode(img_array, 0)
        present = service_instance.get_face_names(image)
        
        insertion_list = []
        for name in present:
            insertion_list.append(
                (name, f_time)
            )
        cursor.executemany(sql_query, insertion_list)
        db.commit()
        cursor.close()
        db.close()
    except:
        return jsonify({
            "error": "Error occured."
        })
    else:
        return jsonify({
            "students": [{"name": name} for name in present],
            "timestamp": current_time
        })

@app.route('/api/attendance/export.csv')
def export_attendance():
    db = sqlite3.connect(DATABASE_FILE)    
    cursor = db.cursor()
    sql_query = 'SELECT * FROM %s' % ATTENDANCE_TABLE
    cursor.execute(sql_query)
    
    sio = io.StringIO()
    writer = csv.DictWriter(sio, fieldnames=['student', 'time'])
    writer.writeheader()

    for row in cursor:
        writer.writerow({"student": row[0], "time": row[1]})
    cursor.close()
    db.close()

    res = make_response(sio.getvalue())
    res.headers['Content-Type'] = 'application/csv'
    return res

# error pages

@app.errorhandler(404)
def page_not_found(err):
    return jsonify({
        "message": "Resource unavailable.",
        "httpError": 404
    })

@app.errorhandler(405)
def method_not_allowed(err):
    return jsonify({
        "message": "HTTP method not allowed.",
        "httpError": 405
    })

@app.errorhandler(500)
def internal_server_error(err):
    return jsonify({
        "message": "Internal server error.",
        "httpError": 500
    })

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0', debug=True)
