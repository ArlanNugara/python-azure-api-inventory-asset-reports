import requests
import json
import sys
import csv
import os

# Get Resource Group Details
def get_rg(subscription_id, subscription_name, header):
    print("Getting Resource Groups Details for Subscription ID - "+subscription_id+"")
    get_rg_details = requests.get(url = "https://management.azure.com/subscriptions/"+subscription_id+"/resourcegroups?api-version=2021-04-01", headers = header)
    rg_response_to_json = get_rg_details.json()
    with open("rg.json", "w", encoding="utf-8") as rg_json:
        json.dump(rg_response_to_json, rg_json, ensure_ascii=False, indent=4)
    if get_rg_details.status_code == 200 or get_rg_details.status_code == 204:
        # Get CSV headers created
        rg_excel_header = ['Subscription', 'Name', 'Location', 'Provisioning Status', 'Scope', 'Tags', 'Locks', 'Total Resources', 'Unique Resource Location', 'Resource Locations', 'Current Billing Period Cost', 'Forecast Billing Period Cost', 'Non Compliant Resources', 'Non Compliant Policy']
        rg_sql_header = ['sub', 'name', 'location', 'provisioning_state', 'id', 'tags', 'locks', 'total_resource', 'unique_resource_loc', 'resource_loc', 'current_cost', 'forecast_cost', 'non_compliant_resources', 'non_compliant_policy']
        
        with open('Resource Group.csv', mode='w', newline='') as rg_csv_file_header:
            csvwriter = csv.writer(rg_csv_file_header, delimiter=',')
            csvwriter.writerow(rg_excel_header)
        with open('sql_resource_group.csv', mode='w', newline='') as rg_sql_file_header:
            csvwriter = csv.writer(rg_sql_file_header, delimiter=',')
            csvwriter.writerow(rg_sql_header)
        
        # Start formatting data
        if rg_response_to_json["value"]:
            rg_csv_value = []
            for rg in rg_response_to_json["value"]:
                # Get Tags Details
                if "tags" in rg:
                    all_tags = []
                    for key,value in rg["tags"].items():
                        tag_value = ""+key+"="+value+""
                        all_tags.append(tag_value)
                    tag_csv_value = '\n'.join(all_tags)
                    tag_sql_value = ','.join(all_tags)
                else:
                    tag_csv_value = None
                    tag_sql_value = "No Tags"
                
                # Get Lock Details
                print("Getting Locks Details for Resource Group - ", rg["name"])
                get_rg_lock_details = requests.get(url = "https://management.azure.com/"+rg["id"]+"/providers/Microsoft.Authorization/locks?api-version=2016-09-01", headers = header)
                rg_lock_resonse_to_json = get_rg_lock_details.json()
                if get_rg_lock_details.status_code == 200 or get_rg_lock_details.status_code == 204:
                    if rg_lock_resonse_to_json["value"]:
                        all_locks = []
                        for lock in rg_lock_resonse_to_json["value"]:
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
                    print("Unable to get Resource group Locks Details. Please check the error..")
                    lock_csv_value = ""+rg_lock_resonse_to_json["error"]["code"]+" - "+rg_lock_resonse_to_json["error"]["message"]+""
                    lock_sql_value = ""+rg_lock_resonse_to_json["error"]["code"]+" - "+rg_lock_resonse_to_json["error"]["message"]+""

                # Get Total Cost
                print("Getting Current Usage Details for Resource Group - ", rg["name"])
                payload = {"type": "Usage", "timeframe": "BillingMonthToDate", "dataset": { "granularity": "None", "aggregation": { "totalCost": { "name": "PreTaxCost", "function": "Sum" } }, "grouping": [ ] } }
                get_rg_consumption_details = requests.post(url = "https://management.azure.com/"+rg["id"]+"/providers/Microsoft.CostManagement/query?api-version=2022-10-01", headers = header, json = payload)
                rg_consumption_response_to_json = get_rg_consumption_details.json()
                if get_rg_consumption_details.status_code == 200 or get_rg_consumption_details.status_code == 204:
                    if rg_consumption_response_to_json["properties"]["rows"]:
                        for usage in rg_consumption_response_to_json["properties"]["rows"]:
                            consumption_csv_value = float("{:.2f}".format(usage[0]))
                            consumption_sql_value = float("{:.2f}".format(usage[0]))
                    else:
                        consumption_csv_value = None
                        consumption_sql_value = float(0)
                else:
                    print("Unable to get Resource group Current Usage Details. Please check the error..")
                    consumption_csv_value = ""+rg_consumption_response_to_json["error"]["code"]+" - "+rg_consumption_response_to_json["error"]["message"]+""
                    consumption_sql_value = float(0)
                
                # Get Resource Group Forecast Usage Details
                print("Getting Forecast Usage Details for Resource Group - ", rg["name"])
                payload = {"type": "Usage", "timeframe": "BillingMonthToDate", "dataset": { "granularity": "None", "aggregation": { "totalCost": { "name": "PreTaxCost", "function": "Sum" } }, "grouping": [ ] } }
                get_rg_forecast_details = requests.post(url = "https://management.azure.com/"+rg["id"]+"/providers/Microsoft.CostManagement/forecast?api-version=2022-10-01", headers = header, json = payload)
                rg_forecast_response_to_json = get_rg_forecast_details.json()
                if get_rg_forecast_details.status_code == 200 or get_rg_forecast_details.status_code == 204:
                    if rg_forecast_response_to_json["properties"]["rows"]:
                        for usage in rg_forecast_response_to_json["properties"]["rows"]:
                            forecast_csv_value = float("{:.2f}".format(usage[0]))
                            forecast_sql_value = float("{:.2f}".format(usage[0]))
                    else:
                        forecast_csv_value = None
                        forecast_sql_value = float(0)
                else:
                    print("Unable to get Resource Group Forecast Usage Details..Please check the error..")
                    forecast_csv_value = ""+rg_forecast_response_to_json["error"]["code"]+" - "+rg_forecast_response_to_json["error"]["message"]+""
                    forecast_sql_value = float(0)
                
                # Get No of Resources and unique locations in Resource Group
                print("Getting number of Resources and unique location for Resource Group - ", rg["name"])
                get_resources_details = requests.get(url = "https://management.azure.com/"+rg["id"]+"/resources?api-version=2021-04-01", headers = header)
                resource_response_to_json = get_resources_details.json()
                resource_number_csv_value = len(resource_response_to_json["value"])
                resource_all_location_list = []
                for all_resource_location in resource_response_to_json["value"]:
                    resource_location = all_resource_location["location"]
                    resource_all_location_list.append(resource_location)
                resource_unique_location_set = set(resource_all_location_list)
                resource_unique_locaton_number_csv_value = len(resource_unique_location_set)
                resource_unique_location_list = list(resource_unique_location_set)
                resource_unique_locations_csv_value = ','.join(resource_unique_location_list)

                # Get Compliance Summary for Resource Group
                print("Getting Compliance Summary for ", rg["name"])
                get_summary = requests.post(url = "https://management.azure.com"+rg["id"]+"/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01", headers = header)
                get_summary_to_json = get_summary.json()
                if get_summary.status_code == 200 or get_summary.status_code == 204:
                    if "value" in get_summary_to_json:
                        non_compliant_resources = get_summary_to_json["value"][0]["results"]["nonCompliantResources"]
                        non_compliant_policy = get_summary_to_json["value"][0]["results"]["nonCompliantPolicies"]
                    else:
                        non_compliant_resources = None
                        non_compliant_policy = None
                else:
                    non_compliant_resources = None
                    non_compliant_policy = None

                # Write to CSV file
                print("Writing Resource Groups information to CSV - ", rg["name"])
                rg_excel_data = [subscription_name,rg["name"],rg["location"],rg["properties"]["provisioningState"],rg["id"],tag_csv_value,lock_csv_value,resource_number_csv_value,resource_unique_locaton_number_csv_value,resource_unique_locations_csv_value,consumption_csv_value,forecast_csv_value,non_compliant_resources,non_compliant_policy]
                rg_sql_data = [subscription_name,rg["name"],rg["location"],rg["properties"]["provisioningState"],rg["id"],tag_sql_value,lock_sql_value,resource_number_csv_value,resource_unique_locaton_number_csv_value,resource_unique_locations_csv_value,consumption_sql_value,forecast_sql_value,non_compliant_resources,non_compliant_policy]
                with open('Resource Group.csv', mode='a', newline='') as rg_csv_file_data:
                    csvwriter = csv.writer(rg_csv_file_data, delimiter=',')
                    csvwriter.writerow(rg_excel_data)
                with open('sql_resource_group.csv', mode='a', newline='') as rg_sql_file_data:
                    csvwriter = csv.writer(rg_sql_file_data, delimiter=',')
                    csvwriter.writerow(rg_sql_data)
        else:
            print("No Resource Group found in the Subscription. Skipping..")
            sys.exit(1)
    else:
        print("Unable to get Resource Group Details for the Subscription ID. Please check subscription ID..")
        print("Error is : "+rg_response_to_json["error"]["code"]+" - "+rg_response_to_json["error"]["message"]+"")
        sys.exit(1)