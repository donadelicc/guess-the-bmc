# from util.postgres import connect_to_db, upload_bmc, get_bmc
from db import upload_bmc
import json
import random

with open('../data/bmc.json', 'r') as file:
    bmc_data = json.load(file)

# Laste opp hvert selskap fra bmc_data til PostgreSQL
for company_name, data in bmc_data.items():
    # Legg til company_name i data-ordboken, siden den skal også lagres
    data['company_name'] = company_name
    if company_name == "Blizzard":
        # Last opp data til databasen
        upload_bmc(data)

print("All BMC data has been uploaded successfully.")