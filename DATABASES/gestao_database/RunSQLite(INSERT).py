# insert_data.py

import sqlite3

DATABASE = 'DATABASES/0000_banco_dados.db'

def insert_items_data(data):
    """
    Insere os dados na tabela 'items' do banco de dados.
    """
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.executemany('''
            INSERT INTO items (vig, matricula, nome, obs, local, data_encontrado)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', data)
        conn.commit()

if __name__ == '__main__':
    data_to_insert = [
        ('vig', 'matricula', 'xxx', 'obs', 'local', '2023-04-19'),
        ('vig', 'matricula', 'nome', 'obs', 'local', '2023-04-25'),
        ('vig', 'matricula', 'nome', 'obs', 'local', '2023-04-12'),
        ('vig', 'matricula', 'nome', 'obs', 'local', '2023-04-29'),
        ('vig', 'matricula', 'nome', 'obs', 'local', '2023-04-29'),
        ('vig', 'matricula', 'nome', 'obs', 'local', '2023-04-30'),
        ('vig', 'matricula', 'nome', 'obs', 'local', '2023-04-29'),
        ('vig', 'matricula', 'nome', 'obs', 'local', '2023-04-29'),
        ('vig', 'matricula', 'nome', 'obs', 'local', '2023-04-29'),
        ('vig', 'matricula', 'nome', 'obs', 'local', '2023-04-29'),
        ('vig', 'matricula', 'nome', 'obs', 'local', '2023-04-29'),
        ('vig', 'matricula', 'nome', 'obs', 'local', '2023-04-29'),
        ('vig', 'matricula', 'nome', 'obs', 'local', '2023-04-29'),
        ('vig', 'matricula', 'nome', 'obs', 'local', '2023-04-29')
    ]

    insert_items_data(data_to_insert)
