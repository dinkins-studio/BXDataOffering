from flask import Flask, request, jsonify, render_template, url_for
import random
import os

app = Flask(__name__)

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
    "How does Bronx government contribute to your success?",
    "How does Bronx government contribute to your stress?",
    "How does Bronx environment contribute to your success?",
    "How does Bronx environment contribute to your stress?",
    "How does Bronx spirit contribute to your success?",
    "What's on your mind?", 
    ]

spanish_questions = [
    "¿Cuál es tu recuerdo favorito?",
    "Sube una foto que te inspire.",
    "Graba un audio diciendo hola.",
    "¿Cuál es tu libro favorito?",
    "Describe tu día perfecto.",
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/bronxbot')
def bronxbot():
    return render_template('bronxbot.html')

@app.route('/bronxbotsp')
def bronxbotsp():
    return render_template('bronxbotsp.html')

@app.route('/api/question', methods=['GET'])
def get_question():
    language = request.args.get('lang', 'en')
    if language == 'es':
        question = random.choice(spanish_questions)
    else:
        question = random.choice(english_questions)
    return jsonify({"question": question})

@app.route('/api/answer', methods=['POST'])
def submit_answer():
    answer = request.form.get('answer')
    file = request.files.get('file')
    file_type = request.form.get('file_type')

    if file:
        if file_type == 'text':
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'text', file.filename)
        elif file_type == 'video':
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'video', file.filename)
        elif file_type == 'audio':
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'audio', file.filename)
        elif file_type == 'image':
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'image', file.filename)
        else:
            return jsonify({'message': 'Invalid file type'}), 400

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        file.save(save_path)

    return jsonify({'message': 'Answer submitted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
