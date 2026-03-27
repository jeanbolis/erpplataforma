-- =====================================================
-- ERP - Módulo de Vendas
-- Idioma: Português Brasil
-- =====================================================

CREATE TABLE IF NOT EXISTS vendas (
    id INT AUTO_INCREMENT PRIMARY KEY,

    cliente VARCHAR(150) NOT NULL,
    data_venda DATE NOT NULL,
    observacao TEXT,

    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB
CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS vendas_itens (
    id INT AUTO_INCREMENT PRIMARY KEY,

    venda_id INT NOT NULL,
    produto_id INT NOT NULL,
    quantidade DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_venda
        FOREIGN KEY (venda_id)
        REFERENCES vendas(id),

    CONSTRAINT fk_venda_produto
        FOREIGN KEY (produto_id)
        REFERENCES produtos(id)

) ENGINE=InnoDB
CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;