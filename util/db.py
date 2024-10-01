import pyodbc, struct
import json
import os

from dotenv import load_dotenv


load_dotenv()

server= "bmc-game.database.windows.net"
database = "bmc"

connection_string = os.environ["AZURE_SQL_CONNECTIONSTRING"]

def connect_to_db():
    try:
        connection = pyodbc.connect(connection_string)
        return connection
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        return None

def upload_bmc(bmc_data):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()

            # Pakk hele BMC-innholdet under selskapets navn
            company_name = bmc_data.pop('company_name')
            bmc_json_data = json.dumps(bmc_data)  # Konverter til JSON-streng

            # Sett inn JSON i Azure SQL
            insert_query = """
                INSERT INTO bmc_data (company_name, bmc)
                VALUES (?, ?)
            """
            
            cursor.execute(insert_query, (company_name, bmc_json_data))
            connection.commit()
            print(f"Data for {company_name} uploaded successfully.")
        except Exception as e:
            print(f"Error uploading data: {str(e)}")
        finally:
            cursor.close()
            connection.close()


def get_bmc(company_name):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()

            # Søk etter JSON-data basert på company_name
            select_query = "SELECT bmc FROM bmc_data WHERE company_name = ?"
            cursor.execute(select_query, (company_name,))
            
            result = cursor.fetchone()
            if result:
                # Pakk ut JSON-dataen og sett selskapets navn som øverste nøkkel
                bmc_data = json.loads(result[0])  # Konverter JSON-streng til Python-objekt
                return {company_name: bmc_data}
            else:
                print(f"No data found for {company_name}.")
                return None
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
        finally:
            cursor.close()
            connection.close()

def get_all_company_names():
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()

            # Søk etter alle selskapene
            select_query = "SELECT company_name FROM bmc_data"
            cursor.execute(select_query)
            
            result = cursor.fetchall()
            if result:
                # Returner en liste med alle selskapsnavn
                return [row[0] for row in result]
            else:
                print("No company names found.")
                return []
        except Exception as e:
            print(f"Error fetching company names: {str(e)}")
            return []
        finally:
            cursor.close()
            connection.close()

