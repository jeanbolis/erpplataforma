-- =====================================================
-- ERP - Módulo de Compras
-- Idioma: Português Brasil
-- =====================================================

CREATE TABLE IF NOT EXISTS compras (
    id INT AUTO_INCREMENT PRIMARY KEY,

    fornecedor VARCHAR(150) NOT NULL,
    data_compra DATE NOT NULL,
    observacao TEXT,

    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB
CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS compras_itens (
    id INT AUTO_INCREMENT PRIMARY KEY,

    compra_id INT NOT NULL,
    produto_id INT NOT NULL,
    quantidade DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_compra
        FOREIGN KEY (compra_id)
        REFERENCES compras(id),

    CONSTRAINT fk_compra_produto
        FOREIGN KEY (produto_id)
        REFERENCES produtos(id)

) ENGINE=InnoDB
CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;