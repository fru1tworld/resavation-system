CREATE TABLE IF NOT EXISTS users (
    user_id bigint PRIMARY KEY,
    password varchar(80) NOT NULL,
    name varchar(50) UNIQUE NOT NULL,
    role varchar(10) NOT NULL,
    created_at timestamp NOT NULL
);

CREATE TABLE IF NOT EXISTS exam_categorie (
    exam_categorie_id bigint PRIMARY KEY,
    name varchar(255) NOT NULL,
    created_at timestamp NOT NULL
);

CREATE TABLE IF NOT EXISTS exam_info (
    exam_info_id bigint PRIMARY KEY,
    exam_name varchar(255) NOT NULL,
    exam_description varchar(3000),
    exam_category_id bigint,
    created_at timestamp NOT NULL
);

CREATE TABLE IF NOT EXISTS exam_schedule (
    exam_schedules_id bigint PRIMARY KEY,
    exam_id bigint NOT NULL,
    start_time timestamp NOT NULL,
    end_time timestamp NOT NULL,
    created_at timestamp NOT NULL
);

CREATE TABLE IF NOT EXISTS exam_reservation (
    exam_reservations_id bigint PRIMARY KEY,
    user_id bigint NOT NULL,
    exam_schedule_id bigint NOT NULL,
    reservation_status varchar(20) NOT NULL,
    created_at timestamp NOT NULL
);

CREATE TABLE IF NOT EXISTS exam_time_slot (
    exam_time_slot_id bigint PRIMARY KEY,
    exam_date date NOT NULL,
    time_slot integer NOT NULL,
    examinee_count integer NOT NULL DEFAULT 0,
    created_at timestamp NOT NULL
);
