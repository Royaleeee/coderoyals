from flask import Flask, render_template, request, redirect, url_for
import re

app=Flask(__name__)

#1°pagina do site
#route -> royalcodes.com/
#função -> o que irá ixibir na pagina
#template

@app.route('/contatos')
def contatos():
    return render_template('contatos.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/registrar')
def registrar():
    return render_template('registrar.html')

@app.route('/registrar', methods=['POST'])
def processar_registro():
    # Pegar dados do formulário
    nome = request.form.get('nome', '')
    sobrenome = request.form.get('sobrenome', '')
    username = request.form.get('username', '')
    email = request.form.get('email', '')
    telefone = request.form.get('telefone', '')
    senha = request.form.get('senha', '')
    confirmar_senha = request.form.get('confirmar_senha', '')
    
    # Validações
    if not nome or not sobrenome or not username or not email or not telefone or not senha:
        return render_template('registrar.html', erro="Todos os campos são obrigatórios")
    
    if senha != confirmar_senha:
        return render_template('registrar.html', erro="As senhas não coincidem")
    
    # Validação de senha mais rigorosa
    if len(senha) < 8:
        return render_template('registrar.html', erro="Senha deve ter pelo menos 8 caracteres")
    
    if not re.search(r'[A-Z]', senha):
        return render_template('registrar.html', erro="Senha deve conter pelo menos 1 letra maiúscula")
    
    if not re.search(r'[a-z]', senha):
        return render_template('registrar.html', erro="Senha deve conter pelo menos 1 letra minúscula")
    
    if not re.search(r'\d', senha):
        return render_template('registrar.html', erro="Senha deve conter pelo menos 1 número")
    
    if not re.search(r'[!@#$%^&*]', senha):
        return render_template('registrar.html', erro="Senha deve conter pelo menos 1 caractere especial (!@#$%^&*)")
    
    # Validação de email
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return render_template('registrar.html', erro="Email inválido")
    
    # Se chegou até aqui, registro foi bem-sucedido
    nome_completo = f"{nome} {sobrenome}"
    return render_template('registrar.html', sucesso=f"Conta registrada com sucesso! Bem vindo, {nome_completo}")

@app.route('/usuarios')
def usuarios_form():
    username = request.args.get('username', 'Visitante')
    senha = request.args.get('senha', '')
    
    # Validação básica da senha
    if senha:
        if len(senha) < 6:
            return render_template('login.html', erro="Senha deve ter pelo menos 6 caracteres")
        
        if not any(c.isdigit() for c in senha):
            return render_template('login.html', erro="Senha deve conter pelo menos 1 número")
        
        if not any(c.isalpha() for c in senha):
            return render_template('login.html', erro="Senha deve conter pelo menos 1 letra")
    
    return render_template('usuarios.html', nome_usuario=username)

@app.route('/usuarios/<nome_usuario>')
def usuarios(nome_usuario):
    return render_template('usuarios.html', nome_usuario=nome_usuario)

@app.route('/pagina-extra')
def pagina_extra():
    nome = request.args.get('nome', 'Visitante')
    return render_template('pagina_extra.html', nome_usuario=nome)

#colocar site no ar 
if __name__ == '__main__':
    app.run(debug=True)
