from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS


from PyPDF2 import PdfReader
# import docx
from dotenv import load_dotenv
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.embeddings.huggingface import HuggingFaceEmbeddings
# from langchain.vectorstores import FAISS
# from langchain.chains import ConversationalRetrievalChain
# from langchain.memory import ConversationBufferMemory
# from langchain.chat_models import ChatOpenAI
# from langchain.callbacks import get_openai_callback

app = Flask(__name__)
CORS(app)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your-secret-key'

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'admin' or 'user'

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', backref=db.backref('files', lazy=True))

def create_database():
    """Create the database and tables."""
    db.create_all()
    # Create an admin user for testing
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password=generate_password_hash('admin123'), role='admin')
        db.session.add(admin)
        db.session.commit()

    if not User.query.filter_by(username='user1').first():
        user1 = User(username='user1', password=generate_password_hash('user123'), role='user')
        db.session.add(user1)
        db.session.commit()

    if not User.query.filter_by(username='user2').first():
        user2 = User(username='user2', password=generate_password_hash('user123'), role='user')
        db.session.add(user2)
        db.session.commit()
        
    print("Database and admin user created!")

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return jsonify({'message': 'Logged in'})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))
        return jsonify({'message': 'File uploaded'})
    else:
        return jsonify({'message': 'Invalid file'}), 400

@app.route('/retreive/<filename>', methods=['GET'])
def get_file(filename):
    try:
        return send_from_directory('uploads', filename)
    except FileNotFoundError:
        return jsonify({'message': 'File not found'}), 404

@app.route('/files', methods=['GET'])
def get_files():
    files = os.listdir('uploads')
    return jsonify({'files': files})

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# @app.route('/process', methods=['POST'])
# def process_files():
#     uploaded_files = request.files.getlist("file")
#     files_text = get_files_text(uploaded_files)
#     text_chunks = get_text_chunks(files_text)
#     vetorestore = get_vectorstore(text_chunks)
#     conversation = get_conversation_chain(vetorestore, openai_api_key)
#     return jsonify({"status": "success", "message": "Files processed successfully"}), 200

# @app.route('/chat', methods=['POST'])
# def chat():
#     user_question = request.json.get('question')
#     response = handle_userinput(user_question)
#     return jsonify({"response": response}), 200

# def get_files_text(uploaded_files):
#     text = ""
#     for uploaded_file in uploaded_files:
#         split_tup = os.path.splitext(uploaded_file.filename)
#         file_extension = split_tup[1]
#         if file_extension == ".pdf":
#             text += get_pdf_text(uploaded_file)
#         elif file_extension == ".docx":
#             text += get_docx_text(uploaded_file)
#         else:
#             text += get_csv_text(uploaded_file)
#     return text

# def get_pdf_text(pdf):
#     pdf_reader = PdfReader(pdf)
#     text = ""
#     for page in pdf_reader.pages:
#         text += page.extract_text()
#     return text

# def get_docx_text(file):
#     doc = docx.Document(file)
#     allText = []
#     for docpara in doc.paragraphs:
#         allText.append(docpara.text)
#     text = ' '.join(allText)
#     return text

# def get_csv_text(file):
#     return "a"

# def get_text_chunks(text):
#     text_splitter = CharacterTextSplitter(
#         separator="\n",
#         chunk_size=900,
#         chunk_overlap=100,
#         length_function=len
#     )
#     chunks = text_splitter.split_text(text)
#     return chunks

# def get_vectorstore(text_chunks):
#     embeddings = HuggingFaceEmbeddings()
#     knowledge_base = FAISS.from_texts(text_chunks,embeddings)
#     return knowledge_base

# def get_conversation_chain(vetorestore,openai_api_key):
#     llm = ChatOpenAI(openai_api_key=openai_api_key, model_name = 'gpt-4-turbo',temperature=0)
#     memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
#     conversation_chain = ConversationalRetrievalChain.from_llm(
#         llm=llm,
#         retriever=vetorestore.as_retriever(),
#         memory=memory
#     )
#     return conversation_chain

# def handle_userinput(user_question):
#     with get_openai_callback() as cb:
#         response = conversation({'question':user_question})
#     chat_history = response['chat_history']
#     return chat_history

if __name__ == '__main__':
    with app.app_context():
        create_database()
    app.run(debug=True)