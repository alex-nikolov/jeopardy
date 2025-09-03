-- Create the database
CREATE DATABASE "Jeopardy";

-- Connect to the newly created database
\c "Jeopardy";

-- Create a table called 'questions'
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,                -- Unique identifier, auto-increment
    show_number INTEGER NOT NULL,         -- Show number
    air_date TIMESTAMP NOT NULL,          -- Air date
    round VARCHAR(32) NOT NULL,           -- Round, max 32 characters
    category VARCHAR(64) NOT NULL,        -- Category, max 64 characters
    value INTEGER,                        -- Value of the question
    question VARCHAR(256) NOT NULL,       -- Question text, max 256 characters
    answer VARCHAR(64) NOT NULL           -- Answer text, max 64 characters
);