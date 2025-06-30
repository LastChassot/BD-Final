import os
import sys
from typing import Dict, Callable, Any
from tabulate import tabulate

from crud import aluno_crud
from crud import professor_crud
from crud import projeto_crud
import reports
import db_setup
import ai_assistant
from db_config import get_db_connection


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    input("\nPressione Enter para continuar...")


def gerenciar_alunos():
    def _create_aluno_interactive():
        print("\n--- Criar Novo Aluno ---")
        nome_completo = input("Nome Completo: ")
        email = input("Email: ")
        senha_hash = input("Senha (hash): ")
        matricula = input("Matrícula: ")
        semestre_str = input("Semestre (opcional, deixe em branco se não souber): ")
        semestre = int(semestre_str) if semestre_str.isdigit() else None
        aluno_crud.create_aluno(nome_completo, email, senha_hash, matricula, semestre)

    def _list_alunos_interactive():
        print("\n--- Listar Alunos ---")
        alunos = aluno_crud.get_all_alunos()
        if alunos:
            headers = ["ID", "Nome Completo", "Email", "Matrícula", "Semestre"]
            data = [[a['id_usuario'], a['nome_completo'], a['email'], a['matricula'],
                     a['semestre']] for a in alunos]
            print(tabulate(data, headers=headers, tablefmt="grid"))
        else:
            print("Nenhum aluno cadastrado.")

    def _update_aluno_interactive():
        print("\n--- Atualizar Aluno ---")
        try:
            id_aluno = int(input("ID do Aluno a ser atualizado: "))
        except ValueError:
            print("ID inválido. Por favor, insira um número.")
            return

        current_aluno = aluno_crud.get_aluno_by_id(id_aluno)
        if not current_aluno:
            print(f"Aluno com ID {id_aluno} não encontrado.")
            return

        print(f"Atualizando Aluno: {current_aluno['nome_completo']}")
        print("Deixe em branco para manter o valor atual.")

        nome_completo = input(f"Novo Nome Completo ({current_aluno['nome_completo']}): ") or None
        email = input(f"Novo Email ({current_aluno['email']}): ") or None
        senha_hash = input("Nova Senha (hash, deixe em branco para manter): ") or None
        matricula = input(f"Nova Matrícula ({current_aluno['matricula']}): ") or None

        semestre_input = input(
            f"Novo Semestre ({current_aluno['semestre'] if current_aluno['semestre'] is not None else 'N/A'}): ")
        semestre = int(semestre_input) if semestre_input.isdigit() else (
            None if semestre_input == '' else current_aluno['semestre'])

        aluno_crud.update_aluno(id_aluno, nome_completo, email, senha_hash, matricula, semestre)

    def _delete_aluno_interactive():
        print("\n--- Deletar Aluno ---")
        try:
            id_aluno = int(input("ID do Aluno a ser deletado: "))
        except ValueError:
            print("ID inválido. Por favor, insira um número.")
            return
        aluno_crud.delete_aluno(id_aluno)

    menu_options: Dict[str, Callable] = {
        "1": _create_aluno_interactive,
        "2": _list_alunos_interactive,
        "3": _update_aluno_interactive,
        "4": _delete_aluno_interactive,
    }

    while True:
        clear_screen()
        print("--- Gerenciar Alunos ---")
        print("1. Criar Aluno")
        print("2. Listar Alunos")
        print("3. Atualizar Aluno")
        print("4. Deletar Aluno")
        print("0. Voltar")

        choice = input("Escolha uma opção: ")

        if choice == '0':
            break

        action = menu_options.get(choice)
        if action:
            action()
        else:
            print("Opção inválida.")

        pause()


def gerenciar_professores():
    def _create_professor_interactive():
        print("\n--- Criar Novo Professor ---")
        nome_completo = input("Nome Completo: ")
        email = input("Email: ")
        senha_hash = input("Senha (hash): ")  # Em um sistema real, isso seria gerado/hashed
        siape = input("SIAPE: ")
        sala = input("Sala (opcional, deixe em branco): ") or None
        professor_crud.create_professor(nome_completo, email, senha_hash, siape, sala)

    def _list_professores_interactive():
        print("\n--- Listar Professores ---")
        professores = professor_crud.get_all_professores()
        if professores:
            headers = ["ID", "Nome Completo", "Email", "SIAPE", "Sala"]
            data = [[p['id_usuario'], p['nome_completo'], p['email'], p['siape'], p['sala']] for p in professores]
            print(tabulate(data, headers=headers, tablefmt="grid"))
        else:
            print("Nenhum professor cadastrado.")

    def _update_professor_interactive():
        print("\n--- Atualizar Professor ---")
        try:
            id_professor = int(input("ID do Professor a ser atualizado: "))
        except ValueError:
            print("ID inválido. Por favor, insira um número.")
            return

        current_professor = professor_crud.get_professor_by_id(id_professor)
        if not current_professor:
            print(f"Professor com ID {id_professor} não encontrado.")
            return

        print(f"Atualizando Professor: {current_professor['nome_completo']}")
        print("Deixe em branco para manter o valor atual.")

        nome_completo = input(f"Novo Nome Completo ({current_professor['nome_completo']}): ") or None
        email = input(f"Novo Email ({current_professor['email']}): ") or None
        senha_hash = input("Nova Senha (hash, deixe em branco para manter): ") or None
        siape = input(f"Novo SIAPE ({current_professor['siape']}): ") or None
        sala = input(
            f"Nova Sala ({current_professor['sala'] if current_professor['sala'] is not None else 'N/A'}): ") or None

        professor_crud.update_professor(id_professor, nome_completo, email, senha_hash, siape, sala)

    def _delete_professor_interactive():
        print("\n--- Deletar Professor ---")
        try:
            id_professor = int(input("ID do Professor a ser deletado: "))
        except ValueError:
            print("ID inválido. Por favor, insira um número.")
            return
        professor_crud.delete_professor(id_professor)

    menu_options: Dict[str, Callable] = {
        "1": _create_professor_interactive,
        "2": _list_professores_interactive,
        "3": _update_professor_interactive,
        "4": _delete_professor_interactive,
    }

    while True:
        clear_screen()
        print("--- Gerenciar Professores ---")
        print("1. Criar Professor")
        print("2. Listar Professores")
        print("3. Atualizar Professor")
        print("4. Deletar Professor")
        print("0. Voltar")

        choice = input("Escolha uma opção: ")

        if choice == '0':
            break

        action = menu_options.get(choice)
        if action:
            action()
        else:
            print("Opção inválida.")

        pause()


def gerenciar_projetos():
    def _create_projeto_interactive():
        print("\n--- Criar Novo Projeto ---")
        titulo = input("Título do Projeto: ")
        descricao = input("Descrição: ")
        dt_inicio = input("Data de Início (YYYY-MM-DD): ")
        dt_fim_prevista_str = input("Data de Fim Prevista (YYYY-MM-DD, opcional, deixe em branco): ")
        dt_fim_prevista = dt_fim_prevista_str if dt_fim_prevista_str else None
        status = input("Status (Proposto, Em Andamento, Concluido, Cancelado): ")
        try:
            id_professor_orientador = int(input("ID do Professor Orientador: "))
        except ValueError:
            print("ID do Professor inválido. Por favor, insira um número.")
            return

        projeto_crud.create_projeto(titulo, descricao, dt_inicio, dt_fim_prevista, status,
                                     id_professor_orientador)

    def _list_projetos_interactive():
        print("\n--- Listar Projetos ---")
        projetos = projeto_crud.get_all_projetos()
        if projetos:
            headers = ["ID", "Título", "Descrição", "Início", "Fim Previsto", "Status", "Orientador"]
            data = [[p['id_projeto'], p['titulo'], p['descricao'], p['dt_inicio'], p['dt_fim_prevista'],
                     p['status'],
                     p['professor_orientador']] for p in projetos]
            print(tabulate(data, headers=headers, tablefmt="grid"))
        else:
            print("Nenhum projeto cadastrado.")

    def _update_projeto_interactive():
        print("\n--- Atualizar Projeto ---")
        try:
            id_projeto = int(input("ID do Projeto a ser atualizado: "))
        except ValueError:
            print("ID inválido. Por favor, insira um número.")
            return

        current_projeto = projeto_crud.get_projeto_by_id(id_projeto)
        if not current_projeto:
            print(f"Projeto com ID {id_projeto} não encontrado.")
            return

        print(f"Atualizando Projeto: {current_projeto['titulo']}")
        print("Deixe em branco para manter o valor atual.")

        titulo = input(f"Novo Título ({current_projeto['titulo']}): ") or None
        descricao = input(f"Nova Descrição ({current_projeto['descricao']}): ") or None
        dt_inicio = input(f"Nova Data de Início (YYYY-MM-DD, {current_projeto['dt_inicio']}): ") or None

        dt_fim_prevista_str = input(
            f"Nova Data de Fim Prevista (YYYY-MM-DD, {current_projeto['dt_fim_prevista'] 
            if current_projeto['dt_fim_prevista'] is not None else 'N/A'}): ")
        dt_fim_prevista = dt_fim_prevista_str if dt_fim_prevista_str != '' else None

        status = input(
            f"Novo Status (Proposto, Em Andamento, Concluido, Cancelado) ({current_projeto['status']}): ") or None

        id_professor_orientador_str = input(
            f"Novo ID do Professor Orientador ({current_projeto['id_professor_orientador']}): ")
        id_professor_orientador = int(id_professor_orientador_str) if (id_professor_orientador_str.
                                                                       isdigit()) else None

        projeto_crud.update_projeto(id_projeto, titulo, descricao, dt_inicio, dt_fim_prevista, status,
                                     id_professor_orientador)

    def _delete_projeto_interactive():
        print("\n--- Deletar Projeto ---")
        try:
            id_projeto = int(input("ID do Projeto a ser deletado: "))
        except ValueError:
            print("ID inválido. Por favor, insira um número.")
            return
        projeto_crud.delete_projeto(id_projeto)

    menu_options: Dict[str, Callable] = {
        "1": _create_projeto_interactive,
        "2": _list_projetos_interactive,
        "3": _update_projeto_interactive,
        "4": _delete_projeto_interactive,
    }

    while True:
        clear_screen()
        print("--- Gerenciar Projetos ---")
        print("1. Criar Projeto")
        print("2. Listar Projetos")
        print("3. Atualizar Projeto")
        print("4. Deletar Projeto")
        print("0. Voltar")

        choice = input("Escolha uma opção: ")

        if choice == '0':
            break

        action = menu_options.get(choice)
        if action:
            action()
        else:
            print("Opção inválida.")

        pause()


def menu_crud():
    """Exibe o menu principal de operações CRUD."""

    menu_options: Dict[str, Callable] = {
        "1": gerenciar_alunos,
        "2": gerenciar_professores,
        "3": gerenciar_projetos,
    }

    while True:
        clear_screen()
        print("--- Menu de Operações CRUD ---")
        print("1. Gerenciar Alunos")
        print("2. Gerenciar Professores")
        print("3. Gerenciar Projetos")
        print("0. Voltar ao Menu Principal")

        choice = input("Escolha uma opção: ")

        if choice == '0':
            break

        action = menu_options.get(choice)
        if action:
            action()
        else:
            print("Opção inválida.")
            pause()


def menu_relatorios():
    """Exibe o menu de relatórios gerenciais e gera os gráficos."""
    conn = get_db_connection()
    if not conn:
        print("\nErro: Não foi possível conectar ao banco de dados.")
        pause()
        return

    menu_actions: Dict[str, Callable] = {
        "1": lambda: reports.gerar_grafico_consulta1(conn),
        "2": lambda: reports.gerar_grafico_consulta2(conn),
        "3": lambda: reports.gerar_grafico_consulta3(conn),
    }

    try:
        while True:
            clear_screen()
            print("--- Menu de Relatórios Gerenciais ---")
            print("1. Popularidade das Áreas por Engajamento de Alunos")
            print("2. Ranking de Professores por Volume de Projetos Ativos")
            print("3. Distribuição de Vagas Abertas por Projeto")
            print("0. Voltar")

            choice = input("Escolha uma opção: ")

            if choice == '0':
                break

            action = menu_actions.get(choice)
            if action:
                action()
                print("\nRelatório gerado com sucesso!")
            else:
                print("Opção inválida.")

            pause()
    finally:
        if conn:
            conn.close()


def drop_all_tables_confirmed():
    """Confirma e executa a exclusão de todas as tabelas do banco de dados."""
    clear_screen()
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!! ATENÇÃO!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("Esta ação é DESTRUTIVA e IRREVERSÍVEL.")
    print("Todas as tabelas e dados do banco de dados serão PERMANENTEMENTE APAGADOS.")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")

    confirm = input('Para confirmar, digite "APAGAR TUDO" e pressione Enter: ')

    if confirm == "APAGAR TUDO":
        db_setup.drop_all_tables()
    else:
        print("\nOperação cancelada. Nenhuma tabela foi apagada.")
    pause()


def main():
    if hasattr(reports, 'OUTPUT_DIR') and not os.path.exists(reports.OUTPUT_DIR):
        os.makedirs(reports.OUTPUT_DIR)
        print(f"Pasta '{reports.OUTPUT_DIR}' criada para salvar relatórios.")
        pause()

    main_menu_actions: Dict[str, Callable] = {
        "1": menu_crud,
        "2": menu_relatorios,
        "3": ai_assistant.ask_ai,
        "4": db_setup.create_tables,
        "5": db_setup.seed_data,
        "6": drop_all_tables_confirmed,
    }

    while True:
        clear_screen()
        print("====== SISTEMA DE GESTÃO DE PROJETOS DE EXTENSÃO ======")
        print("\n")
        print("1. Operações CRUD (Inserir, Ler, Atualizar, Deletar)")

        print("\n")
        print("2. Gerar Relatórios Gerenciais")

        print("\n")
        print("3. Assistente de IA (Linguagem Natural para SQL)")

        print("\n")
        print("4. Criar Estrutura de Tabelas (Requer BD vazio)")
        print("5. Popular Banco de Dados com Dados de Exemplo (Seed)")
        print("6. APAGAR TODAS AS TABELAS (AÇÃO DESTRUTIVA)")

        print("\n0. Sair")
        print("=======================================================")

        choice = input("Escolha uma opção: ")

        if choice == '0':
            print("\nSaindo do sistema. Até logo!")
            sys.exit(0)

        action = main_menu_actions.get(choice)
        if action:
            if choice in ["1", "2", "3"]:
                action()
            else:
                action()
        else:
            print("Opção inválida. Tente novamente.")
            pause()


if __name__ == "__main__":
    main()