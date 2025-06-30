import os
import google.generativeai as genai
from db_config import get_db_connection
from tabulate import tabulate

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_schema_representation():
    try:
        with open('DDL.sql', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "ERRO: Arquivo DDL.sql não encontrado."

def ask_ai():
    global conn
    schema = get_schema_representation()
    if "ERRO" in schema:
        print(schema)
        return

    natural_query = input("\nFaça uma pergunta sobre os dados (Ex: 'quantos alunos existem?'): ")

    prompt = f"""
    Baseado no seguinte schema de banco de dados PostgreSQL:
    ---
    {schema}
    ---
    Traduza a seguinte pergunta em linguagem natural para uma única consulta SQL válida para PostgreSQL.
    Responda APENAS com o código SQL e nada mais. Não use markdown (```sql).

    Pergunta: "{natural_query}"
    """

    try:
        print("Gerando consulta SQL com IA...")
        model = genai.get_generative_model('gemini-pro')
        response = model.generate_content(prompt)
        sql_query = response.text.strip()
        print(f"SQL Gerado: {sql_query}")

        conn = get_db_connection()
        if not conn: return

        with conn.cursor() as cur:
            cur.execute(sql_query)
            if cur.description:
                data = cur.fetchall()
                headers = [desc[0] for desc in cur.description]
                print("\n--- Resultado da Consulta da IA ---")
                print(tabulate(data, headers=headers, tablefmt="grid"))
            else:
                print("Comando executado, mas não retornou dados (ex: UPDATE, INSERT).")
        conn.commit()

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()