import os
from flask import Flask # importa o Flask para poder ser inicializado
from controllers import VitrineController, UserController
from database import db  #importa o database que esta importando o sql

app = Flask(__name__)
app.config['SECRET_KEY'] = '05c31152d33d28330bfd6cdfb5ee36e2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db.init_app(app)   #para inicializar o app com esse banco de dados que esta no database

@app.route('/')   #esses returns abaixo vem do user controllers.py um é o VitrineController e o outro UserController
def index():
  return VitrineController.index()

@app.route('/login')
def login():
  return UserController.login()

@app.route('/signin', methods=['POST'])
def signin():
  return UserController.signin()

@app.route('/register')
def register():
  return UserController.register()
  
@app.route('/signup', methods=['POST'])
def signup():
  return UserController.signup()

@app.route('/logout')
def logout():
  return UserController.logout()

@app.route('/create', methods=['POST'])
def create():
  return VitrineController.create()

@app.route('/delete/<int:id>')
def delete(id):
  return VitrineController.delete(id)

@app.route('/complete/<int:id>')
def complete(id):
  return VitrineController.complete(id)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    return VitrineController.update(id)

with app.app_context():  #para esperar o app ser inicializado, 
  db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)