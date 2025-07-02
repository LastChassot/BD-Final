import psycopg
from backend.db_config import get_db_connection
from tabulate import tabulate


def create_aluno(self, nome_completo, email, senha_hash, matricula, semestre):
    """
    Cria um novo aluno no banco de dados usando os dados fornecidos.
    Primeiro insere na tabela 'usuario' e depois na tabela 'aluno'.
    """
    conn = get_db_connection()
    if not conn:
        return

    try:
        # A senha pode ser padronizada aqui se não for passada como argumento
        if not senha_hash:
            senha_hash = "senha_padrao_123"

        with conn.cursor() as cur:
            # Etapa 1: Inserir na tabela 'usuario'
            cur.execute(
                "INSERT INTO cpe_enc.usuario (nome_completo, email, senha_hash) VALUES (%s, %s, %s) RETURNING id_usuario",
                (nome_completo, email, senha_hash)
            )
            # Pega o ID do usuário que acabou de ser criado
            id_usuario = cur.fetchone()[0]

            # Etapa 2: Inserir na tabela 'aluno' com o ID obtido
            cur.execute(
                "INSERT INTO cpe_enc.aluno (id_usuario, matricula, semestre) VALUES (%s, %s, %s)",
                (id_usuario, matricula, semestre)
            )

        # Se tudo deu certo, efetiva a transação
        conn.commit()
        print(f"\nAluno '{nome_completo}' criado com sucesso!")

    except psycopg.Error as e:
        # Se qualquer erro ocorrer, desfaz a transação inteira
        if conn:
            conn.rollback()
        print(f"Erro ao criar aluno: {e}")
    finally:
        # Fecha a conexão independentemente do resultado
        if conn:
            conn.close()


def read_alunos():
    conn = get_db_connection()
    if not conn:
        return False  # Retorna False para indicar que a operação não pôde ser concluída

    try:
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT u.id_usuario, u.nome_completo, u.email, a.matricula, a.semestre
                        FROM cpe_enc.usuario u
                                 JOIN cpe_enc.aluno a ON u.id_usuario = a.id_usuario
                        ORDER BY u.nome_completo;
                        """)
            alunos = cur.fetchall()

            if not alunos:
                print("\nNenhum aluno encontrado.")
                return False

            headers = [desc[0] for desc in cur.description]
            print("\n--- Lista de Alunos ---")
            print(tabulate(alunos, headers=headers, tablefmt="grid"))
            return True

    except psycopg.Error as e:
        print(f"Erro ao ler alunos: {e}")
        return False
    finally:
        if conn:
            conn.close()


def update_aluno():
    if not read_alunos():
        return

    conn = get_db_connection()
    if not conn:
        return

    try:
        id_aluno_str = input("\nDigite o ID do aluno que deseja atualizar: ")
        id_aluno = int(id_aluno_str)

        with conn.cursor() as cur:
            # Busca os dados atuais do aluno
            cur.execute("""
                        SELECT u.nome_completo, u.email, a.matricula, a.semestre
                        FROM cpe_enc.usuario u
                                 JOIN cpe_enc.aluno a ON u.id_usuario = a.id_usuario
                        WHERE u.id_usuario = %s;
                        """, (id_aluno,))
            aluno_atual = cur.fetchone()

            if not aluno_atual:
                print(f"Erro: Aluno com ID {id_aluno} não encontrado.")
                return

            nome_atual, email_atual, matricula_atual, semestre_atual = aluno_atual
            print("\nDigite os novos dados (pressione Enter para manter o valor atual):")

            novo_nome = input(f"Nome completo [{nome_atual}]: ") or nome_atual
            novo_email = input(f"Email [{email_atual}]: ") or email_atual
            nova_matricula = input(f"Matrícula [{matricula_atual}]: ") or matricula_atual

            while True:
                try:
                    novo_semestre_str = input(f"Semestre [{semestre_atual}]: ")
                    novo_semestre = int(novo_semestre_str) if novo_semestre_str else semestre_atual
                    if novo_semestre <= 0:
                        print("O semestre deve ser um número positivo.")
                        continue
                    break
                except ValueError:
                    print("Entrada inválida. Por favor, insira um número.")

            cur.execute(
                "UPDATE cpe_enc.usuario SET nome_completo = %s, email = %s WHERE id_usuario = %s",
                (novo_nome, novo_email, id_aluno)
            )
            # Atualiza a tabela 'aluno'
            cur.execute(
                "UPDATE cpe_enc.aluno SET matricula = %s, semestre = %s WHERE id_usuario = %s",
                (nova_matricula, novo_semestre, id_aluno)
            )

        conn.commit()
        print(f"\nDados do aluno ID {id_aluno} atualizados com sucesso!")

    except (ValueError, psycopg.Error) as e:
        if conn:
            conn.rollback()
        if isinstance(e, ValueError):
            print("Erro: ID inválido. Por favor, digite um número.")
        else:
            print(f"Erro ao atualizar aluno: {e}")
    finally:
        if conn:
            conn.close()


def delete_aluno():
    if not read_alunos():
        return

    conn = get_db_connection()
    if not conn:
        return

    try:
        id_aluno_str = input("\nDigite o ID do aluno que deseja deletar: ")
        id_aluno = int(id_aluno_str)

        with conn.cursor() as cur:
            cur.execute("SELECT nome_completo FROM cpe_enc.usuario WHERE id_usuario = %s", (id_aluno,))
            aluno = cur.fetchone()

            if not aluno:
                print(f"Erro: Aluno com ID {id_aluno} não encontrado.")
                return

            nome_aluno = aluno[0]
            confirmacao = input(
                f"Tem certeza que deseja deletar o aluno '{nome_aluno}' (ID: {id_aluno})? "
                f"Esta ação é irreversível. (s/n): ")

            if confirmacao.lower() != 's':
                print("Operação cancelada.")
                return

            cur.execute("DELETE FROM cpe_enc.usuario WHERE id_usuario = %s", (id_aluno,))

        conn.commit()
        print(f"\nAluno '{nome_aluno}' deletado com sucesso.")

    except (ValueError, psycopg.Error) as e:
        if conn:
            conn.rollback()
        if isinstance(e, ValueError):
            print("Erro: ID inválido. Por favor, digite um número.")
        else:
            print(f"Erro ao deletar aluno: {e}")
    finally:
        if conn:
            conn.close()