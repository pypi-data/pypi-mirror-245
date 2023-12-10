import os
import sys

import pymysql
from dotenv import load_dotenv

load_dotenv()

# TODO: We should move this code to python-sdk/infrastructure repo. We should call our_python_init() which calls get_debug() as we might want to add things in the future
os_debug = os.getenv('DEBUG', "False")
debug = os_debug.lower() == 'true' or os_debug == '1'

if debug:
    print("Writer.py debug is on debug=", debug)


class Writer:
    # Since logger should not use our database package (to avoid cyclic dependency) we are using the database directly
    @staticmethod
    def get_connection() -> pymysql.connections.Connection:
        return pymysql.connect(
            host=os.getenv('RDS_HOSTNAME'),
            user=os.getenv('RDS_USERNAME'),
            password=os.getenv('RDS_PASSWORD'),

        )

    def add(self, **kwargs):
        connection = None
        try:
            params_to_insert = kwargs['object']
            # creating connection
            connection = self.get_connection()
            # connection = self._pool.get_connection()
            cursor = connection.cursor()

            try:
                if params_to_insert['latitude'] is None:
                    params_to_insert['latitude'] = 0
                if params_to_insert['longitude'] is None:
                    params_to_insert['longitude'] = 0
            except Exception:
                params_to_insert['latitude'] = 0
                params_to_insert['longitude'] = 0
            cursor.execute(
                f"insert into location.location_table (coordinate) "
                f"values (POINT({params_to_insert['latitude'] or 0},{params_to_insert['longitude'] or 0}));")
            coordinate_id = cursor.lastrowid

            params_to_insert.pop('latitude')
            params_to_insert.pop('longitude')

            params_to_insert['location_id'] = coordinate_id
            listed_values = list(params_to_insert.values())
            joined_keys = ','.join(list(params_to_insert.keys()))
            generate_values_pattern = ','.join(['%s'] * len(listed_values))
            sql = f"""INSERT INTO logger.logger_table ({joined_keys})
                        VALUES ({generate_values_pattern});
            """
            cursor.execute(sql, listed_values)
        except Exception as e:
            print("Exception caught " + str(e), file=sys.stderr)
        finally:
            connection.commit()
            cursor.close()
            connection.close()

    def add_message(self, message, log_level):
        if debug:
            print("add_message" + message + ' ' + str(log_level), file=sys.stderr)
        connection = None
        try:
            # creating connection
            connection = self.get_connection()
            # connection = self._pool.get_connection()
            cursor = connection.cursor()
            sql = f"INSERT INTO logger.logger_table (message, severity_id) VALUES ('{message}', {log_level})"
            cursor.execute(sql)
        except Exception as e:
            print("Exception Writer.py Writer.add_message caught" + str(e), file=sys.stderr)
        finally:
            if connection:
                connection.commit()
                cursor.close()
                connection.close()

    def addMessageAndPayload(self, message, **kwargs):
        connection = None
        try:
            connection = self.get_connection()
            params_to_insert = kwargs['object']
            # creating connection:
            # connection = self._pool.get_connection()
            cursor = connection.cursor()

            try:
                if params_to_insert['latitude'] is None:
                    params_to_insert['latitude'] = 0
                if params_to_insert['longitude'] is None:
                    params_to_insert['longitude'] = 0
            except Exception:
                params_to_insert['latitude'] = 0
                params_to_insert['longitude'] = 0
            cursor.execute(
                f"insert into location.location_table (coordinate) "
                f"values (POINT({params_to_insert['latitude'] or 0},{params_to_insert['longitude'] or 0}));")
            coordinate_id = cursor.lastrowid

            params_to_insert.pop('latitude')
            params_to_insert.pop('longitude')

            params_to_insert['location_id'] = coordinate_id
            listed_values = list(params_to_insert.values()) + [message]
            joined_keys = ','.join(list(params_to_insert.keys()) + ["message"])
            placeholders = ','.join(['%s'] * len(listed_values))
            sql = f"""INSERT INTO logger.logger_table ({joined_keys})
                        VALUES ({placeholders});"""
            cursor = connection.cursor()
            cursor.execute(sql, listed_values)
        except Exception as e:
            print("Exception caught " + str(e), file=sys.stderr)
        finally:
            if connection:
                connection.commit()
                cursor.close()
                connection.close()
