-- =============================================
-- SCRIPT DE MIGRAÇÃO: ADICIONAR COLUNA SINTOMAS
-- =============================================
-- Execute este script no banco de dados existente para adicionar
-- a coluna 'sintomas' na tabela 'agendamento'
-- =============================================

-- Adiciona a coluna 'sintomas' na tabela agendamento
ALTER TABLE agendamento 
ADD COLUMN IF NOT EXISTS sintomas TEXT;

-- Confirma que a coluna foi adicionada
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns 
WHERE table_name = 'agendamento' 
ORDER BY ordinal_position;

-- Mensagem de sucesso (comentário)
-- A coluna 'sintomas' foi adicionada com sucesso à tabela 'agendamento'
-- Os clientes agora podem descrever seus sintomas ao fazer agendamentos