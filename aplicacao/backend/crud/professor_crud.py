import os
import psycopg
from backend.db_config import get_db_connection

def create_professor(nome_completo, email, senha_hash, siape, sala=None):
    conn = get_db_connection()
    if not conn:
        print("Erro: Não foi possível conectar ao banco de dados.")
        return None

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO cpe_enc.usuario (nome_completo, email, senha_hash)
                VALUES (%s, %s, %s)
                RETURNING id_usuario;
                """,
                (nome_completo, email, senha_hash)
            )
            id_usuario = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO cpe_enc.professor (id_usuario, siape, sala)
                VALUES (%s, %s, %s);
                """,
                (id_usuario, siape, sala)
            )
            conn.commit()
            print(f"Professor '{nome_completo}' (ID: {id_usuario}) criado com sucesso.")
            return id_usuario
    except psycopg.errors.UniqueViolation as e:
        conn.rollback()
        print(f"Erro: Email ou SIAPE já existem. Detalhes: {e}")
        return None
    except Exception as e:
        conn.rollback()
        print(f"Erro ao criar professor: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_professor_by_id(id_usuario):
    conn = get_db_connection()
    if not conn:
        print("Erro: Não foi possível conectar ao banco de dados.")
        return None

    try:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(
                """
                SELECT u.id_usuario, u.nome_completo, u.email, p.siape, p.sala
                FROM cpe_enc.usuario AS u
                JOIN cpe_enc.professor AS p ON u.id_usuario = p.id_usuario
                WHERE u.id_usuario = %s;
                """,
                (id_usuario,)
            )
            professor = cur.fetchone()
            return professor
    except Exception as e:
        print(f"Erro ao buscar professor por ID: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_all_professores():
    conn = get_db_connection()
    if not conn:
        print("Erro: Não foi possível conectar ao banco de dados.")
        return []

    try:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(
                """
                SELECT u.id_usuario, u.nome_completo, u.email, p.siape, p.sala
                FROM cpe_enc.usuario AS u
                JOIN cpe_enc.professor AS p ON u.id_usuario = p.id_usuario
                ORDER BY u.nome_completo;
                """
            )
            professores = cur.fetchall()
            return professores
    except Exception as e:
        print(f"Erro ao buscar todos os professores: {e}")
        return []
    finally:
        if conn:
            conn.close()

def update_professor(id_usuario, nome_completo=None, email=None, senha_hash=None, siape=None, sala=None):
    conn = get_db_connection()
    if not conn:
        print("Erro: Não foi possível conectar ao banco de dados.")
        return False

    try:
        with conn.cursor() as cur:
            user_updates = []
            user_params = []
            if nome_completo is not None:
                user_updates.append("nome_completo = %s")
                user_params.append(nome_completo)
            if email is not None:
                user_updates.append("email = %s")
                user_params.append(email)
            if senha_hash is not None:
                user_updates.append("senha_hash = %s")
                user_params.append(senha_hash)

            if user_updates:
                user_params.append(id_usuario)
                cur.execute(
                    f"UPDATE cpe_enc.usuario SET {', '.join(user_updates)} WHERE id_usuario = %s;",
                    user_params
                )

            prof_updates = []
            prof_params = []
            if siape is not None:
                prof_updates.append("siape = %s")
                prof_params.append(siape)
            if sala is not None:
                prof_updates.append("sala = %s")
                prof_params.append(sala)

            if prof_updates:
                prof_params.append(id_usuario)
                cur.execute(
                    f"UPDATE cpe_enc.professor SET {', '.join(prof_updates)} WHERE id_usuario = %s;",
                    prof_params
                )

            conn.commit()
            print(f"Professor (ID: {id_usuario}) atualizado com sucesso.")
            return True
    except psycopg.errors.UniqueViolation as e:
        conn.rollback()
        print(f"Erro: Email ou SIAPE já existem. Detalhes: {e}")
        return False
    except Exception as e:
        conn.rollback()
        print(f"Erro ao atualizar professor: {e}")
        return False
    finally:
        if conn:
            conn.close()

def delete_professor(id_usuario):
    conn = get_db_connection()
    if not conn:
        print("Erro: Não foi possível conectar ao banco de dados.")
        return False

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT COUNT(*) FROM cpe_enc.projeto
                WHERE id_professor_orientador = %s;
                """,
                (id_usuario,)
            )
            num_projetos = cur.fetchone()[0]

            if num_projetos > 0:
                print(f"Erro: Professor (ID: {id_usuario}) não pode ser excluído. "
                      f"Ele está orientando {num_projetos} projeto(s). "
                      "Reatribua ou exclua os projetos primeiro.")
                return False

            cur.execute(
                """
                DELETE FROM cpe_enc.usuario
                WHERE id_usuario = %s;
                """,
                (id_usuario,)
            )
            conn.commit()
            if cur.rowcount > 0:
                print(f"Professor (ID: {id_usuario}) excluído com sucesso.")
                return True
            else:
                print(f"Professor (ID: {id_usuario}) não encontrado.")
                return False
    except Exception as e:
        conn.rollback()
        print(f"Erro ao deletar professor: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("--- Testando CRUD de Professores ---")
    print("\n--- Criando um novo professor ---")
    new_prof_id = create_professor(
        "Prof. Teste", "teste.prof@ufsc.br", "senha_hash_teste", "100001", "D404"
    )
    if new_prof_id:
        print(f"Novo professor criado com ID: {new_prof_id}")
    else:
        print("Falha ao criar professor.")

    print("\n--- Listando todos os professores ---")
    professores = get_all_professores()
    if professores:
        for prof in professores:
            print(f"ID: {prof['id_usuario']}, Nome: {prof['nome_completo']}, "
                  f"Email: {prof['email']}, SIAPE: {prof['siape']}, Sala: {prof['sala']}")
    else:
        print("Nenhum professor encontrado.")

    if new_prof_id:
        print(f"\n--- Buscando professor com ID {new_prof_id} ---")
        prof_found = get_professor_by_id(new_prof_id)
        if prof_found:
            print(f"Encontrado: {prof_found['nome_completo']}, SIAPE: {prof_found['siape']}")
        else:
            print("Professor não encontrado.")

    if new_prof_id:
        print(f"\n--- Atualizando professor com ID {new_prof_id} ---")
        update_success = update_professor(
            new_prof_id,
            nome_completo="Prof. Teste Atualizado",
            sala="D405"
        )
        if update_success:
            prof_updated = get_professor_by_id(new_prof_id)
            print(f"Atualizado para: {prof_updated['nome_completo']}, Sala: {prof_updated['sala']}")
        else:
            print("Falha ao atualizar professor.")

    if new_prof_id:
        print(f"\n--- Tentando excluir professor com ID {new_prof_id} ---")
        delete_success = delete_professor(new_prof_id)
        if delete_success:
            print("Professor excluído com sucesso.")
        else:
            print("Falha ao excluir professor ou professor não encontrado/com projetos associados.")

    print("\n--- Tentando excluir Prof. Dr. Carlos Silva (ID 1) ---")
    delete_professor(1)