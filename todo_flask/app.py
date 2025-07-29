from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired

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

# Criar classe do formulario
class TaksForm(FlaskForm):
    title = StringField("Titulo", validators=[DataRequired()])
    description = TextAreaField("Descrição")
    status = BooleanField("Concluido")
    submit = SubmitField("Salvar")

# Rota Principal
@app.route("/")
def index():

    # Busca de tarefas
    search_query = request.args.get('search', '').strip()

    if search_query:
        tasks = Todo.query.filter(Todo.title.ilike(f"%{search_query}%")).all()
    else:
        tasks = Todo.query.all()

    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["GET", "POST"])
def add_task():
    form = TaksForm()

    if form.validate_on_submit():
        new_task = Todo(title=form.title.data, description=form.description.data, status=form.status.data)
        db.session.add(new_task)
        db.session.commit()
        # Flash message de sucesso
        flash("Tarefa criada com sucesso", "success")
        return redirect(url_for("index"))

    return render_template("add_task.html", form=form)

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = Todo.query.get_or_404(task_id)
    form = TaksForm(obj=task)

    return render_template("edit_task.html", form=form, task=task)

# Rota para excluir tarefas
@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    task = Todo.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Tarefa removida com sucesso!", "danger")
    return redirect(url_for("index"))

# Rota para alterar o status da tarefa
@app.route("/toggle_status/<int:task_id>", methods=["POST"])
def toggle_status(task_id):
    task = Todo.query.get_or_404(task_id)
    task.status = not task.status
    db.session.commit()
    flash(f"Tarefa '{task.title}' atualizada!", 'success')
    return redirect(url_for('index'))

if __name__=="__main__":
    app.run(debug=True)
