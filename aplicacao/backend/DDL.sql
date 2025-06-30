-- Criacao do esquema para encapsular o projeto
CREATE SCHEMA cpe_enc;

-- Tabela base para todos os usuarios do sistema
CREATE TABLE cpe_enc.usuario (
    id_usuario SERIAL PRIMARY KEY,
    nome_completo VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL
);

-- Tabela de especializacao para Professores
CREATE TABLE cpe_enc.professor (
    id_usuario INTEGER PRIMARY KEY,
    siape VARCHAR(20) NOT NULL UNIQUE,
    sala VARCHAR(50),
    CONSTRAINT fk_professor_usuario FOREIGN KEY (id_usuario) REFERENCES cpe_enc.usuario(id_usuario) ON DELETE CASCADE
);

-- Tabela de especializacao para Alunos
CREATE TABLE cpe_enc.aluno (
    id_usuario INTEGER PRIMARY KEY,
    matricula VARCHAR(20) NOT NULL UNIQUE,
    semestre INTEGER,
    CONSTRAINT fk_aluno_usuario FOREIGN KEY (id_usuario) REFERENCES cpe_enc.usuario(id_usuario) ON DELETE CASCADE,
    CONSTRAINT chk_semestre_valido CHECK (semestre IS NULL OR semestre > 0)
);

-- Tabela para armazenar as areas de interesse/pesquisa
CREATE TABLE cpe_enc.area_de_interesse (
    id_area SERIAL PRIMARY KEY,
    nome_area VARCHAR(100) NOT NULL UNIQUE
);

-- Tabela central de Projetos
CREATE TABLE cpe_enc.projeto (
    id_projeto SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    dt_inicio DATE NOT NULL,
    dt_fim_prevista DATE,
    status VARCHAR(50) NOT NULL DEFAULT 'Proposto',
    id_professor_orientador INTEGER NOT NULL,
    CONSTRAINT fk_projeto_professor FOREIGN KEY (id_professor_orientador) REFERENCES cpe_enc.professor(id_usuario),
    CONSTRAINT chk_status_projeto CHECK (status IN ('Proposto', 'Em Andamento', 'Concluido', 'Cancelado')),
    CONSTRAINT chk_datas_validas CHECK (dt_fim_prevista IS NULL OR dt_fim_prevista > dt_inicio)
);

-- Tabela de juncao para o relacionamento N:M entre Projeto e AreaDeInteresse
CREATE TABLE cpe_enc.projeto_area (
    id_projeto INTEGER,
    id_area INTEGER,
    CONSTRAINT pk_projeto_area PRIMARY KEY (id_projeto, id_area),
    CONSTRAINT fk_projetoarea_projeto FOREIGN KEY (id_projeto) REFERENCES cpe_enc.projeto(id_projeto) ON DELETE CASCADE,
    CONSTRAINT fk_projetoarea_area FOREIGN KEY (id_area) REFERENCES cpe_enc.area_de_interesse(id_area) ON DELETE CASCADE
);

-- Tabela de juncao para o relacionamento N:M entre Aluno e Projeto
CREATE TABLE cpe_enc.aluno_projeto (
    id_aluno INTEGER,
    id_projeto INTEGER,
    data_ingresso DATE NOT NULL DEFAULT CURRENT_DATE,
    CONSTRAINT pk_aluno_projeto PRIMARY KEY (id_aluno, id_projeto),
    CONSTRAINT fk_alunoprojeto_aluno FOREIGN KEY (id_aluno) REFERENCES cpe_enc.aluno(id_usuario) ON DELETE CASCADE,
    CONSTRAINT fk_alunoprojeto_projeto FOREIGN KEY (id_projeto) REFERENCES cpe_enc.projeto(id_projeto) ON DELETE CASCADE
);

-- Tabela para cadastro de Vagas em projetos
CREATE TABLE cpe_enc.vaga (
    id_vaga SERIAL PRIMARY KEY,
    id_projeto INTEGER NOT NULL,
    descricao_requisitos TEXT,
    numero_posicoes INTEGER NOT NULL,
    prazo_inscricao TIMESTAMP NOT NULL,
    CONSTRAINT fk_vaga_projeto FOREIGN KEY (id_projeto) REFERENCES cpe_enc.projeto(id_projeto) ON DELETE CASCADE,
    CONSTRAINT chk_posicoes_positivas CHECK (numero_posicoes > 0)
);

-- Tabela para registrar as Candidaturas dos alunos as vagas
CREATE TABLE cpe_enc.candidatura (
    id_candidatura SERIAL PRIMARY KEY,
    id_aluno INTEGER NOT NULL,
    id_vaga INTEGER NOT NULL,
    dt_candidatura TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL DEFAULT 'Enviada',
    CONSTRAINT fk_candidatura_aluno FOREIGN KEY (id_aluno) REFERENCES cpe_enc.aluno(id_usuario) ON DELETE CASCADE,
    CONSTRAINT fk_candidatura_vaga FOREIGN KEY (id_vaga) REFERENCES cpe_enc.vaga(id_vaga) ON DELETE CASCADE,
    CONSTRAINT chk_status_candidatura CHECK (status IN ('Enviada', 'Em Analise', 'Aprovada', 'Rejeitada')),
    CONSTRAINT uq_aluno_vaga UNIQUE (id_aluno, id_vaga)
);

-- Tabela para os Marcos (milestones) do calendario do projeto
CREATE TABLE cpe_enc.marco_calendario (
    id_marco SERIAL PRIMARY KEY,
    id_projeto INTEGER NOT NULL,
    titulo_marco VARCHAR(255) NOT NULL,
    data_marco DATE NOT NULL,
    descricao TEXT,
    CONSTRAINT fk_marco_projeto FOREIGN KEY (id_projeto) REFERENCES cpe_enc.projeto(id_projeto) ON DELETE CASCADE
);

-- Tabela para registrar as Publicacoes resultantes de um projeto
CREATE TABLE cpe_enc.publicacao (
    id_publicacao SERIAL PRIMARY KEY,
    id_projeto INTEGER NOT NULL,
    titulo_publicacao VARCHAR(512) NOT NULL,
    ano_publicacao INTEGER NOT NULL,
    referencia TEXT,
    CONSTRAINT fk_publicacao_projeto FOREIGN KEY (id_projeto) REFERENCES cpe_enc.projeto(id_projeto) ON DELETE CASCADE,
    CONSTRAINT chk_ano_publicacao CHECK (ano_publicacao > 1900)
);