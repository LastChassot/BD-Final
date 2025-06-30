-- Inserindo Usuarios (Professores e Alunos)
INSERT INTO cpe_enc.usuario (nome_completo, email, senha_hash) VALUES
-- Professores "normais"
('Prof. Dr. Carlos Silva', 'carlos.silva@ufsc.br', 'senha_hash_123'),
('Profa. Dra. Ana Pereira', 'ana.pereira@ufsc.br', 'senha_hash_123'),
('Prof. Dr. João Mendes', 'joao.mendes@ufsc.br', 'senha_hash_123'),

-- Alunos
('Maria Joaquina', 'maria.joaquina@grad.ufsc.br', 'senha_hash_123'),
('José da Silva', 'jose.silva@grad.ufsc.br', 'senha_hash_123'),
('Beatriz Costa', 'beatriz.costa@grad.ufsc.br', 'senha_hash_123'),
('Lucas Martins', 'lucas.martins@grad.ufsc.br', 'senha_hash_123'),
('Fernanda Lima', 'fernanda.lima@grad.ufsc.br', 'senha_hash_123'),
('Ricardo Souza', 'ricardo.souza@grad.ufsc.br', 'senha_hash_123'),

-- Professores easter egg 🐣
('Prof. Roberta Silvano', 'roberta.silvano@ufsc.br', 'senha_hash_123'),
('Prof. Jhennifer Matias', 'jhennifer.matias@ufsc.br', 'senha_hash_123'),
('Prof. Augusto Scarduelli', 'augusto.scarduelli@ufsc.br', 'senha_hash_123'),
('Prof. Otavio Moratelli', 'otavio.moratelli@ufsc.br', 'senha_hash_123'),
('Prof. Vinicius Rover', 'vinicius.rover@ufsc.br', 'senha_hash_123'),
('Prof. Eduardo Hahn', 'eduardo.hahn@ufsc.br', 'senha_hash_123');

-- Especializando Professores (1 a 3 são os primeiros, 10 a 15 são os easter eggs)
INSERT INTO cpe_enc.professor (id_usuario, siape, sala) VALUES
(1, '112233', 'A101'),
(2, '445566', 'A102'),
(3, '778899', 'B205'),
(10, '987001', 'C301'),
(11, '987002', 'C302'),
(12, '987003', 'C303'),
(13, '987004', 'C304'),
(14, '987005', 'C305'),
(15, '987006', 'C306');

-- Especializando Alunos (id_usuario de 4 a 9)
INSERT INTO cpe_enc.aluno (id_usuario, matricula, semestre) VALUES
(4, '20220101', 4),
(5, '20210202', 6),
(6, '20230103', 2),
(7, '20200204', 8),
(8, '20220105', 4),
(9, '20210206', 6);

-- Inserindo Áreas de Interesse
INSERT INTO cpe_enc.area_de_interesse (nome_area) VALUES
('Inteligência Artificial'),
('Sistemas Embarcados'),
('Segurança da Informação'),
('Desenvolvimento Web'),
('Redes de Computadores'),
('Blockchain e Criptografia');

-- Inserindo Projetos (com professores comuns e easter egg)
INSERT INTO cpe_enc.projeto (titulo, descricao, dt_inicio, dt_fim_prevista, status, id_professor_orientador) VALUES
-- Normais
('Sistema de Recomendação para E-commerce', 'Desenvolvimento de um sistema de recomendação baseado em filtragem colaborativa.', '2024-03-01', '2025-03-01', 'Em Andamento', 1),
('Detecção de Anomalias em Redes IoT', 'Uso de machine learning para detectar comportamento anômalo em redes de sensores.', '2023-09-01', '2024-09-01', 'Em Andamento', 2),
('Plataforma Segura de Votação Eletrônica', 'Implementação de um sistema de votação com blockchain para garantir a segurança.', '2024-01-15', '2025-01-15', 'Em Andamento', 3),
('Robô Seguidor de Linha Autônomo', 'Projeto de hardware e software para um robô competidor.', '2023-05-01', '2024-05-01', 'Concluído', 2),
('Portal de Notícias para o Campus', 'Desenvolvimento de um portal web completo com React e Node.js.', '2024-08-01', '2025-02-01', 'Proposto', 1),

-- Easter Eggs
('IA Aplicada à Educação', 'Estudo de técnicas de IA para personalizar o ensino.', '2024-03-10', '2025-03-10', 'Em Andamento', 10),
('Sistemas Distribuídos Avançados', 'Simulação de sistemas distribuídos com tolerância a falhas.', '2024-04-15', '2025-04-15', 'Proposto', 11),
('Plataforma para Simulações Científicas', 'Sistema que permite execução remota de simulações.', '2024-01-01', '2025-01-01', 'Em Andamento', 12),
('Sistema de Detecção de Fake News', 'Uso de NLP para verificação automática de notícias.', '2024-02-01', '2025-02-01', 'Em Andamento', 13),
('Aplicação Web para Gestão de Eventos', 'Agenda de eventos para universidades com notificações.', '2024-06-01', '2024-12-01', 'Proposto', 14);

-- Associando Projetos e Áreas
INSERT INTO cpe_enc.projeto_area (id_projeto, id_area) VALUES
(1, 1), (1, 4),
(2, 1), (2, 5),
(3, 3), (3, 6),
(4, 2),
(5, 4),
(6, 1),
(7, 2),
(8, 4),
(9, 1), (9, 3),
(10, 4);

-- Alunos em Projetos
INSERT INTO cpe_enc.aluno_projeto (id_aluno, id_projeto, data_ingresso) VALUES
(4, 1, '2024-03-15'),
(5, 1, '2024-04-01'),
(6, 2, '2023-10-01'),
(7, 3, '2024-02-01'),
(5, 4, '2023-06-01'),
(8, 6, '2024-03-20'),
(9, 9, '2024-04-02');

-- Inserindo Vagas
INSERT INTO cpe_enc.vaga (id_projeto, descricao_requisitos, numero_posicoes, prazo_inscricao) VALUES
(1, 'Conhecimento em Python e Pandas. Desejável ter cursado IA.', 2, '2025-07-30 23:59:59'),
(2, 'Conhecimento em Redes e Machine Learning.', 1, '2025-08-15 23:59:59'),
(3, 'Interesse em criptografia e blockchain. Lógica de programação avançada.', 2, '2025-07-20 23:59:59'),
(6, 'Noções básicas de educação e IA. Desejável experiência com GPT.', 1, '2025-07-01 23:59:59'),
(9, 'Conhecimento básico em HTML/CSS. Curiosidade sobre algoritmos.', 1, '2025-07-15 23:59:59');

-- Candidaturas a Vagas
INSERT INTO cpe_enc.candidatura (id_aluno, id_vaga, status) VALUES
(8, 1, 'Enviada'),
(9, 1, 'Enviada'),
(4, 2, 'Aprovada'),
(6, 3, 'Em Análise'),
(7, 4, 'Enviada'),
(5, 5, 'Enviada');
