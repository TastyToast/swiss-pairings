-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament;

-- Players Table
CREATE TABLE players (
  name varchar(40),
  id SERIAL PRIMARY KEY
);

-- Matches Table
CREATE TABLE matches (
  player1 INTEGER REFERENCES players(id),
  player2 INTEGER REFERENCES players(id),
  winner INTEGER NULL REFERENCES players(id),
  PRIMARY KEY (player1, player2) -- Ensure that players are only matched once
);

-- Wins View. Shows the number of wins for each Player
CREATE VIEW wins AS
  SELECT players.id as winner, COUNT(matches.winner) as matches_won
  FROM players LEFT JOIN matches
  ON players.id = matches.winner
  GROUP BY players.id;

-- Match_Count View. Shows the number of matches for each player.
CREATE VIEW match_count AS
  SELECT players.id AS player, COUNT(player1) as num_matches
  FROM players LEFT JOIN matches
  ON players.id = player1 OR players.id = player2
  GROUP BY players.id;

-- Standings View. Shows the standings for each player
CREATE VIEW standings AS
  SELECT winner as id,
    players.name,
    wins.matches_won as wins,
    match_count.num_matches as matches
  FROM wins
    JOIN players ON winner = players.id
    JOIN match_count ON winner = match_count.player
  ORDER BY wins DESC;
