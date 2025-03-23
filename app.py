import os
import json
from datetime import datetime as dt, date
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
import webbrowser
import sys
from plotly.express import *
import plotly_express as px
import pandas as pd




app = Flask(__name__)

app.secret_key = '123456789'
DATABASE = 'DATABASES/0000_banco_dados.db'

def create_items_table():
    """
    Cria a tabela 'items' no banco de dados se ela ainda não existir.
    A tabela 'items' armazena informações sobre os itens encontrados.
    """
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vig TEXT,
                matricula TEXT,
                nome TEXT,
                obs TEXT, 
                local TEXT,
                data_encontrado DATE
            )
        ''')
        conn.commit()

def create_completed_items_table():
    """
    Cria a tabela 'items_baixados' no banco de dados se ela ainda não existir.
    A tabela 'items_baixados' armazena informações sobre os itens completados (baixados).
    """
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS items_baixados (
                id INTEGER PRIMARY KEY,
                vig TEXT,
                matricula TEXT,
                nome TEXT, 
                obs TEXT,
                local TEXT,
                data_encontrado DATE,
                completado_por_nome TEXT,
                completado_por_matric TEXT,
                observacao TEXT, 
                data_da_baixa DATE,
                FOREIGN KEY (id) REFERENCES items (id)
            )
        ''')
        conn.commit()
        

@app.route('/')
def index():
    """
    Rota principal que exibe a página inicial do aplicativo web.
    """
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    """
    Rota para adicionar um novo item encontrado ao sistema.
    Suporta tanto a exibição do formulário para adicionar um novo item (GET)
    quanto o recebimento e salvamento dos dados do formulário no banco de dados (POST).
    """
    if request.method == 'POST':
        # Recebe os dados do formulário para adicionar um novo item
        vig = request.form['vig']
        matricula = request.form['matricula']
        nome = request.form['nome']
        obs = request.form['obs']
        local = request.form['local']
        data_encontrado = dt.strptime(request.form['data_encontrado'], '%Y-%m-%d').date()

        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            # Insere os dados na tabela 'items'
            c.execute('''
                INSERT INTO items (vig, matricula, nome, obs, local, data_encontrado)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (vig, matricula, nome, obs, local, data_encontrado))
            conn.commit()

            item_id = c.lastrowid

        # Retorna um JSON com o ID do item adicionado
        return json.dumps({'id': item_id})
    else:
        # Renderiza o modelo 'add.html' para solicitar os dados do item
        return render_template('add.html')

@app.route('/view', methods=['GET'])
def view_all_items():
    """
    Rota para visualizar todos os itens encontrados no sistema.
    Suporta a pesquisa de itens por palavra-chave e intervalo de datas.
    """
    # Recebe parâmetros de pesquisa (palavra-chave, data inicial e data final)
    palavra_chave = request.args.get('palavra_chave', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        query = '''
            SELECT * FROM items
            WHERE (nome LIKE ? OR id = ?)
        '''
        query_params = (f'%{palavra_chave}%', palavra_chave)

        if start_date and end_date:
            start_date = dt.strptime(start_date, '%Y-%m-%d').date()
            end_date = dt.strptime(end_date, '%Y-%m-%d').date()

            query += " AND (DATE(data_encontrado) BETWEEN ? AND ?) "
            query_params += (start_date, end_date)

        # Executa a consulta e obtém os itens
        c.execute(query, query_params)
        items = c.fetchall()

    numero_itens = len(items)

    # Renderiza o modelo 'view.html' com os itens obtidos
    return render_template('view.html', items=items, numero_itens=numero_itens)

@app.route('/view_completed_items', methods=['GET'])
def view_completed_items():
    """
    Rota para visualizar todos os itens completados (baixados) no sistema.
    Suporta a pesquisa de itens por palavra-chave.
    """
    # Recebe parâmetro de pesquisa (palavra-chave)
    palavra_chave = request.args.get('palavra_chave', '')

    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        query = '''SELECT * FROM items_baixados WHERE (nome LIKE ? OR id = ?)'''
        query_params = (f'%{palavra_chave}%', palavra_chave)

        # Executa a consulta e obtém os itens completados
        c.execute(query, query_params)
        items_baixados = c.fetchall()

    numero_itens_baixados = len(items_baixados)

    # Renderiza o modelo 'view_completed_items.html' com os itens completados obtidos
    return render_template('view_completed_items.html', items_baixados=items_baixados, numero_itens_baixados=numero_itens_baixados)

@app.route('/complete/<int:item_id>', methods=['GET', 'POST'])
def complete_item(item_id):
    """
    Rota para marcar um item como completado (baixado) no sistema.
    Permite tanto a exibição do formulário para completar o item (GET)
    quanto o recebimento e salvamento dos dados do formulário na tabela 'items_baixados' (POST).
    """
    if request.method == 'POST':
        # Recebe os dados do formulário para completar o item
        completado_por_nome = request.form.get('completado_por_nome')
        completado_por_matric = request.form.get('completado_por_matric')
        observacao = request.form.get('observacao')
        data_da_baixa = date.today().strftime('%d/%m/%Y')

        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            # Obtém os detalhes do item a ser completado
            c.execute('SELECT * FROM items WHERE id = ?', (item_id,))
            item = c.fetchone()

            # Insere os dados do item completado na tabela 'items_baixados'
            c.execute('''
                INSERT INTO items_baixados (
                    id, vig, matricula, nome, obs, local,
                    data_encontrado, completado_por_nome, completado_por_matric, observacao, data_da_baixa
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (item[0], item[1], item[2], item[3], item[4], item[5], item[6], completado_por_nome, completado_por_matric, observacao, data_da_baixa))

            # Remove o item da tabela 'items' após ser completado
            c.execute('DELETE FROM items WHERE id = ?', (item_id,))

            conn.commit()

        # Redireciona para a página inicial após completar o item
        return redirect(url_for('index'))
    else:
        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            # Obtém os detalhes do item a ser completado
            c.execute('SELECT * FROM items WHERE id = ?', (item_id,))
            item = c.fetchone()

        # Renderiza o modelo 'complete.html' para preencher detalhes do item completado
        return render_template('complete.html', item=item)

@app.route('/formulario', methods=['GET'])
def formulario():
    """
    Rota para exibir um formulário para preencher detalhes do item completado em formato de PDF.
    """
    item_id = request.args.get('id')
    form_name = f"{item_id}"
    item_descri = request.args.get('nome')
    item_data = dt.strptime(request.args.get('data_encontrado'), '%Y-%m-%d').strftime('%d/%m/%Y')
    data_atual = date.today().strftime('%d/%m/%Y')

    # Renderiza o modelo 'formulario.html' com os dados do item
    return render_template('formulario.html', form_name=form_name, item_id=item_id, item_descri=item_descri, item_data=item_data, data_atual=data_atual)

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Rota para lidar com o upload de arquivos.
    Permite que os usuários façam upload de arquivos e os salva em uma pasta específica.
    """
    if "fileToUpload" in request.files:
        file = request.files["fileToUpload"]
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        upload_folder = os.path.join(base_path, "static/upload")

        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # Salva o arquivo enviado em uma pasta específica
        file.save(os.path.join(upload_folder, file.filename))

        return jsonify({"message": "Upload concluído com sucesso!"}), 200
    else:
        return jsonify({"message": "Nenhum arquivo enviado."}), 400

@app.route('/visualizar_formulario/<int:item_id>')
def visualizar_formulario(item_id):
    """
    Rota para visualizar o formulário preenchido em formato PDF.
    """
    file_path = f'static/upload/formulario{item_id}.pdf'
    # Retorna o formulário preenchido em formato PDF
    return send_from_directory('', file_path)




if __name__ == '__main__':
    # Cria as tabelas no banco de dados
    create_items_table()
    create_completed_items_table()

    def open_browser():
        # Abre o navegador padrão para exibir a aplicação web
        webbrowser.open('http://127.0.0.1:5000')

    # Abrir o navegador padrão antes de iniciar o servidor Flask
    open_browser()

    # Iniciar o servidor Flask
    app.run(host='127.0.0.1', debug=True)