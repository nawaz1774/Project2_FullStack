"""This Module implements various functions that is used to Manage the swiss style Tournamnets.

This module contains various functions which helps in managing the data related to conducting a swiss style tounaments.
The backend Database Management system is postgress.
Below are the list functions available:
    connect: Returns a connection object for a postgress SQL datbase instance.
    deleteMatches: Remove all the match records from the database
    deletePlayers: Remove all the player records from the database
    countPlayers: Returns the number of players currently registered
    registerPlayer: Adds a player to the tournament database.
    playerStandings: Returns a list of the players and their win records, sorted by wins.
    reportMatch: Records the outcome of a single match between two players.
    swissPairings: Returns a list of pairs of players for the next round of a match.
"""
#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

#Creates a Connection object for a Postgresql Instance and rtuens it
def connect():
    """Connect to the PostgreSQL database.  Returns a database connection.
    Args:
        None
    Returns:
        Connection object for a Postgresql Instance
    """
    return psycopg2.connect("dbname=tournament")

#Deletes all the matches from the table match.
def deleteMatches():
    """Remove all the match records from the database.
    Args:
        None
    Returns:
        None
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM match;")
    conn.commit()
    conn.close()

#Deletes all the players from the table player.
def deletePlayers():
    """Remove all the player records from the database.
    Args:
        None
    Returns:
        None
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM player;")
    conn.commit()
    conn.close()

#Retunts the cont of players from player table
def countPlayers():
    """Returns the number of players currently registered.
    Args:
        None
    Returns:
        Returns the number of players registred for the tournament.
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(1) as c FROM player;")
    count = cur.fetchall()
    conn.close()
    return count[0][0]

#Registers a player to the tournament. Adds a new row in player table.
def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    Returns:
        None
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO player (Name, Points) VALUES(%s, 0)",(name,))
    conn.commit()
    conn.close()


#Returns the player standings. 
def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Args:
        None
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("\
                    SELECT PlayerID, Name, Points, \
                        (SELECT count(1) FROM match WHERE Winner = PlayerID or Loser = PlayerID) \
                        AS MatchesPlayed \
                    FROM player ORDER BY Points DESC, PlayerID ASC;\
                ")
    standings = cur.fetchall()

    return standings

#Records the match details. Such as Winner, Loser.
def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost

    Returns:
        None
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO match (Winner, Loser) VALUES(%s, %s);",(str(winner), str(loser)))
    cur.execute("UPDATE player SET Points = (Points + 1) WHERE PlayerID = %s;", (str(winner),))
    conn.commit()
    conn.close()
 
 
 #Returns a list of pairs of players for the next round of a match.
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT \
                    L.PlayerID, \
                    L.Name, \
                    R.PlayerID, \
                    R.Name \
                FROM \
                    (\
                        SELECT *, ROW_NUMBER() OVER(ORDER BY Points DESC, PlayerID) AS Rn \
                        FROM player \
                    ) L JOIN \
                    ( \
                        SELECT *, ROW_NUMBER() OVER(ORDER BY Points DESC, PlayerID) AS Rn \
                        FROM player \
                    ) R \
                    ON L.Rn = (R.Rn - 1) \
                WHERE  \
                    L.Rn % 2 != 0 " \
                )
    rows = cur.fetchall()
    return rows


