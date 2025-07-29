from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Iniciando o Flask
app = Flask(__name__)

# Configuração do banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SECRET_KEY"] = "minha_chave_secreta"

db = SQLAlchemy(app)

# Modelo do banco de dados
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.Boolean, default=False)

# Criar as tabelas no banco
with app.app_context():
    db.create_all()

# Rota Principal
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["GET", "POST"])
def add_task():
    return render_template("add_task.html")

if __name__=="__main__":
    app.run(debug=True)
