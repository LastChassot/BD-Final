import os
import google.generativeai as genai
from backend.db_config import get_db_connection
import psycopg

# Configure a API do Gemini
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
except TypeError:
    print("\nERRO: Chave da API do Gemini não configurada.")
    print("Verifique se sua variável de ambiente 'GEMINI_API_KEY' está correta.")
    exit()


def _ask_gemini(prompt):
    """Função genérica para enviar um prompt para a IA e retornar a resposta."""
    print("\n🤖 Pensando... A IA está gerando sugestões criativas...")
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Ocorreu um erro ao contatar a IA: {e}"


def _get_interests_by_user(user_id, user_type):
    """Busca as áreas de interesse de um aluno ou professor com base em seus projetos."""
    if user_type == 'aluno':
        query = """
                SELECT DISTINCT ai.nome_area
                FROM cpe_enc.aluno_projeto ap
                         JOIN cpe_enc.projeto_area pa ON ap.id_projeto = pa.id_projeto
                         JOIN cpe_enc.area_de_interesse ai ON pa.id_area = ai.id_area
                WHERE ap.id_aluno = %s; \
                """
    elif user_type == 'professor':
        query = """
                SELECT DISTINCT ai.nome_area
                FROM cpe_enc.projeto p
                         JOIN cpe_enc.projeto_area pa ON p.id_projeto = pa.id_projeto
                         JOIN cpe_enc.area_de_interesse ai ON pa.id_area = ai.id_area
                WHERE p.id_professor_orientador = %s; \
                """
    else:
        return []

    conn = get_db_connection()
    if not conn: return []

    interests = []
    try:
        with conn.cursor() as cur:
            cur.execute(query, (user_id,))
            results = cur.fetchall()
            interests = [row[0] for row in results]
    except psycopg.Error as e:
        print(f"Erro de banco de dados ao buscar interesses: {e}")
    finally:
        if conn: conn.close()

    return interests


def suggest_projects_with_professor():
    """Handler para a Opção 1: Sugerir projeto com um professor específico."""
    aluno_id = input("Qual o seu ID de aluno? ")
    professor_id = input("Qual o ID do professor com quem você gostaria de trabalhar? ")

    print("\nBuscando informações no banco de dados...")
    aluno_interests = _get_interests_by_user(aluno_id, 'aluno')
    prof_interests = _get_interests_by_user(professor_id, 'professor')

    if not aluno_interests:
        print(
            f"Aviso: Não foram encontradas áreas de interesse para o aluno com ID {aluno_id}. A sugestão pode ser menos precisa.")

    if not prof_interests:
        print(
            f"Erro: Não foram encontradas áreas de interesse para o professor com ID {professor_id}. Não é possível continuar.")
        return

    # Combina as listas e remove duplicatas
    combined_interests = list(set(aluno_interests + prof_interests))

    prompt = f"""
    Você é um conselheiro acadêmico especialista em inovação.
    Um aluno e um professor querem desenvolver um projeto juntos.

    Contexto:
    - Áreas de interesse do aluno (inferidas de projetos anteriores): {', '.join(aluno_interests) or 'Nenhuma listada'}
    - Áreas de interesse do professor (inferidas de projetos que orienta): {', '.join(prof_interests)}
    - Interesses combinados: {', '.join(combined_interests)}

    Tarefa:
    Com base neste contexto, sugira 3 ideias de projetos de pesquisa ou desenvolvimento que combinem de forma criativa as áreas de interesse de ambos.
    Para cada ideia, forneça:
    1. Um Título para o projeto.
    2. Uma Descrição curta (2-3 frases) explicando o objetivo do projeto.
    3. As Áreas Combinadas (quais interesses o projeto une).

    Formate a resposta de maneira clara e organizada.
    """

    suggestion = _ask_gemini(prompt)
    print("\n--- 🤖 Sugestões de Projetos ---")
    print(suggestion)


def find_professors_with_similar_interests():
    """Handler para a Opção 2: Encontrar professores com interesses em comum."""
    aluno_id = input("Qual o seu ID de aluno? ")

    print("\nBuscando suas áreas de interesse...")
    aluno_interests = _get_interests_by_user(aluno_id, 'aluno')

    if not aluno_interests:
        print(f"Não foram encontradas áreas de interesse associadas aos seus projetos (ID: {aluno_id}).")
        print("Tente participar de algum projeto para que possamos identificar seus interesses!")
        return

    print(f"Seus interesses são: {', '.join(aluno_interests)}")

    prompt = f"""
    Você é um assistente de pesquisa inteligente para uma universidade.
    Um aluno precisa de ajuda para encontrar um orientador e ter ideias de projetos.

    Contexto:
    - As áreas de interesse do aluno, com base nos projetos que ele já participou, são: {', '.join(aluno_interests)}.

    Tarefa:
    1. Descreva o perfil de 2 ou 3 tipos de professores ideais para este aluno, com base nos interesses dele.
    2. Para cada perfil de professor, sugira 2 ideias de projetos inovadores que o aluno poderia desenvolver com ele.
    3. As ideias de projeto devem ser diretamente relacionadas aos interesses do aluno.

    Seja criativo e prático nas suas sugestões. Formate a resposta de forma clara.
    """

    suggestion = _ask_gemini(prompt)
    print("\n--- 🤖 Professores e Projetos Recomendados ---")
    print(suggestion)


def menu_ai_assistant():
    while True:
        print("\n--- Assistente de Projetos com IA ---")
        print("Qual sua necessidade hoje?")
        print("1 - Quero desenvolver um projeto com um professor específico.")
        print("2 - Quero descobrir professores com meus interesses e ter ideias de projetos.")
        print("3 - Sair")

        choice = input("Escolha uma opção: ")

        if choice == '1':
            suggest_projects_with_professor()
        elif choice == '2':
            find_professors_with_similar_interests()
        elif choice == '3':
            print("Até logo!")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")


if __name__ == '__main__':
    menu_ai_assistant()