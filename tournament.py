#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Failed to connect the the database {}".format(database_name))


def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()
    query = "DELETE FROM matches;"
    cursor.execute(query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    query = "DELETE FROM players;"
    cursor.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
    query = "SELECT count(*) FROM players;"
    cursor.execute(query);
    players = [int(row[0]) for row in cursor.fetchall()][0];
    db.close()
    return players


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()
    query = "INSERT INTO players VALUES(%s);"
    param = (name,)
    cursor.execute(query, param)
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, cursor = connect()
    query = "SELECT id, name, wins, matches FROM standings ORDER BY wins DESC;"
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return results

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()
    query = "INSERT INTO matches (player1, player2, winner) VALUES (%s, %s, %s);"
    param = (winner, loser, winner,)
    cursor.execute(query, param)
    db.commit()
    db.close()

def getMatches():
    """ Returns a list of matches played """
    db, cursor = connect()
    query = "SELECT player1, player2 FROM matches;"
    cursor.execute(query)
    matches = cursor.fetchall()
    db.close()
    return matches

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

    # Get matches played
    matches = set(getMatches())

    # Get standings
    standings = playerStandings()

    results = []
    while standings:
        player1 = standings.pop(0)
        id1, name1 = player1[0], player1[1]
        for i in range(len(standings)):
            player2 = standings[i]
            id2, name2 = player2[0], player2[1]
            if set([id1, id2]) not in matches:
                standings.pop(i)
                results.append((id1, name1, id2, name2))
                break
    return results
