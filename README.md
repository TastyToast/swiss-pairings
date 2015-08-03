# Swiss Pairings Tournament
A swiss pairings tournament system

##Files
* tournament.py
* tournament.sql
* tournament_test.py

##Usage
Initialize the tournament database. You must have [PostgreSQL](http://www.postgresql.org/) installed.
```
vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ psql
psql (9.3.5)
Type "help" for help.

vagrant=> CREATE DATABASE tournament;
CREATE DATABASE
```
Then run
```
\i tournament.sql
```

Run the test
```
python tournament_test.py
```
