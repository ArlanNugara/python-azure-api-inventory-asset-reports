import sys
import csv
import pyodbc
import os

sql_file_map = ("subscription", "resource_group", "resource", "resource_type_summary", "vm_general", "vm_data_disk", "vm_network_interfaces", "vm_metrics", "vn", "subnet", "peering", "nsg", "udr", "pip", "sa", "blob", "file_share", "tables", "queue", "policy_assignments", "policy_assessment", "rcs", "rcc", "aar", "sql_srv", "sql_dbs", "sql_fwr", "sql_va", "sql_vas", "sql_vasr", "sqlmi_srv", "sqlmi_dbs", "df", "dfds", "dfp", "kv_active", "kv_deleted", "lb", "lb_fip", "ag", "vmss", "vmss_vm")

# Login to Database
try:
    cgm_con = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER='+os.environ['DBSERVER']+';'
        'DATABASE='+os.environ['DB']+';'
        'Uid='+os.environ['USER']+';'
        'PWD='+os.environ['PASS']+';'
        'ENCRYPT=yes;')

    cursor = cgm_con.cursor()
    print("Conection Successful")
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Insert Data
try:
    for tables in sql_file_map:
        print("Starting SQL Inserts for - ", tables)
        with open ('sql_'+tables+'.csv', 'r') as f:
            reader = csv.reader(f)
            columns = next(reader) 
            query = 'insert into '+tables+'({0}) values ({1})'
            query = query.format(','.join(columns), ','.join('?' * len(columns)))
            for data in reader:
                cursor.execute(query, data)
            cursor.commit()
        print("SQL Insert Done for - ", tables)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Close Connection
cursor.close()
print("Cursor Closed")
cgm_con.close()
print("Connection Closed")