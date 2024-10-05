import pyodbc
import json
import os

from dotenv import load_dotenv

load_dotenv()

server = os.environ["AZURE_SQL_SERVER"]
database = os.environ["AZURE_SQL_DATABASE"]

connection_string = os.environ["AZURE_SQL_CONNECTIONSTRING"]

def connect_to_db():
    try:
        connection = pyodbc.connect(connection_string)
        return connection
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        return None

def upload_bmc(bmc_data, connection):
    # connection = connect_to_db()
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
            # connection.close()

def get_bmc(connection):
    if connection:
        try:
            cursor = connection.cursor()

            # Select a random company and its BMC data in one query
            select_query = """
                SELECT company_name, bmc 
                FROM bmc_data 
                ORDER BY NEWID() 
                OFFSET 0 ROWS 
                FETCH NEXT 1 ROWS ONLY
            """
            cursor.execute(select_query)
            result = cursor.fetchone()
            
            if result:
                company_name = result[0]
                bmc_data = json.loads(result[1])  # Convert JSON string to Python object
                return {company_name: bmc_data}
            else:
                print("No data found.")
                return None
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
        finally:
            cursor.close()

def get_all_company_names(connection):
    # connection = connect_to_db()
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
            # connection.close()

