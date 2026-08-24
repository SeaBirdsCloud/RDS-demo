    -- CREATE DATABASE gerenciador_tarefas;

    USE gerenciador_tarefas;

    CREATE TABLE tarefas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        titulo VARCHAR(150) NOT NULL,
        descricao TEXT,
        status ENUM('pendente', 'concluida') DEFAULT 'pendente',
        prioridade ENUM('baixa', 'media', 'alta') DEFAULT 'media',
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE USER 'user-rds'@'%'
    IDENTIFIED BY 'P@ssw0rd';
    GRANT ALL PRIVILEGES ON gerenciador_tarefas.* TO 'user-rds'@'%';
    FLUSH PRIVILEGES;
