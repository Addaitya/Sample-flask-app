from flask import Flask, jsonify, request, url_for, redirect
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import uuid
import os
from database.create_db import create_database
from database.person import fetch_people, append_person, fetch_person, add_image_name
from werkzeug.middleware.proxy_fix import ProxyFix
from waitress import serve



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd() + os.getenv('image_folder')
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

load_dotenv()

db_path = os.getenv('database_path')
if not os.path.isfile(db_path):
    create_database()


@app.route('/')
def hello():
    return 'The server is working :)'


@app.get('/persons')
def get_people():
    data = fetch_people()
    res = jsonify({"data": data})
    return res

@app.post('/person')
def add_person():
    try:
        data = request.get_json()
        if not data or type(data.get("name")) != str or type(data.get("age")) != int:
            return jsonify("Missing name or age or incorrect datatype"), 400
        
        id_info = append_person(data) # db fucntion
        
        return jsonify(id_info), 201

    except Exception as e:
        print("error in add_person: \n", e)
        return jsonify({"msg": "something went wrong"}), 500


@app.get('/person/<int:person_id>')
def get_person(person_id):
    print("Person id: ", person_id)
    if not person_id:
        return jsonify({"msg": "Incorrect person_id"}), 400

    data = fetch_person(person_id)
    return jsonify({"data": data}), 200


@app.route('/person/<int:person_id>', methods=['PATCH'])
def add_image(person_id):
    if not person_id:
        return jsonify({"msg": "provide person id"}), 400
    
    try:
        if 'file' not in request.files:
            return jsonify({"msg": "Either image file does not exist or is not of right type"}), 400
        
        allowed_types = {'png', 'jpg', 'jpeg', 'pdf'}
        file = request.files['file']

        if file.filename.rsplit('.')[1] not in allowed_types:
            return jsonify({"msg": "The image file is not of right type"}), 400
        
        filename = secure_filename(file.filename)
        unique_filename = uuid.uuid4().hex + filename

        if not add_image_name(person_id, unique_filename):
            return 500

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))

        return jsonify({'id': person_id, 'photo_id': unique_filename})

    except IndexError:
        return jsonify({"msg": 'The image file has no extension'}), 400
    except Exception as e:
        print(f"Error in add_image: \n{e}")
        return 500


@app.get('/photo/<photo_id>')
def get_photo(photo_id):
    if not photo_id:
        return jsonify({"msg": "photo not found"}), 404
    try:
        return redirect(url_for('static', filename=photo_id))

    except Exception as e:
        print(f"Error in get_photo: \n{e}")
        return 404

@app.get('/photo/person/<int:person_id>')
def get_photo_by_person_id(person_id):
    if not person_id:
        return jsonify({"msg": "person id not found"}), 404
    try:
        person = fetch_person(person_id)
        if not person or not person['photo_id']:
            return jsonify({"msg": "Either person_id or photo_id not found"}), 404
        
        return redirect(url_for('get_photo', photo_id=person['photo_id']))
    except Exception as e:
        print(f"Error in get_photo_by_person_id: \n{e}")
        return 500

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000, threads=2)   