import requests
import json
import sys
import csv
import os

# Get Resource Summary
def get_resource_summary(subscription_id, subscription_name, header):
    # Get Resources details for Subscription
    get_resources_summary_details = requests.get(url = "https://management.azure.com/subscriptions/"+subscription_id+"/resources?api-version=2021-04-01", headers = header)
    resource_summary_response_to_json = get_resources_summary_details.json()
    if get_resources_summary_details.status_code == 200 or get_resources_summary_details.status_code == 204:
        if "value" in resource_summary_response_to_json:
            resource_type_excel_header = ['Subscription', 'Resource Type', 'Number of Resources']
            resource_type_sql_header = ['sub', 'type', 'num']
            with open('Resources Type Summary.csv', mode='w', newline='') as resource_type_excel_file_header:
                csvwriter = csv.writer(resource_type_excel_file_header, delimiter=',')
                csvwriter.writerow(resource_type_excel_header)
            with open('sql_resource_type_summary.csv', mode='w', newline='') as resource_type_sql_file_header:
                csvwriter = csv.writer(resource_type_sql_file_header, delimiter=',')
                csvwriter.writerow(resource_type_sql_header)
            list_of_resource_types = []
            for resource_types in resource_summary_response_to_json["value"]:
                resource_type = resource_types["type"]
                list_of_resource_types.append(resource_type)
            count_of_resource_types = dict((i, list_of_resource_types.count(i)) for i in list_of_resource_types)
            print("Writing Resource Type Summary Details to CSV")
            for key,value in count_of_resource_types.items():
                resource_type_generic_data = [subscription_name,key,value]
                with open('Resources Type Summary.csv', mode='a', newline='') as resource_excel_file_data:
                    csvwriter = csv.writer(resource_excel_file_data, delimiter=',')
                    csvwriter.writerow(resource_type_generic_data)
                with open('sql_resource_type_summary.csv', mode='a', newline='') as resource_sql_file_data:
                    csvwriter = csv.writer(resource_sql_file_data, delimiter=',')
                    csvwriter.writerow(resource_type_generic_data)
        else:
            print("No resources found. Skipping")
    else:
        print("Failed to get response. Please check the error")
