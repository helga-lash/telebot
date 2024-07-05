CREATE TABLE IF NOT EXISTS scheduler_jobs(
   id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
   execute_time timestamp NOT NULL,
   user_id VARCHAR (50) NOT NULL,
   data jsonb NOT NULL,
   created_at timestamp NOT NULL DEFAULT current_timestamp,
   updated_at timestamp NOT NULL DEFAULT current_timestamp,
   lock bool NOT NULL DEFAULT false,
   done bool NOT NULL DEFAULT false,
   constraint scheduler_jobs_users_fk foreign key (user_id) references users (tg_id) on delete cascade on update cascade
);