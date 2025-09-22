
-- =============================================
-- INSTRUÇÕES PARA USO COM SUPABASE/POSTGRESQL
-- =============================================
-- 1. Conecte-se ao banco de dados já criado no Supabase usando as credenciais fornecidas.
-- 2. NÃO execute CREATE DATABASE aqui! O banco já existe.
-- 3. Execute apenas os comandos de CREATE TABLE, INSERT, etc, já conectado ao banco.
-- 4. Se usar VS Code, selecione a conexão do banco antes de rodar este script.
-- =============================================
-- CREATE DATABASE hmmassoterapia;  -- (Comentado para evitar erro)
CREATE TABLE IF NOT EXISTS cliente ( 
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    sexo VARCHAR(20) NOT NULL,
    data_nascimento DATE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) DEFAULT 'sem_senha',
    email_confirmado BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS massoterapeuta (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    sexo VARCHAR(20) NOT NULL,
    data_nascimento DATE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) DEFAULT 'sem_senha',
    email_confirmado BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS agendamento (
    id SERIAL PRIMARY KEY,
    cliente_id INT NOT NULL,
    massoterapeuta_id INT NOT NULL,
    data_hora TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'marcado',
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES cliente(id) ON DELETE CASCADE,
    FOREIGN KEY (massoterapeuta_id) REFERENCES massoterapeuta(id) ON DELETE CASCADE
);

-- Inserts de exemplo
INSERT INTO cliente (nome, telefone, sexo, data_nascimento, email)
VALUES 
('Makoto Higashi', '11777777777', 'Masculino', '1990-05-10', 'makoto@gmail.com');

INSERT INTO massoterapeuta (nome, telefone, sexo, data_nascimento, email)
VALUES
('Luara Meissner', '113777777777', 'Feminino', '1980-03-15', 'luara@gmail.com');

-- Testes
SELECT * FROM cliente; 
SELECT * FROM massoterapeuta;
SELECT * FROM agendamento; 

DELETE FROM cliente;
DELETE FROM massoterapeuta;
DELETE FROM agendamento;

ALTER SEQUENCE cliente_id_seq RESTART WITH 1;
ALTER SEQUENCE massoterapeuta_id_seq RESTART WITH 1;
