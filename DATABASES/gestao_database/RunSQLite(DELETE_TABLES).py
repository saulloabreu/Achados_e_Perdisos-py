# delete_tables.py

import sqlite3

DATABASE = 'DATABASES/0000_banco_dados.db'

def drop_items_table():
    """
    Apaga a tabela 'items' do banco de dados se ela existir.
    """
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS items')
        conn.commit()

def drop_completed_items_table():
    """
    Apaga a tabela 'items_baixados' do banco de dados se ela existir.
    """
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS items_baixados')
        conn.commit()

if __name__ == '__main__':
    drop_items_table()
    drop_completed_items_table()

