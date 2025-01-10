from flask import Flask, request, jsonify, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import random

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bronxbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create a directory for uploads if it doesn't exist
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define the questions lists
english_questions = [
    "If someone wants to understand what matters most to your community, where should they look?",
    "What should BronxBot know about you & your community?",
    "How does living in the Bronx influence the way you see the world?",
    "What should BronxBot talk about?",
    "What does your neighborhood stand for?",
    "What does your community add to Bronx culture?",
    "How is culture passed down in your family?",
    "Rep your family BX style.",
    "Upload an image of pride", 
    "How does Bronx government contribute to your success?",
    "How does Bronx government contribute to your stress?",
    "How does Bronx environment contribute to your success?",
    # Add more questions as needed
]

spanish_questions = [
    "Si alguien quiere entender lo que más importa a tu comunidad, ¿dónde debería mirar?",
    "¿Qué debería saber BronxBot sobre ti y tu comunidad?",
    "¿Cómo influye vivir en el Bronx en la forma en que ves el mundo?",
    "¿De qué debería hablar BronxBot?",
    "¿Qué representa tu vecindario?",
    "¿Qué aporta tu comunidad a la cultura del Bronx?",
    "¿Cómo se transmite la cultura en tu familia?",
    "Representa a tu familia al estilo BX.",
    "Sube una imagen de orgullo",
    "¿Cómo contribuye el gobierno del Bronx a tu éxito?",
    "¿Cómo contribuye el gobierno del Bronx a tu estrés?",
    "¿Cómo contribuye el entorno del Bronx a tu éxito?",
    # Add more questions as needed
]

# Define the Answer model
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(500), nullable=False)

# Define the FileMetadata model
class FileMetadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    filetype = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bronxbot')
def bronxbot():
    return render_template('bronxbot.html')

@app.route('/bronxbotsp')
def bronxbotsp():
    return render_template('bronxbotsp.html')

@app.route('/api/question', methods=['GET'])
def get_question():
    question = random.choice(english_questions)
    return jsonify({"question": question})

@app.route('/api/questionsp', methods=['GET'])
def get_question_sp():
    question = random.choice(spanish_questions)
    return jsonify({"question": question})

@app.route('/submit-answer', methods=['POST'])
def submit_answer_route():
    data = request.json
    answer_text = data.get('answer')
    if not answer_text:
        return jsonify({"error": "No answer provided"}), 400
    answer = Answer(answer=answer_text)
    db.session.add(answer)
    db.session.commit()
    return jsonify({"message": "Answer submitted successfully"})

@app.route('/upload', methods=['POST'])
def upload_file_route():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    file_metadata = FileMetadata(filename=file.filename, filetype=file.mimetype)
    db.session.add(file_metadata)
    db.session.commit()
    return jsonify({"message": "File uploaded successfully"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)