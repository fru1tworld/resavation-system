CREATE TABLE IF NOT EXISTS "user" (
    user_id bigint PRIMARY KEY,
    password varchar(80) NOT NULL,
    name varchar(50) UNIQUE NOT NULL,
    role varchar(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS test_categorie (
    id bigint PRIMARY KEY,
    name varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS test_info (
    id bigint PRIMARY KEY,
    name varchar(255) NOT NULL,
    description varchar(3000),
    category_id bigint
);

CREATE TABLE IF NOT EXISTS schedules (
    id bigint PRIMARY KEY,
    test_id bigint NOT NULL,
    start_time timestamp NOT NULL,
    end_time timestamp NOT NULL,
    max_capacity integer
);

CREATE TABLE IF NOT EXISTS reservations (
    id bigint PRIMARY KEY,
    user_id bigint NOT NULL,
    schedule_id bigint NOT NULL,
    status varchar(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS reservation_log (
    id bigint PRIMARY KEY,
    reservation_id bigint NOT NULL,
    action varchar(20) NOT NULL,
    timestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    performed_by bigint NOT NULL
);
