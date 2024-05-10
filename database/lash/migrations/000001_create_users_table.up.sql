CREATE TABLE IF NOT EXISTS users(
   tg_id VARCHAR (50) PRIMARY KEY,
   name VARCHAR (50) NOT NULL,
   surname VARCHAR (50) NOT NULL,
   phone_number VARCHAR (20) UNIQUE NOT NULL,
   description TEXT
);