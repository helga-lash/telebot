CREATE TABLE IF NOT EXISTS registrations(
   id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
   date DATE NOT NULL,
   time time NOT NULL,
   user_id VARCHAR (50),
   confirmation_day bool NOT NULL DEFAULT false,
   confirmation_two_hours bool NOT NULL DEFAULT false,
   lock bool NOT NULL DEFAULT false,
   notes TEXT,
   constraint registrations_user_fk foreign key (user_id) references users (tg_id) on delete cascade on update cascade
);