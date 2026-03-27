-- =====================================================
-- ERP - Auditoria de Ações
-- =====================================================

CREATE TABLE IF NOT EXISTS auditoria (
    id INT AUTO_INCREMENT PRIMARY KEY,

    usuario_id INT,
    email_usuario VARCHAR(150),

    acao VARCHAR(100) NOT NULL,
    recurso VARCHAR(100) NOT NULL,

    detalhes TEXT,
    ip_origem VARCHAR(50),

    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB
CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;