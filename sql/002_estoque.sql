-- =====================================================
-- ERP - Módulo de Estoque
-- Idioma: Português Brasil
-- =====================================================

CREATE TABLE IF NOT EXISTS estoque_movimentacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,

    produto_id INT NOT NULL,
    tipo_movimentacao ENUM('ENTRADA', 'SAIDA') NOT NULL,
    quantidade DECIMAL(10, 2) NOT NULL,

    origem VARCHAR(50),
    observacao TEXT,

    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_estoque_produto
        FOREIGN KEY (produto_id)
        REFERENCES produtos(id)
) ENGINE=InnoDB
CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;