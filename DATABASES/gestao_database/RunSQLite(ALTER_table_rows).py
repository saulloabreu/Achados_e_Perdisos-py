import sqlite3

DATABASE = 'DATABASES/0000_banco_dados.db'



def update_items_data(updates):
    """
    Atualiza as linhas da tabela 'items' com os dados fornecidos.
    """
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        for update in updates:
            c.execute('''
                UPDATE items
                SET vig = ?, matricula = ?, nome = ?, obs = ?, local = ?, data_encontrado = ?
                WHERE id = ?
            ''', update)
        conn.commit()

if __name__ == '__main__':
    updates_to_apply = [
        ('teteu', '21210011', 'celular Moto G100', '--', 'Foyer', '2023/07/11', 1)
        
    ]

    update_items_data(updates_to_apply)
