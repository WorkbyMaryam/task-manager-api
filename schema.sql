-- Users
CREATE TABLE users (
    id            INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username      VARCHAR(30)  NOT NULL UNIQUE,
    email         VARCHAR(255) NOT NULL UNIQUE,
    password_hash TEXT         NOT NULL,
    age           INTEGER      CHECK (age BETWEEN 13 AND 120),
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT now()
);

-- Tasks
CREATE TYPE task_priority AS ENUM ('low', 'medium', 'high');

CREATE TABLE tasks (
    id          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    owner_id    INTEGER       NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title       VARCHAR(100)  NOT NULL CHECK (length(trim(title)) > 0),
    description VARCHAR(500),
    priority    task_priority NOT NULL DEFAULT 'medium',
    completed   BOOLEAN       NOT NULL DEFAULT FALSE,
    created_at  TIMESTAMPTZ   NOT NULL DEFAULT now()
);

CREATE INDEX idx_tasks_owner_id ON tasks(owner_id);

-- Tags
CREATE TABLE tags (
    id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(30) NOT NULL UNIQUE
);

-- Join table (many-to-many)
CREATE TABLE task_tags (
    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    tag_id  INTEGER NOT NULL REFERENCES tags(id)  ON DELETE CASCADE,
    PRIMARY KEY (task_id, tag_id)
);

CREATE INDEX idx_task_tags_tag_id ON task_tags(tag_id);