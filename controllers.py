from flask import render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash #verifcar se o passoword enviado é o mesmo que esta armazenado. 
from models import Vitrine, User, db
class VitrineController():# no controler é preciso colocar o nome da class para quando for importar para saber de o todo é model ou controller
  def index(): # mostra itens do danco de dados
    if 'user_id' not in session:
      return redirect('/login')
    user_id = session['user_id']  
    vitrine = Vitrine.query.filter_by(user_id=user_id).all()
    return render_template('index.html', vitrine=vitrine)  

  def create(): # cria itens no banco de dados

    if 'user_id' not in session:
      return redirect('/login')
    user_id = session['user_id']

    title = request.form.get('title')
    price = request.form.get('price')
    novo_produto = Vitrine(title=title, price=price, user_id=user_id)
    db.session.add(novo_produto)
    db.session.commit()
    return redirect('/')

  def delete(id): # deleta itens do banco de dados
    if 'user_id' not in session:
      return redirect('/login')
    produto = Vitrine.query.filter_by(id=id).first()
    db.session.delete(produto)
    db.session.commit()
    return redirect('/')

  def complete(id): # nova funcionalidade no banco de dados
    if 'user_id' not in session:
      return redirect('/login')
    vitrine = Vitrine.query.filter_by(id=id).first()
    vitrine.complete = True
    db.session.commit()
    return redirect('/')

  def update(id): # Edita itens no banco de dados
      title = request.form.get('title')
      price = request.form.get('price')
      produto = Vitrine.query.filter_by(id=id).first()
      produto.title = title
      produto.price = price
      db.session.commit()
      return redirect('/')

class UserController():
  def login():
    return render_template('login.html')

  def signin():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if not user:
      return redirect('/login')
    if not check_password_hash(user.password, password):
      return redirect('/login')
    session['user_id'] = user.id
    return redirect('/')

  def register():
    return render_template('register.html')

  def signup(): #rota para autenticar os usuarios
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if user:
      return redirect('/register')
    new_user = User(
      name=name,
      email=email,
      password=generate_password_hash(password, method='sha256')
    )
    db.session.add(new_user)
    db.session.commit()
    return redirect('/login')

  def logout():
    if 'user_id' in session:
      session.pop('user_id', None)
    return redirect('/login')