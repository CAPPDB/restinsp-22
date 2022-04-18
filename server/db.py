from os import path
import logging # Logging Library
from errors import KeyNotFound, BadRequest, InspError

# Utility factor to allow results to be used like a dictionary
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# helper function that converts query result to json list, after cursor has executed a query
# this will not work for all endpoints directly, just the ones where you can translate
# a single query to the required json.


def to_json_list(cursor):
    results = cursor.fetchall()
    headers = [d[0] for d in cursor.description]
    return [dict(zip(headers, row)) for row in results]


"""
Wraps a single connection to the database with higher-level functionality.
"""


class DB:
    def __init__(self, connection):
        self.conn = connection

    def execute_script(self, script_file):
        with open(script_file, "r") as script:
            c = self.conn.cursor()
            # Only using executescript for running a series of SQL commands.
            c.executescript(script.read())
            self.conn.commit()

    def create_script(self):
        """
        Calls the schema/create.sql file
        """
        script_file = path.join("schema", "create.sql")
        if not path.exists(script_file):
            raise InspError("Create Script not found")
        self.execute_script(script_file)

    def seed_data(self):
        """
        Calls the schema/seed.sql file
        """
        script_file = path.join("schema", "seed.sql")
        if not path.exists(script_file):
            raise InspError("Seed Script not found")
        self.execute_script(script_file)


    def find_restaurant(self, restaurant_id):
        """
        Searches for the restaurant with the given ID. Returns None if the
        restaurant cannot be found in the database.
        """
        if not restaurant_id:
            raise InspError("No Restaurant Id", 404)
        # TODO milestone 1
        return None

    def find_inspection(self, inspection_id):
        if not inspection_id:
            raise InspError("No inspection_id", 404)
        """
        Searches for the inspection with the given ID. Returns None if the
        inspection cannot be found in the database.
        """
        # TODO milestone 1
        return None

    def find_inspections(self, restaurant_id):
        """
        Searches for all inspections associated with the given restaurant.
        Returns an empty list if no matching inspections are found.
        """
        if not restaurant_id:
            raise InspError("No Restaurant Id", 404)
        # TODO milestone 1
        return []

    def add_inspection_for_restaurant(self, inspection, restaurant):
        """
        Finds or creates the restaurant then inserts the inspection and
        associates it with the restaurant.
        """
        # TODO milestone 1
        return None

    # Simple example of how to execute a query against the DB.
    # Again NEVER do this, you should only execute parameterized query
    # See https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.execute
    # This is the qmark style:
    # cur.execute("insert into people values (?, ?)", (who, age))
    # And this is the named style:
    # cur.execute("select * from people where name_last=:who and age=:age", {"who": who, "age": age})
    def run_query(self, query):
        c = self.conn.cursor()
        c.execute(query)
        res =to_json_list(c)
        self.conn.commit()
        return res
