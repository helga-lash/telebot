CREATE TABLE IF NOT EXISTS users(
   tg_id VARCHAR (50) PRIMARY KEY,
   name VARCHAR (10) NOT NULL,
   surname VARCHAR (10) NOT NULL,
   phone_number VARCHAR (20) UNIQUE NOT NULL,
   notes TEXT,
   admin bool NOT NULL DEFAULT false
);