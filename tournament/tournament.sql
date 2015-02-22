-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Creating the table Player. This table holds Player details alnog with his standings in the tournment.
CREATE TABLE player (
	PlayerId SERIAL,
	Name varchar(100),
	Points smallint
);

--Adding Primary key to Player table
ALTER TABLE player 
ADD CONSTRAINT pk_player PRIMARY KEY (PlayerId);

--Creating the table Match. This table hold every match details such is winner, loser.
CREATE TABLE match (
	MatchId SERIAL,
	Winner int,
	Loser int
);

--Creting a primary key on Match table
ALTER TABLE match 
ADD CONSTRAINT pk_match PRIMARY KEY (MatchId);

--Creating a Foreign Key on Match table on the Column Winner which refrences PlayerID in Player table. This is to maintain refrential integrity.
ALTER TABLE match ADD CONSTRAINT fk_match_player_Winner 
FOREIGN KEY (Winner) REFERENCES player (PlayerId) MATCH FULL;

--Creating a Foreign Key on Match table on the Column Loser which refrences PlayerID in Player table. This is to maintain refrential integrity.
ALTER TABLE match ADD CONSTRAINT fk_match_player_Loser 
FOREIGN KEY (Loser) REFERENCES player (PlayerId) MATCH FULL;