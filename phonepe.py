# Required Packages
import streamlit as st
import os
import json
import pandas as pd
import plotly.express as px 
import requests
import mysql.connector

# Aggregate Transactions
path_1="C:/project/Phone_Pe/pulse/data/aggregated/transaction/country/india/state/"
aggre_trans_list = os.listdir(path_1)

column_1={"States":[], "Years":[], "Quarter":[], "Transaction_type":[], "Transaction_count":[], "Transaction_amount":[]}

for state in aggre_trans_list:
    present_states=path_1+state+"/"
    aggre_year_list=os.listdir(present_states)
    
    for year in aggre_year_list:
        present_year=present_states+year+"/"
        aggre_file_list=os.listdir(present_year)
        
        for file in aggre_file_list:
            present_file=present_year+file
            data=open(present_file, "r")
            S=json.load(data)

            for i in S["data"]["transactionData"]:
                name=i["name"]
                count=i["paymentInstruments"][0]["count"]
                amount=i["paymentInstruments"][0]["amount"]
                column_1["Transaction_type"].append(name)
                column_1["Transaction_count"].append(count)
                column_1["Transaction_amount"].append(amount)
                column_1["States"].append(state)
                column_1["Years"].append(year)
                column_1["Quarter"].append(int(file.strip(".json")))

aggre_transaction=pd.DataFrame(column_1)

aggre_transaction["States"] = aggre_transaction["States"].str.replace("andaman-&-nicobar-islands","Andaman and Nicobar")
aggre_transaction["States"] = aggre_transaction["States"].str.replace("-"," ")
aggre_transaction["States"] = aggre_transaction["States"].str.title()
aggre_transaction["States"] = aggre_transaction["States"].str.replace("dadra-&-nagar-haveli-&-daman-&-diu","Dadra and Nagar Haveli and Daman Diu")

print(f" Extracted rows: {len(aggre_transaction)}")
print(aggre_transaction.head())

# Aggregate Users
path_2="C:/project/Phone_Pe/pulse/data/aggregated/user/country/india/state/"
aggre_user_list = os.listdir(path_2)

column_2 = {"States":[], "Years":[], "Quarter":[], "Brands":[], "Transaction_count":[], "Percentage":[]}

for state in aggre_user_list:
    present_states = path_2+state+"/"
    aggre_year_list = os.listdir(present_states)
    
    for year in aggre_year_list:
        present_year = present_states+year+"/"
        aggre_file_list = os.listdir(present_year)
        
        for file in aggre_file_list:
            present_file = present_year+file
            data = open(present_file, "r")
            U = json.load(data)
            
            try:
                for i in U["data"]["usersByDevice"]:
                    brand = i["brand"]
                    count =i["count"]
                    percentage = i["percentage"]
                    column_2["Brands"].append(brand)
                    column_2["Transaction_count"].append(count)
                    column_2["Percentage"].append(percentage)
                    column_2["States"].append(state)
                    column_2["Years"].append(year)
                    column_2["Quarter"].append(int(file.strip(".json")))
            except:
                pass

aggre_user=pd.DataFrame(column_2)

aggre_user["States"] = aggre_user["States"].str.replace("andaman-&-nicobar-islands","Andaman and Nicobar")
aggre_user["States"] = aggre_user["States"].str.replace("-"," ")
aggre_user["States"] = aggre_user["States"].str.title()
aggre_user["States"] = aggre_user["States"].str.replace("dadra-&-nagar-haveli-&-daman-&-diu","Dadra and Nagar Haveli and Daman Diu")

print(f" Extracted rows: {len(aggre_user)}")
print(aggre_user.head())

# Map Transaction
path_3="C:/project/Phone_Pe/pulse/data/map/transaction/hover/country/india/state/"
map_trans_list = os.listdir(path_3)

column_3 = {"States":[], "Years":[], "Quarter":[], "Districts":[], "Transaction_count":[], "Transaction_amount":[]}

for state in map_trans_list:
    present_states = path_3+state+"/"
    map_year_list = os.listdir(present_states)
    
    for year in map_year_list:
        present_year = present_states+year+"/"
        map_file_list = os.listdir(present_year)
        
        for file in map_file_list:
            present_file = present_year+file
            data = open(present_file, "r")
            D = json.load(data)
            
            for i in D["data"]["hoverDataList"]:
                name = i["name"]
                count = i["metric"][0]["count"]
                amount = i["metric"][0]["amount"]
                column_3["Districts"].append(name)
                column_3["Transaction_count"].append(count)
                column_3["Transaction_amount"].append(amount)
                column_3["States"].append(state)
                column_3["Years"].append(year)
                column_3["Quarter"].append(int(file.strip(".json")))

map_transaction=pd.DataFrame(column_3)

map_transaction["States"] = map_transaction["States"].str.replace("andaman-&-nicobar-islands","Andaman and Nicobar")
map_transaction["States"] = map_transaction["States"].str.replace("-"," ")
map_transaction["States"] = map_transaction["States"].str.title()
map_transaction["States"] = map_transaction["States"].str.replace("dadra-&-nagar-haveli-&-daman-&-diu","Dadra and Nagar Haveli and Daman Diu")

print(f" Extracted rows: {len(map_transaction)}")
print(map_transaction.head())

# Map User
path_4="C:/project/Phone_Pe/pulse/data/map/user/hover/country/india/state/"
map_user_list = os.listdir(path_4)

column_4 = {"States":[], "Years":[], "Quarter":[], "Districts":[], "RegisteredUser":[], "AppOpens":[]}

for state in map_user_list:
    present_states = path_4+state+"/"
    map_year_list = os.listdir(present_states)
    
    for year in map_year_list:
        present_year = present_states+year+"/"
        map_file_list = os.listdir(present_year)
        
        for file in map_file_list:
            present_file=present_year+file
            data=open(present_file, "r")
            H = json.load(data)
            
            for i in H["data"]["hoverData"].items():
                district = i[0]
                registereduser = i[1]["registeredUsers"]
                appopens = i[1]["appOpens"]
                column_4["Districts"].append(district)
                column_4["RegisteredUser"].append(registereduser)
                column_4["AppOpens"].append(appopens)
                column_4["States"].append(state)
                column_4["Years"].append(year)
                column_4["Quarter"].append(int(file.strip(".json")))

map_user = pd.DataFrame(column_4)

map_user["States"] = map_user["States"].str.replace("andaman-&-nicobar-islands","Andaman and Nicobar")
map_user["States"] = map_user["States"].str.replace("-"," ")
map_user["States"] = map_user["States"].str.title()
map_user["States"] = map_user["States"].str.replace("dadra-&-nagar-haveli-&-daman-&-diu","Dadra and Nagar Haveli and Daman Diu")

print(f" Extracted rows: {len(map_user)}")
print(map_user.head())

# Top Transactions
path_5="C:/project/Phone_Pe/pulse/data/top/transaction/country/india/state/"
top_trans_list = os.listdir(path_5)

column_5 = {"States":[], "Years":[], "Quarter":[], "Pincodes":[], "Transaction_count":[], "Transaction_amount":[]}

for state in top_trans_list:
    present_states = path_5+state+"/"
    top_year_list = os.listdir(present_states)
       
    for year in top_year_list:
        present_year = present_states+year+"/"
        top_file_list = os.listdir(present_year)
                
        for file in top_file_list:
            present_file = present_year+file
            data = open(present_file, "r")
            A = json.load(data)
            
            for i in A["data"]["pincodes"]:
                entityName = i["entityName"]
                count = i["metric"]["count"]
                amount = i["metric"]["amount"]
                column_5["Pincodes"].append(entityName)
                column_5["Transaction_count"].append(count)
                column_5["Transaction_amount"].append(amount)
                column_5["States"].append(state)
                column_5["Years"].append(year)
                column_5["Quarter"].append(int(file.strip(".json")))

top_transaction = pd.DataFrame(column_5)

top_transaction["States"] = top_transaction["States"].str.replace("andaman-&-nicobar-islands","Andaman and Nicobar")
top_transaction["States"] = top_transaction["States"].str.replace("-"," ")
top_transaction["States"] = top_transaction["States"].str.title()
top_transaction["States"] = top_transaction["States"].str.replace("dadra-&-nagar-haveli-&-daman-&-diu","Dadra and Nagar Haveli and Daman Diu")

print(f" Extracted rows: {len(top_transaction)}")
print(top_transaction.head())

# Top User
path_6 = "C:/project/Phone_Pe/pulse/data/top/user/country/india/state/"
top_user_list = os.listdir(path_6)

column_6 = {"States":[], "Years":[], "Quarter":[], "Pincodes":[], "RegisteredUser":[]}

for state in top_user_list:
    present_states = path_6+state+"/"
    top_year_list = os.listdir(present_states)

    for year in top_year_list:
        present_year = present_states+year+"/"
        top_file_list = os.listdir(present_year)

        for file in top_file_list:
            present_file = present_year+file
            data = open(present_file,"r")
            K = json.load(data)

            for i in K["data"]["pincodes"]:
                name = i["name"]
                registereduser = i["registeredUsers"]
                column_6["Pincodes"].append(str(name))
                column_6["RegisteredUser"].append(registereduser)
                column_6["States"].append(state)
                column_6["Years"].append(year)
                column_6["Quarter"].append(int(file.strip(".json")))

top_user = pd.DataFrame(column_6)

top_user["States"] = top_user["States"].str.replace("andaman-&-nicobar-islands","Andaman and Nicobar")
top_user["States"] = top_user["States"].str.replace("-"," ")
top_user["States"] = top_user["States"].str.title()
top_user["States"] = top_user["States"].str.replace("dadra-&-nagar-haveli-&-daman-&-diu","Dadra and Nagar Haveli and Daman Diu")

print(f" Extracted rows: {len(top_user)}")
print(top_user.head())

# Define path to insurance data
path_aggre_insurance = "C:/project/Phone_Pe/pulse/data/aggregated/insurance/country/india/state/"

# Initialize column structure
column_aggre_insurance = {
    "States": [], "Years": [], "Quarter": [],
    "Insurance_type": [], "Total_count": [], "Total_amount": []
}

# Get list of state folders
aggre_insurance_list = os.listdir(path_aggre_insurance)

for state_raw in aggre_insurance_list:
    state_path = os.path.join(path_aggre_insurance, state_raw)
    if not os.path.isdir(state_path):
        continue

    state = state_raw.replace("andaman-&-nicobar-islands", "Andaman and Nicobar")\
                     .replace("dadra-&-nagar-haveli-&-daman-&-diu", "Dadra and Nagar Haveli and Daman Diu")\
                     .replace("-", " ")\
                     .title()

    year_list = os.listdir(state_path)
    for year in year_list:
        year_path = os.path.join(state_path, year)
        if not os.path.isdir(year_path):
            continue

        file_list = os.listdir(year_path)
        for file in file_list:
            file_path = os.path.join(year_path, file)

            try:
                with open(file_path, "r") as f:
                    data = json.load(f)

                transaction_data = data.get("data", {}).get("transactionData", [])
                for txn in transaction_data:
                    if txn.get("name") == "Insurance":
                        instruments = txn.get("paymentInstruments", [])
                        if isinstance(instruments, list) and len(instruments) > 0:
                            count = instruments[0].get("count", 0)
                            amount = instruments[0].get("amount", 0)

                            column_aggre_insurance["States"].append(state)
                            column_aggre_insurance["Years"].append(int(year))
                            column_aggre_insurance["Quarter"].append(int(file.strip(".json")))
                            column_aggre_insurance["Insurance_type"].append("Total")
                            column_aggre_insurance["Total_count"].append(count)
                            column_aggre_insurance["Total_amount"].append(amount)

            except Exception as e:
                print(f"Error processing file: {file_path} — {e}")

aggre_insurance = pd.DataFrame(column_aggre_insurance)

print(f"Extracted rows: {len(aggre_insurance)}")
print(aggre_insurance.head())

# Map Insurance
path_map_insurance = "C:/project/Phone_Pe/pulse/data/map/insurance/hover/country/india/state/"
map_insurance_list = os.listdir(path_map_insurance)

column_map_insurance = {"States": [], "Years": [], "Quarter": [], "Districts": [], 
                        "Transaction_count": [], "Transaction_amount": []}

for state in map_insurance_list:
    present_states = path_map_insurance + state + "/"
    map_insurance_year_list = os.listdir(present_states)

    for year in map_insurance_year_list:
        present_year = present_states + year + "/"
        map_insurance_file_list = os.listdir(present_year)

        for file in map_insurance_file_list:
            present_file = present_year + file
            try:
                data = open(present_file, "r")
                file_contents = data.read()
                if not file_contents:
                    continue

                MI = json.loads(file_contents)
                hover_data_list = MI.get("data", {}).get("hoverDataList")

                if hover_data_list:
                    for item in hover_data_list:
                        district = item.get("name")
                        metric = item.get("metric")

                        if metric and len(metric) > 0:
                            count = metric[0].get("count", 0)
                            amount = metric[0].get("amount", 0)

                            column_map_insurance["Districts"].append(district)
                            column_map_insurance["Transaction_count"].append(count)
                            column_map_insurance["Transaction_amount"].append(amount)
                            column_map_insurance["States"].append(state)
                            column_map_insurance["Years"].append(year)
                            column_map_insurance["Quarter"].append(int(file.strip(".json")))

            except Exception as e:
                print(f"Error processing {present_file}: {e}")

map_insurance = pd.DataFrame(column_map_insurance)

if not map_insurance.empty:
    map_insurance["States"] = map_insurance["States"].str.replace("andaman-&-nicobar-islands", "Andaman and Nicobar")
    map_insurance["States"] = map_insurance["States"].str.replace("-", " ")
    map_insurance["States"] = map_insurance["States"].str.title()
    map_insurance["States"] = map_insurance["States"].str.replace("dadra-&-nagar-haveli-&-daman-&-diu", "Dadra and Nagar Haveli and Daman Diu")

print(f" Extracted rows: {len(map_insurance)}")
print(map_insurance.head())

# Top Insurance
path_top_insurance = "C:/project/Phone_Pe/pulse/data/top/insurance/country/india/state/"
top_insurance_list = os.listdir(path_top_insurance)

column_top_insurance = {"States": [], "Years": [], "Quarter": [], "Pincodes": [],
                        "Transaction_count": [], "Transaction_amount": []}

for state in top_insurance_list:
    present_states = path_top_insurance + state + "/"
    top_insurance_year_list = os.listdir(present_states)

    for year in top_insurance_year_list:
        present_year = present_states + year + "/"
        top_insurance_file_list = os.listdir(present_year)

        for file in top_insurance_file_list:
            present_file = present_year + file
            try:
                data = open(present_file, "r")
                file_contents = data.read()
                if not file_contents:
                    continue

                TI = json.loads(file_contents)
                pincode_data = TI.get("data", {}).get("pincodes")
                
                if pincode_data:
                    for i in pincode_data:
                        pincode = i.get("entityName")
                        count = i.get("metric", {}).get("count", 0)
                        amount = i.get("metric", {}).get("amount", 0)
                        
                        column_top_insurance["Pincodes"].append(pincode)
                        column_top_insurance["Transaction_count"].append(count)
                        column_top_insurance["Transaction_amount"].append(amount)
                        column_top_insurance["States"].append(state)
                        column_top_insurance["Years"].append(year)
                        column_top_insurance["Quarter"].append(int(file.strip(".json")))

            except Exception as e:
                print(f"Error processing {present_file}: {e}")

top_insurance = pd.DataFrame(column_top_insurance)

if not top_insurance.empty:
    top_insurance["States"] = top_insurance["States"].str.replace("andaman-&-nicobar-islands", "Andaman and Nicobar")
    top_insurance["States"] = top_insurance["States"].str.replace("-", " ")
    top_insurance["States"] = top_insurance["States"].str.title()
    top_insurance["States"] = top_insurance["States"].str.replace("dadra-&-nagar-haveli-&-daman-&-diu", "Dadra and Nagar Haveli and Daman Diu")

print(f" Extracted rows: {len(top_insurance)}")
print(top_insurance.head())

# DATABASE INSERTION - COMPLETELY FIXED VERSION
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="phonepe_user",
    password="harish@21",
    database="phonepe_db",
    auth_plugin='mysql_native_password'
)

cursor = mydb.cursor()

# DEBUG: Check current table structure first
print("\n=== DEBUG: CHECKING EXISTING TABLE STRUCTURES ===")
cursor.execute("SHOW TABLES")
existing_tables = cursor.fetchall()
print("Existing tables:", [table[0] for table in existing_tables])

for table in existing_tables:
    table_name = table[0]
    try:
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        print(f"\nTable: {table_name}")
        for col in columns:
            print(f"  Column: {col[0]} | Type: {col[1]}")
    except Exception as e:
        print(f"  Could not describe {table_name}: {e}")

# DROP ALL EXISTING TABLES TO AVOID COLUMN CONFLICTS
print("\n=== DROPPING EXISTING TABLES ===")
tables_to_drop = [
    'aggregated_transaction', 'map_transaction', 'aggregate_user', 
    'map_user', 'top_user', 'aggregated_insurance', 'map_insurance', 'top_insurance'
]

for table in tables_to_drop:
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
        print(f"✅ Dropped table: {table}")
    except Exception as e:
        print(f"⚠️ Could not drop {table}: {e}")

mydb.commit()

# CREATE ALL TABLES WITH CORRECT COLUMN NAMES
print("\n=== CREATING NEW TABLES ===")

# 1. Aggregated Transaction Table
create_query1 = '''CREATE TABLE aggregated_transaction (
                   States VARCHAR(100),
                   Years INT,
                   Quarter INT,
                   Transaction_type VARCHAR(100),
                   Transaction_count BIGINT,
                   Transaction_amount BIGINT
                   )'''
cursor.execute(create_query1)
print("✅ Created aggregated_transaction table")

# Insert data
for index, row in aggre_transaction.iterrows():
    insert_query1 = '''INSERT INTO aggregated_transaction 
                      (States, Years, Quarter, Transaction_type, Transaction_count, Transaction_amount)
                      VALUES (%s, %s, %s, %s, %s, %s)'''
    values = (row["States"], row["Years"], row["Quarter"], row["Transaction_type"], 
              row["Transaction_count"], row["Transaction_amount"])
    cursor.execute(insert_query1, values)
mydb.commit()
print("✅ Inserted data into aggregated_transaction")

# 2. Map Transaction Table
create_query2 = '''CREATE TABLE map_transaction (
                   States VARCHAR(100),
                   Years INT,
                   Quarter INT,
                   Districts VARCHAR(100),
                   Transaction_count BIGINT,
                   Transaction_amount BIGINT
                   )'''
cursor.execute(create_query2)
print("✅ Created map_transaction table")

# Insert data
for index, row in map_transaction.iterrows():
    insert_query2 = '''INSERT INTO map_transaction 
                      (States, Years, Quarter, Districts, Transaction_count, Transaction_amount)
                      VALUES (%s, %s, %s, %s, %s, %s)'''
    values = (row["States"], row["Years"], row["Quarter"], row["Districts"], 
              row["Transaction_count"], row["Transaction_amount"])
    cursor.execute(insert_query2, values)
mydb.commit()
print("✅ Inserted data into map_transaction")

# 3. Aggregate User Table
create_query3 = '''CREATE TABLE aggregate_user (
                   States VARCHAR(100),
                   Years INT,
                   Quarter INT,
                   Brands VARCHAR(100),
                   Transaction_count BIGINT,
                   Percentage FLOAT
                   )'''
cursor.execute(create_query3)
print("✅ Created aggregate_user table")

# Insert data
for index, row in aggre_user.iterrows():
    insert_query3 = '''INSERT INTO aggregate_user 
                      (States, Years, Quarter, Brands, Transaction_count, Percentage)
                      VALUES (%s, %s, %s, %s, %s, %s)'''
    values = (row["States"], row["Years"], row["Quarter"], row["Brands"], 
              row["Transaction_count"], row["Percentage"])
    cursor.execute(insert_query3, values)
mydb.commit()
print("✅ Inserted data into aggregate_user")

# 4. Map User Table
create_query4 = '''CREATE TABLE map_user (
                   States VARCHAR(100),
                   Years INT,
                   Quarter INT,
                   Districts VARCHAR(100),
                   RegisteredUser BIGINT,
                   AppOpens BIGINT
                   )'''
cursor.execute(create_query4)
print("✅ Created map_user table")

# Insert data
for index, row in map_user.iterrows():
    insert_query4 = '''INSERT INTO map_user 
                      (States, Years, Quarter, Districts, RegisteredUser, AppOpens)
                      VALUES (%s, %s, %s, %s, %s, %s)'''
    values = (row["States"], row["Years"], row["Quarter"], row["Districts"], 
              row["RegisteredUser"], row["AppOpens"])
    cursor.execute(insert_query4, values)
mydb.commit()
print("✅ Inserted data into map_user")

# 5. Top User Table
create_query5 = '''CREATE TABLE top_user (
                   States VARCHAR(100),
                   Years INT,
                   Quarter INT,
                   Pincodes VARCHAR(20),
                   RegisteredUser BIGINT
                   )'''
cursor.execute(create_query5)
print("✅ Created top_user table")

# Insert data
for index, row in top_user.iterrows():
    insert_query5 = '''INSERT INTO top_user 
                      (States, Years, Quarter, Pincodes, RegisteredUser)
                      VALUES (%s, %s, %s, %s, %s)'''
    values = (row["States"], row["Years"], row["Quarter"], str(row["Pincodes"]), row["RegisteredUser"])
    cursor.execute(insert_query5, values)
mydb.commit()
print("✅ Inserted data into top_user")

# 6. Aggregated Insurance Table
create_query6 = '''CREATE TABLE aggregated_insurance (
                   States VARCHAR(100),
                   Years INT,
                   Quarter INT,
                   Insurance_type VARCHAR(255),
                   Total_count BIGINT,
                   Total_amount BIGINT
                   )'''
cursor.execute(create_query6)
print("✅ Created aggregated_insurance table")

# Insert data
if not aggre_insurance.empty:
    for index, row in aggre_insurance.iterrows():
        insert_query6 = '''INSERT INTO aggregated_insurance 
                          (States, Years, Quarter, Insurance_type, Total_count, Total_amount)
                          VALUES (%s, %s, %s, %s, %s, %s)'''
        values = (row["States"], row["Years"], row["Quarter"], row["Insurance_type"], 
                  row["Total_count"], row["Total_amount"])
        cursor.execute(insert_query6, values)
    mydb.commit()
    print("✅ Inserted data into aggregated_insurance")
else:
    print("⚠️ No data for aggregated_insurance")

# 7. Map Insurance Table
create_query7 = '''CREATE TABLE map_insurance (
                   States VARCHAR(100),
                   Years INT,
                   Quarter INT,
                   Districts VARCHAR(100),
                   Transaction_count BIGINT,
                   Transaction_amount BIGINT
                   )'''
cursor.execute(create_query7)
print("✅ Created map_insurance table")

# Insert data
if not map_insurance.empty:
    for index, row in map_insurance.iterrows():
        insert_query7 = '''INSERT INTO map_insurance 
                          (States, Years, Quarter, Districts, Transaction_count, Transaction_amount)
                          VALUES (%s, %s, %s, %s, %s, %s)'''
        values = (row["States"], row["Years"], row["Quarter"], row["Districts"], 
                  row["Transaction_count"], row["Transaction_amount"])
        cursor.execute(insert_query7, values)
    mydb.commit()
    print("✅ Inserted data into map_insurance")
else:
    print("⚠️ No data for map_insurance")

# 8. Top Insurance Table
create_query8 = '''CREATE TABLE top_insurance (
                   States VARCHAR(100),
                   Years INT,
                   Quarter INT,
                   Pincodes VARCHAR(20),
                   Transaction_count BIGINT,
                   Transaction_amount BIGINT
                   )'''
cursor.execute(create_query8)
print("✅ Created top_insurance table")

# Insert data
if not top_insurance.empty:
    for index, row in top_insurance.iterrows():
        insert_query8 = '''INSERT INTO top_insurance 
                          (States, Years, Quarter, Pincodes, Transaction_count, Transaction_amount)
                          VALUES (%s, %s, %s, %s, %s, %s)'''
        values = (row["States"], row["Years"], row["Quarter"], row["Pincodes"], 
                  row["Transaction_count"], row["Transaction_amount"])
        cursor.execute(insert_query8, values)
    mydb.commit()
    print("✅ Inserted data into top_insurance")
else:
    print("⚠️ No data for top_insurance")

print("\n🎉 ALL TABLES CREATED AND DATA INSERTED SUCCESSFULLY!")

# Final verification
print("\n=== FINAL VERIFICATION ===")
cursor.execute("SHOW TABLES")
final_tables = cursor.fetchall()
print("Final tables in database:", [table[0] for table in final_tables])

cursor.close()
mydb.close()