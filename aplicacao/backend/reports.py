import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from db_config import get_db_connection

OUTPUT_DIR = "imagens"

def gerar_grafico_consulta1(conn):
    print("Executando Consulta 1: Popularidade das Áreas...")

    sql = """
        SELECT ai.nome_area,
               COUNT(DISTINCT ap.id_aluno) AS numero_de_alunos_unicos
        FROM cpe_enc.area_de_interesse AS ai
        JOIN cpe_enc.projeto_area AS pa ON ai.id_area = pa.id_area
        JOIN cpe_enc.aluno_projeto AS ap ON pa.id_projeto = ap.id_projeto
        GROUP BY ai.nome_area
        ORDER BY numero_de_alunos_unicos DESC;
    """
    df = pd.read_sql(sql, conn)

    plt.figure(figsize=(10, 6))
    sns.barplot(x='nome_area', y='numero_de_alunos_unicos', data=df, palette='Blues_d')
    plt.title('Popularidade das Áreas por Engajamento de Alunos')
    plt.xlabel('Área de Interesse')
    plt.ylabel('Número de Alunos Únicos')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    path = os.path.join(OUTPUT_DIR, 'consulta1.png')
    plt.savefig(path)
    plt.close()
    print(f"Gráfico 1 salvo em: {path}\n")


def gerar_grafico_consulta2(conn):
    print("Executando Consulta 2: Ranking de Professores...")

    sql = """
        SELECT u.nome_completo AS nome_professor,
               COUNT(p.id_projeto) AS numero_de_projetos
        FROM cpe_enc.professor AS prof
        JOIN cpe_enc.usuario AS u ON prof.id_usuario = u.id_usuario
        JOIN cpe_enc.projeto AS p ON prof.id_usuario = p.id_professor_orientador
        WHERE p.status IN ('Em Andamento', 'Proposto')
        GROUP BY u.nome_completo
        ORDER BY numero_de_projetos ASC;
    """
    df = pd.read_sql(sql, conn)

    plt.figure(figsize=(10, 6))
    sns.barplot(x='numero_de_projetos', y='nome_professor', data=df, palette='Reds_r')
    plt.title('Ranking de Professores por Volume de Orientação')
    plt.xlabel('Número de Projetos Ativos')
    plt.ylabel('Professor')
    plt.tight_layout()

    path = os.path.join(OUTPUT_DIR, 'consulta2.png')
    plt.savefig(path)
    plt.close()
    print(f"Gráfico 2 salvo em: {path}\n")


def gerar_grafico_consulta3(conn):
    print("Executando Consulta 3: Vagas Abertas por Projeto...")

    sql = """
        SELECT p.titulo AS titulo_projeto,
               u.nome_completo AS professor_orientador,
               SUM(v.numero_posicoes) AS total_de_vagas_abertas
        FROM cpe_enc.vaga AS v
        JOIN cpe_enc.projeto AS p ON v.id_projeto = p.id_projeto
        JOIN cpe_enc.professor AS prof ON p.id_professor_orientador = prof.id_usuario
        JOIN cpe_enc.usuario AS u ON prof.id_usuario = u.id_usuario
        WHERE v.prazo_inscricao > CURRENT_TIMESTAMP
        GROUP BY p.titulo, u.nome_completo
        ORDER BY total_de_vagas_abertas DESC;
    """
    df = pd.read_sql(sql, conn)

    plt.figure(figsize=(10, 10))
    plt.pie(
        df['total_de_vagas_abertas'],
        labels=df['titulo_projeto'],
        autopct='%1.1f%%',
        startangle=140,
        textprops={'fontsize': 10}
    )
    plt.title('Distribuição de Vagas Abertas por Projeto', fontsize=14)
    plt.axis('equal')
    plt.tight_layout()

    path = os.path.join(OUTPUT_DIR, 'consulta3.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"Gráfico 3 salvo em: {path}\n")


def executar_todas():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Pasta '{OUTPUT_DIR}' criada.")

    conn = get_db_connection()
    if conn:
        gerar_grafico_consulta1(conn)
        gerar_grafico_consulta2(conn)
        gerar_grafico_consulta3(conn)
        conn.close()
        print("Conexão com o banco de dados fechada.")
        print("Todos os gráficos foram gerados com sucesso!")
    else:
        print("Não foi possível conectar ao banco.")
