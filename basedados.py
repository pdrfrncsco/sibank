import sqlite3

def conectar_banco_dados():
    try:
        conn = sqlite3.connect('sisbank.db')
        return conn
    except sqlite3.Error as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None

def criar_tabelas():
    conn = conectar_banco_dados()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
                            id INTEGER PRIMARY KEY,
                            bi TEXT UNIQUE,
                            nome TEXT,
                            data_nascimento TEXT,
                            endereco TEXT
                            )''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS contas (
                            id INTEGER PRIMARY KEY,
                            numero TEXT UNIQUE,
                            cliente_id INTEGER,
                            saldo REAL,
                            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
                            )''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS transacoes (
                            id INTEGER PRIMARY KEY,
                            tipo TEXT,
                            valor REAL,
                            data TEXT,
                            conta_id INTEGER,
                            FOREIGN KEY (conta_id) REFERENCES contas (id)
                            )''')
            conn.commit()
            print("Tabelas criadas com sucesso!")
        except sqlite3.Error as e:
            print("Erro ao criar tabelas:", e)
        finally:
            conn.close()

def inserir_cliente(bi, nome, data_nascimento, endereco):
    conn = conectar_banco_dados()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO clientes (bi, nome, data_nascimento, endereco) VALUES (?, ?, ?, ?)',
                           (bi, nome, data_nascimento, endereco))
            conn.commit()
            print("Cliente inserido com sucesso!")
        except sqlite3.Error as e:
            print("Erro ao inserir cliente:", e)
        finally:
            conn.close()

def inserir_conta(numero, cliente_id, saldo):
    conn = conectar_banco_dados()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO contas (numero, cliente_id, saldo) VALUES (?, ?, ?)',
                           (numero, cliente_id, saldo))
            conn.commit()
            print("Conta inserida com sucesso!")
        except sqlite3.Error as e:
            print("Erro ao inserir conta:", e)
        finally:
            conn.close()

def main():
    criar_tabelas()

    # Inserir cliente
    inserir_cliente('1234568', 'Pedro Francisco', '2000-02-20', 'Rua 3')

    # Inserir conta
    inserir_conta('123456', 1, 5000)

    # Consultar clientes e contas
    conn = conectar_banco_dados()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM clientes')
            clientes = cursor.fetchall()
            print("Clientes:", clientes)

            cursor.execute('SELECT * FROM contas')
            contas = cursor.fetchall()
            print("Contas:", contas)
        except sqlite3.Error as e:
            print("Erro ao consultar clientes e contas:", e)
        finally:
            conn.close()

if __name__ == "__main__":
    main()
