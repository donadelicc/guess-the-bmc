import psycopg2
from dotenv import load_dotenv
import os
import json

load_dotenv()

password = os.getenv("POSTGRES_PASSWORD")
DB_PASSWORD = password.replace("@", "%40")
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME=  "bmc_db"
DB_TABLE = "bmc_data"

conn_info = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# sync_connection = psycopg.connect(conn_info)

def connect_to_db():
    try:
        connection = psycopg2.connect(conn_info)
        return connection
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        return None
    
    
# Funksjon for å laste opp BMC-data til PostgreSQL som JSON
def upload_bmc(bmc_data):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()

            # Pakk hele BMC-innholdet under selskapets navn
            company_name = bmc_data.pop('company_name')
            bmc_json_data = json.dumps(bmc_data)

            insert_query = sql.SQL("""
                INSERT INTO bmc_data (company_name, bmc)
                VALUES (%s, %s)
            """)
            
            cursor.execute(insert_query, (
                company_name,  # Sett inn 'company_name'
                bmc_json_data  # Lagre resten som JSON
            ))
            
            connection.commit()
            print(f"Data for {company_name} uploaded successfully.")
        except Exception as e:
            print(f"Error uploading data: {str(e)}")
        finally:
            cursor.close()
            connection.close()

# Funksjon for å hente BMC-data fra PostgreSQL
def get_bmc(company_name):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()

            # Søk etter JSON-data basert på company_name
            select_query = "SELECT bmc FROM bmc_data WHERE company_name = %s"
            cursor.execute(select_query, (company_name,))
            
            result = cursor.fetchone()
            if result:
                # Pakk ut JSON-dataen og sett selskapets navn som øverste nøkkel
                bmc_data = result[0]
                return {company_name: bmc_data}
            else:
                print(f"No data found for {company_name}.")
                return None
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
        finally:
            cursor.close()
            connection.close()
            
            
# Funksjon for å hente alle selskapsnavn fra PostgreSQL
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



# Last opp BMC-data til PostgreSQL
# upload_bmc(bmc_data2)

# # Hent data fra PostgreSQL
# company_data = get_bmc("Spotify")
# print(json.dumps(company_data))

# print(get_all_company_names())