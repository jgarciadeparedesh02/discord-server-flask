-- Crear la tabla User
CREATE TABLE tellmedam_user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    photoUrl VARCHAR(255)
);

-- Crear la tabla Chat
CREATE TABLE tellmedam_chat (
    id SERIAL PRIMARY KEY,
    idUser1 INTEGER REFERENCES tellmedam_user(id) NOT NULL,
    idUser2 INTEGER REFERENCES tellmedam_user(id) NOT NULL,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear la tabla Message
CREATE TABLE tellmedam_message (
    id SERIAL PRIMARY KEY,
    idSender INTEGER REFERENCES tellmedam_user(id) NOT NULL,
    content TEXT NOT NULL,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    receivedAt TIMESTAMP,
    chatId INTEGER REFERENCES tellmedam_chat(id) NOT NULL
);




-- Inserts para la tabla tellmedam_user
INSERT INTO tellmedam_user (username, email, password, photoUrl) VALUES
    ('user1', 'user1@example.com', 'password1', 'photo1.jpg'),
    ('user2', 'user2@example.com', 'password2', 'photo2.jpg'),
    ('user3', 'user3@example.com', 'password3', 'photo3.jpg');

-- Inserts para la tabla tellmedam_chat
INSERT INTO tellmedam_chat (idUser1, idUser2, createdAt, updatedAt) VALUES
    (1, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (1, 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (2, 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Inserts para la tabla tellmedam_message
INSERT INTO tellmedam_message (idSender, content, createdAt, receivedAt, chatId) VALUES
    (1, 'Hola, ¿cómo estás?', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
    (2, '¡Hola! Estoy bien, gracias.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
    (3, 'Hola a ambos, ¿qué tal?', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
    (1, 'Todo bien por aquí.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 2),
    (2, 'Me alegra escuchar eso.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 2),
    (3, 'Sí, todo está bien. Gracias.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 3);
