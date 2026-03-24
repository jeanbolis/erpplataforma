-- =====================================================
-- ERP - Schema Inicial
-- Módulo: Produtos
-- Idioma: Português Brasil
-- =====================================================

CREATE TABLE IF NOT EXISTS produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,

    codigo VARCHAR(30) NOT NULL,
    nome VARCHAR(150) NOT NULL,
    descricao TEXT,

    sku VARCHAR(60),
    ean VARCHAR(14),
    ncm VARCHAR(10),

    unidade VARCHAR(10) NOT NULL DEFAULT 'UN',
    ativo TINYINT(1) NOT NULL DEFAULT 1,

    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY uk_produtos_codigo (codigo),
    UNIQUE KEY uk_produtos_sku (sku),
    UNIQUE KEY uk_produtos_ean (ean),
    KEY idx_produtos_nome (nome)

) ENGINE=InnoDB
CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;

SHOW TABLES;