# profjeto_crud.py
import os
import psycopg
from db_config import get_db_connection
from tabulate import tabulate # Para exibir resultados de forma tabular

def create_projeto(titulo, descricao, dt_inicio, dt_fim_prevista, status, id_professor_orientador):
    """
    Cria um novo projeto no sistema.
    dt_inicio e dt_fim_prevista devem ser strings no formato 'YYYY-MM-DD'.
    status deve ser um dos valores permitidos ('Proposto', 'Em Andamento', 'Concluido', 'Cancelado').
    """
    conn = get_db_connection()
    if not conn:
        print("Erro: Não foi possível conectar ao banco de dados.")
        return None

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO cpe_enc.projeto (titulo, descricao, dt_inicio, dt_fim_prevista, status, id_professor_orientador)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_projeto;
                """,
                (titulo, descricao, dt_inicio, dt_fim_prevista, status, id_professor_orientador)
            )
            id_projeto = cur.fetchone()[0]
            conn.commit()
            print(f"Projeto '{titulo}' (ID: {id_projeto}) criado com sucesso.")
            return id_projeto
    except psycopg.errors.ForeignKeyViolation as e:
        conn.rollback()
        print(f"Erro: O professor orientador com ID {id_professor_orientador} não existe. Detalhes: {e}")
        return None
    except psycopg.errors.CheckViolation as e:
        conn.rollback()
        print(f"Erro de validação: Verifique o status ou as datas do projeto. Detalhes: {e}")
        return None
    except Exception as e:
        conn.rollback()
        print(f"Erro ao criar projeto: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_projeto_by_id(id_projeto):
    """
    Busca os detalhes de um projeto pelo seu ID.
    """
    conn = get_db_connection()
    if not conn:
        print("Erro: Não foi possível conectar ao banco de dados.")
        return None

    try:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(
                """
                SELECT p.id_projeto, p.titulo, p.descricao, p.dt_inicio, p.dt_fim_prevista, p.status,
                       u.nome_completo AS professor_orientador
                FROM cpe_enc.projeto AS p
                JOIN cpe_enc.professor AS prof ON p.id_professor_orientador = prof.id_usuario
                JOIN cpe_enc.usuario AS u ON prof.id_usuario = u.id_usuario
                WHERE p.id_projeto = %s;
                """,
                (id_projeto,)
            )
            projeto = cur.fetchone()
            return projeto
    except Exception as e:
        print(f"Erro ao buscar projeto por ID: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_all_projetos():
    """
    Retorna uma lista com todos os projetos cadastrados no sistema.
    """
    conn = get_db_connection()
    if not conn:
        print("Erro: Não foi possível conectar ao banco de dados.")
        return []

    try:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(
                """
                SELECT p.id_projeto, p.titulo, p.descricao, p.dt_inicio, p.dt_fim_prevista, p.status,
                       u.nome_completo AS professor_orientador
                FROM cpe_enc.projeto AS p
                JOIN cpe_enc.professor AS prof ON p.id_professor_orientador = prof.id_usuario
                JOIN cpe_enc.usuario AS u ON prof.id_usuario = u.id_usuario
                ORDER BY p.titulo;
                """
            )
            projetos = cur.fetchall()
            return projetos
    except Exception as e:
        print(f"Erro ao buscar todos os projetos: {e}")
        return []
    finally:
        if conn:
            conn.close()

def update_projeto(id_projeto, titulo=None, descricao=None, dt_inicio=None, dt_fim_prevista=None, status=None, id_professor_orientador=None):
    """
    Atualiza os dados de um projeto.
    Campos não fornecidos (None) não serão atualizados.
    """
    conn = get_db_connection()
    if not conn:
        print("Erro: Não foi possível conectar ao banco de dados.")
        return False

    try:
        with conn.cursor() as cur:
            updates = []
            params = []

            if titulo is not None:
                updates.append("titulo = %s")
                params.append(titulo)
            if descricao is not None:
                updates.append("descricao = %s")
                params.append(descricao)
            if dt_inicio is not None:
                updates.append("dt_inicio = %s")
                params.append(dt_inicio)
            if dt_fim_prevista is not None:
                updates.append("dt_fim_prevista = %s")
                params.append(dt_fim_prevista)
            if status is not None:
                updates.append("status = %s")
                params.append(status)
            if id_professor_orientador is not None:
                updates.append("id_professor_orientador = %s")
                params.append(id_professor_orientador)

            if not updates:
                print("Nenhum campo para atualizar foi fornecido.")
                return False

            params.append(id_projeto)
            cur.execute(
                f"UPDATE cpe_enc.projeto SET {', '.join(updates)} WHERE id_projeto = %s;",
                params
            )
            conn.commit()
            if cur.rowcount > 0:
                print(f"Projeto (ID: {id_projeto}) atualizado com sucesso.")
                return True
            else:
                print(f"Projeto (ID: {id_projeto}) não encontrado.")
                return False
    except psycopg.errors.ForeignKeyViolation as e:
        conn.rollback()
        print(f"Erro: O novo professor orientador com ID {id_professor_orientador} não existe. Detalhes: {e}")
        return False
    except psycopg.errors.CheckViolation as e:
        conn.rollback()
        print(f"Erro de validação: Verifique o status ou as datas do projeto. Detalhes: {e}")
        return False
    except Exception as e:
        conn.rollback()
        print(f"Erro ao atualizar projeto: {e}")
        return False
    finally:
        if conn:
            conn.close()

def delete_projeto(id_projeto):
    """
    Deleta um projeto do sistema.
    ATENÇÃO: A exclusão de um projeto pode cascatear para tabelas como
    'projeto_area', 'aluno_projeto', 'vaga', 'marco_calendario', 'publicacao'
    devido ao ON DELETE CASCADE definido no DDL.
    """
    conn = get_db_connection()
    if not conn:
        print("Erro: Não foi possível conectar ao banco de dados.")
        return False

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM cpe_enc.projeto
                WHERE id_projeto = %s;
                """,
                (id_projeto,)
            )
            conn.commit()
            if cur.rowcount > 0:
                print(f"Projeto (ID: {id_projeto}) excluído com sucesso.")
                return True
            else:
                print(f"Projeto (ID: {id_projeto}) não encontrado.")
                return False
    except Exception as e:
        conn.rollback()
        print(f"Erro ao deletar projeto: {e}")
        return False
    finally:
        if conn:
            conn.close()

def get_projetos_by_professor(id_professor):
    """
    Retorna uma lista de projetos orientados por um professor específico.
    """
    conn = get_db_connection()
    if not conn:
        print("Erro: Não foi possível conectar ao banco de dados.")
        return []

    try:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(
                """
                SELECT p.id_projeto, p.titulo, p.descricao, p.dt_inicio, p.dt_fim_prevista, p.status
                FROM cpe_enc.projeto AS p
                WHERE p.id_professor_orientador = %s
                ORDER BY p.titulo;
                """,
                (id_professor,)
            )
            projetos = cur.fetchall()
            return projetos
    except Exception as e:
        print(f"Erro ao buscar projetos por professor: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_professor_projetos_summary():
    """
    Retorna um resumo de professores e o número de projetos que cada um orienta.
    """
    conn = get_db_connection()
    if not conn:
        print("Erro: Não foi possível conectar ao banco de dados.")
        return []

    try:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(
                """
                SELECT u.nome_completo AS professor, COUNT(p.id_projeto) AS total_projetos
                FROM cpe_enc.usuario AS u
                JOIN cpe_enc.professor AS prof ON u.id_usuario = prof.id_usuario
                LEFT JOIN cpe_enc.projeto AS p ON prof.id_usuario = p.id_professor_orientador
                GROUP BY u.nome_completo
                ORDER BY total_projetos DESC, u.nome_completo;
                """
            )
            summary = cur.fetchall()
            return summary
    except Exception as e:
        print(f"Erro ao buscar resumo de projetos por professor: {e}")
        return []
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # Este bloco é para testar as funções CRUD.
    # Certifique-se de que seu arquivo .env está configurado
    # e o banco de dados está rodando e populado (db_setup.py).

    print("--- Testando CRUD de Projetos ---")

    # Exemplo de Criação
    print("\n--- Criando um novo projeto ---")
    # Usando um professor existente (ex: Prof. Dr. Carlos Silva - ID 1)
    new_proj_id = create_projeto(
        "Novo Projeto de Teste",
        "Descrição detalhada do novo projeto de teste.",
        "2024-07-01",
        "2025-07-01",
        "Proposto",
        1 # ID do Prof. Dr. Carlos Silva
    )
    if new_proj_id:
        print(f"Novo projeto criado com ID: {new_proj_id}")
    else:
        print("Falha ao criar projeto.")


    print("\n--- Listando todos os projetos ---")
    projetos = get_all_projetos()
    if projetos:
        headers = ["ID", "Título", "Status", "Orientador", "Início", "Fim Previsto"]
        data = [[p['id_projeto'], p['titulo'], p['status'], p['professor_orientador'], p['dt_inicio'], p['dt_fim_prevista']] for p in projetos]
        print(tabulate(data, headers=headers, tablefmt="grid"))
    else:
        print("Nenhum projeto encontrado.")

    if new_proj_id:
        print(f"\n--- Buscando projeto com ID {new_proj_id} ---")
        proj_found = get_projeto_by_id(new_proj_id)
        if proj_found:
            print(f"Encontrado: Título: {proj_found['titulo']}, Status: {proj_found['status']}, Orientador: {proj_found['professor_orientador']}")
        else:
            print("Projeto não encontrado.")

    if new_proj_id:
        print(f"\n--- Atualizando projeto com ID {new_proj_id} ---")
        update_success = update_projeto(
            new_proj_id,
            descricao="Descrição atualizada do projeto de teste.",
            status="Em Andamento"
        )
        if update_success:
            proj_updated = get_projeto_by_id(new_proj_id)
            print(f"Atualizado para: Título: {proj_updated['titulo']}, Status: {proj_updated['status']}, Descrição: {proj_updated['descricao']}")
        else:
            print("Falha ao atualizar projeto.")

    print("\n--- Projetos orientados pelo Prof. Dr. Carlos Silva (ID 1) ---")
    carlos_projetos = get_projetos_by_professor(1)
    if carlos_projetos:
        headers = ["ID", "Título", "Status", "Início"]
        data = [[p['id_projeto'], p['titulo'], p['status'], p['dt_inicio']] for p in carlos_projetos]
        print(tabulate(data, headers=headers, tablefmt="grid"))
    else:
        print("Nenhum projeto encontrado para este professor.")

    print("\n--- Resumo de Projetos por Professor ---")
    prof_summary = get_professor_projetos_summary()
    if prof_summary:
        headers = ["Professor", "Total de Projetos"]
        data = [[s['professor'], s['total_projetos']] for s in prof_summary]
        print(tabulate(data, headers=headers, tablefmt="grid"))
    else:
        print("Nenhum resumo de professor encontrado.")

    if new_proj_id:
        print(f"\n--- Excluindo projeto com ID {new_proj_id} ---")
        delete_success = delete_projeto(new_proj_id)
        if delete_success:
            print("Projeto excluído com sucesso.")
        else:
            print("Falha ao excluir projeto ou projeto não encontrado.")

    print("\n--- Tentando criar projeto com professor inexistente (ID 999) ---")
    create_projeto(
        "Projeto Invalido", "Este projeto não deve ser criado.", "2024-01-01", "2024-12-31", "Proposto", 999
    )