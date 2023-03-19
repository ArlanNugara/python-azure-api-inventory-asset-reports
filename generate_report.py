import csv
import sys
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import load_workbook
from modules.generate_excel import create_excel

csv_file_map = ('Subscription', 'Resource Group', 'Resources', 'Resources Type Summary', 'Virtual Machines', 'Virtual Machine Data Disk', 'VM Network Interfaces', 'VM Metrics', 'Virtual Network', 'Subnet', 'Virtual Network Peering', 'Network Security Groups', 'Route Tables', 'Public IP Address', 'Storage Accounts', 'Storage Account Containers', 'Storage Account File Shares', 'Storage Account Tables', 'Storage Account Queue', 'Policy Assignments', 'Policy Assessments', 'Regulatory Compliance Standards', 'Regulatory Compliance Controls', 'Azure Advisor Recommendation', 'SQL Servers', 'SQL Databases', 'SQL Firewall Rules', 'SQL Vulnerability Assessments', 'SQL Vulnerability Assessments Scan', 'SQL Vulnerability Assessments Scan Results', 'SQLMI Servers', 'SQLMI Databases', 'Data Factory', 'Data Factory Dataset', 'Data Factory Pipeline', 'Active Key Vaults', 'Deleted Key Vaults', 'Load Balancer', 'LB Frontend Config', 'Application Gateway', 'Virtual Machine Scale Set', 'VMSS Virtual Machines')

try:
    print("Creating Excel Report")
    excel_writer = pd.ExcelWriter('reports.xlsx', engine='openpyxl')
    excel_header = pd.DataFrame(columns = ['Table of Content'])
    excel_header.to_excel(excel_writer, sheet_name='Table of Content', index=False)
    excel_writer.save()
    
    for files in csv_file_map:
        print("Creating Excel Sheet for ", files)
        create_excel(""+files+".csv",files)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)