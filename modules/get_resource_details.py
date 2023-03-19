import requests
import json
import sys
import csv
import os

# Get Resource Details
def get_resource(subscription_id, subscription_name, header):
    # Get Resource Group details for Subscription
    get_rg_details = requests.get(url = "https://management.azure.com/subscriptions/"+subscription_id+"/resourcegroups?api-version=2021-04-01", headers = header)
    rg_response_to_json = get_rg_details.json()
    if get_rg_details.status_code == 200 or get_rg_details.status_code == 204:
        resource_excel_header = ['Subscription', 'Name', 'Location', 'Resource Group', 'Resource Type', 'Scope', 'Tags', 'Locks', 'Non Compliant Policy']
        resource_sql_header = ['sub', 'name', 'location', 'rg_name', 'type', 'scope', 'tags', 'locks', 'non_compliant_policy']
        with open('Resources.csv', mode='w', newline='') as resource_csv_file_header:
            csvwriter = csv.writer(resource_csv_file_header, delimiter=',')
            csvwriter.writerow(resource_excel_header)
        with open('sql_resource.csv', mode='w', newline='') as resource_sql_csv_file_header:
            csvwriter = csv.writer(resource_sql_csv_file_header, delimiter=',')
            csvwriter.writerow(resource_sql_header)
        for rg in rg_response_to_json["value"]:
            print("Getting Resources details for Resource Group - ", rg["name"])
            get_resources_details = requests.get(url = "https://management.azure.com/"+rg["id"]+"/resources?api-version=2021-04-01", headers = header)
            resource_response_to_json = get_resources_details.json()
            if get_resources_details.status_code == 200 or get_resource_details.status_code == 204:
                for resource in resource_response_to_json["value"]:
                    # Get Resource Tags Details
                    if "tags" in resource:
                        all_tags = []
                        for key,value in resource["tags"].items():
                            tag_value = ""+key+"="+value+""
                            all_tags.append(tag_value)
                        tag_csv_value = '\n'.join(all_tags)
                        tag_sql_value = ','.join(all_tags)
                    else:
                        tag_csv_value = None
                        tag_sql_value = "No Tags"
                    # Get Resource Lock Details
                    get_resource_lock_details = requests.get(url = "https://management.azure.com/"+resource["id"]+"/providers/Microsoft.Authorization/locks?api-version=2016-09-01", headers = header)
                    get_resource_lock_resonse_to_json = get_resource_lock_details.json()
                    if get_resource_lock_details.status_code == 200 or get_resource_lock_details.status_code == 204:
                        if get_resource_lock_resonse_to_json["value"]:
                            all_locks = []
                            for lock in get_resource_lock_resonse_to_json["value"]:
                                lock_level = lock["properties"]["level"]
                                lock_name = lock["name"]
                                lock_scope = lock["id"]
                                lock_value = "Level="+lock_level+", Name="+lock_name+", Scope="+lock_scope+""
                                all_locks.append(lock_value)
                            lock_csv_value = '\n'.join(all_locks)
                            lock_sql_value = ','.join(all_locks)
                        else:
                            lock_csv_value = None
                            lock_sql_value = "No Locks"
                    else:
                        print("Unable to get Resource Locks Details. Please check error..")
                        lock_csv_value = ""+get_resource_lock_resonse_to_json["error"]["code"]+" - "+get_resource_lock_resonse_to_json["error"]["message"]+""
                        lock_sql_value = ""+get_resource_lock_resonse_to_json["error"]["code"]+" - "+get_resource_lock_resonse_to_json["error"]["message"]+""
                    
                    # Get Compliance Summary for Resources
                    get_summary = requests.post(url = "https://management.azure.com"+resource["id"]+"/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01", headers = header)
                    get_summary_to_json = get_summary.json()
                    if get_summary.status_code == 200 or get_summary.status_code == 204:
                        if "value" in get_summary_to_json:
                            non_compliant_policy = get_summary_to_json["value"][0]["results"]["nonCompliantPolicies"]
                        else:
                            non_compliant_policy = None
                    else:
                        non_compliant_policy = None

                    # Write to CSV
                    resource_excel_data = [subscription_name,resource["name"],resource["location"],rg["name"],resource["type"], resource["id"], tag_csv_value,lock_csv_value,non_compliant_policy]
                    resource_sql_data = [subscription_name,resource["name"],resource["location"],rg["name"],resource["type"], resource["id"], tag_sql_value,lock_sql_value,non_compliant_policy]
                    print("Writing Resource Details to CSV - ", resource["name"])
                    with open('Resources.csv', mode='a', newline='') as resource_excel_file_data:
                        csvwriter = csv.writer(resource_excel_file_data, delimiter=',')
                        csvwriter.writerow(resource_excel_data)
                    with open('sql_resource.csv', mode='a', newline='') as resource_sql_file_data:
                        csvwriter = csv.writer(resource_sql_file_data, delimiter=',')
                        csvwriter.writerow(resource_sql_data)
            else:
                print("Unable to get Resource details. Please check the error")
                print("Error is : "+resource_response_to_json["error"]["code"]+" - "+resource_response_to_json["error"]["message"]+"")
                os.remove('Resources.csv')
                os.remove('sql_resource.csv')
                sys.exit(1)
    else:
        print("Unable to get Resource details from Resource Group. Please check the error.")
        print("Error is : "+rg_response_to_json["error"]["code"]+" - "+rg_response_to_json["error"]["message"]+"")
        sys.exit(1)