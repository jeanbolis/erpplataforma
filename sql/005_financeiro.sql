-- =====================================================
-- ERP - Módulo Financeiro
-- Idioma: Português Brasil
-- =====================================================

CREATE TABLE IF NOT EXISTS contas_pagar (
    id INT AUTO_INCREMENT PRIMARY KEY,

    referencia_tipo VARCHAR(20) NOT NULL, -- COMPRA
    referencia_id INT NOT NULL,

    fornecedor VARCHAR(150) NOT NULL,
    valor DECIMAL(12,2) NOT NULL,
    data_vencimento DATE NOT NULL,

    status ENUM('ABERTO', 'PAGO') NOT NULL DEFAULT 'ABERTO',

    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB
CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS contas_receber (
    id INT AUTO_INCREMENT PRIMARY KEY,

    referencia_tipo VARCHAR(20) NOT NULL, -- VENDA
    referencia_id INT NOT NULL,

    cliente VARCHAR(150) NOT NULL,
    valor DECIMAL(12,2) NOT NULL,
    data_vencimento DATE NOT NULL,

    status ENUM('ABERTO', 'RECEBIDO') NOT NULL DEFAULT 'ABERTO',

    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB
CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;