from db_config import get_db_connection
import os

def execute_sql_from_file(filepath):
    if not os.path.exists(filepath):
        print(f"Arquivo '{filepath}' não encontrado.")
        return

    conn = get_db_connection()
    if not conn:
        print("Erro: não foi possível conectar ao banco de dados.")
        return

    try:
        with conn.cursor() as cur, open(filepath, 'r', encoding='utf-8') as f:
            sql_script = f.read().strip()

            if not sql_script:
                print(f"O arquivo '{filepath}' está vazio.")
                return

            cur.execute(sql_script)
        conn.commit()
        print(f"Script '{filepath}' executado com sucesso.")
    except Exception as e:
        print(f" Erro ao executar o script '{filepath}': {e}")
        conn.rollback()
    finally:
        conn.close()

def create_tables():
    print("Tentando criar tabelas...")
    execute_sql_from_file('DDL.sql')

def seed_data():
    print("Tentando popular o banco de dados...")
    execute_sql_from_file('seed.sql')

def drop_all_tables():
    print("ATENÇÃO: Esta ação irá apagar todos os dados permanentemente.")
    confirm = input("Digite 'CONFIRMAR' para continuar: ")

    if confirm != 'CONFIRMAR':
        print("Operação cancelada.")
        return

    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("DROP SCHEMA IF EXISTS cpe_enc CASCADE;")
            conn.commit()
            print("Todas as tabelas foram apagadas com sucesso.")
        except Exception as e:
            print(f"Erro ao apagar as tabelas: {e}")
            conn.rollback()
        finally:
            conn.close()