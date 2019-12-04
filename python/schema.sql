CREATE DATABASE api_storage;

\connect api_storage;

CREATE TABLE gamesaves (
  "id" uuid PRIMARY KEY NOT NULL,
  "gamesave" TEXT NOT NULL
);
