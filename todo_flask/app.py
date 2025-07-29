from flask import Flask, render_template, request, redirect, url_for, flash

# Iniciando o Flask
app = Flask(__name__)

# Rota Principal
@app.route("/")
def index():
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)
