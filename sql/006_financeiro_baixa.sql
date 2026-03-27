-- =====================================================
-- ERP - Financeiro | Baixa Financeira
-- =====================================================

ALTER TABLE contas_pagar
ADD COLUMN data_baixa DATE NULL;

ALTER TABLE contas_receber
ADD COLUMN data_baixa DATE NULL;