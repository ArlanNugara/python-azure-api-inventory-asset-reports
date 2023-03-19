import requests
import json
import sys
import csv

# Get Subscription Details
def get_sub(subscription_id, header):
    # Get Subscription General Details
    print("Getting General Details for Subscription ID - "+subscription_id+"")
    get_subscription_details = requests.get(url = "https://management.azure.com/subscriptions/"+subscription_id+"?api-version=2020-01-01", headers = header)
    if get_subscription_details.status_code == 200 or get_subscription_details.status_code == 204:
        subscription_response_to_json = get_subscription_details.json()
        sub_id = subscription_response_to_json["subscriptionId"]
        sub_scope = subscription_response_to_json["id"]
        sub_alias = subscription_response_to_json["displayName"]
        sub_status = subscription_response_to_json["state"]
        if "tags" in subscription_response_to_json:
            all_tags = []
            for key,value in subscription_response_to_json["tags"].items():
                tag_value = ""+key+"="+value+""
                all_tags.append(tag_value)
            tag_csv_value = '\n'.join(all_tags)
            tag_sql_value = ','.join(all_tags)
        else:
            tag_csv_value = str()
            tag_sql_value = "No Tags"
    else:
        print("Unable to get Subscription details. Please check subscription ID..")
        sys.exit(1)
    
    # Get Subscription Locks Details
    print("Getting Lock Details for Subscription ID - "+subscription_id+"")
    get_subscription_lock_details = requests.get(url = "https://management.azure.com/subscriptions/"+subscription_id+"/providers/Microsoft.Authorization/locks?api-version=2016-09-01", headers = header)
    subscription_lock_response_to_json = get_subscription_lock_details.json()
    if get_subscription_lock_details.status_code == 200 or get_subscription_lock_details.status_code == 204:
        if subscription_lock_response_to_json['value']:
            all_locks = []
            for locks in subscription_lock_response_to_json['value']:
                lock_level = locks['properties']['level']
                scope_split = locks['id'].split('/')[:-4]
                scope_joined = '/'.join(scope_split)
                lock_name = locks['name']
                lock_value = "Level="+lock_level+", Name="+lock_name+", Scope="+scope_joined+""
                all_locks.append(lock_value)
            lock_csv_value = '\n'.join(all_locks)
            lock_sql_value = ','.join(all_locks)
        else:
            lock_csv_value = str()
            lock_sql_value = "No Locks"
    else:
        print("Unable to get Subscription Lock Details. Please check the error..")
        lock_csv_value = ""+subscription_lock_response_to_json["error"]["code"]+"-"+subscription_lock_response_to_json["error"]["message"]+""
        lock_sql_value = ""+subscription_lock_response_to_json["error"]["code"]+"-"+subscription_lock_response_to_json["error"]["message"]+""
    
    # Get Subscription Usage Details
    print("Getting Current Usage Details for Subscription ID - "+subscription_id+"")
    payload = {"type": "Usage", "timeframe": "BillingMonthToDate", "dataset": { "granularity": "None", "aggregation": { "totalCost": { "name": "PreTaxCost", "function": "Sum" } }, "grouping": [ ] } }
    get_subscription_consumption_details = requests.post(url = "https://management.azure.com/subscriptions/"+subscription_id+"/providers/Microsoft.CostManagement/query?api-version=2022-10-01", headers = header, json = payload)
    subscription_consumption_response_to_json = get_subscription_consumption_details.json()
    if get_subscription_consumption_details.status_code == 200 or get_subscription_consumption_details.status_code == 204:
        if subscription_consumption_response_to_json["properties"]["rows"]:
            for usage in subscription_consumption_response_to_json["properties"]["rows"]:
                consumption_csv_value = float("{:.2f}".format(usage[0]))
                consumption_sql_value = float("{:.2f}".format(usage[0]))
        else:
            consumption_csv_value = str()
            consumption_sql_value = float(0)
    else:
        print("Unable to get Subscription Current Usage Details. Please check subscription ID..")
        consumption_csv_value = ""+subscription_consumption_response_to_json["error"]["code"]+"-"+subscription_consumption_response_to_json["error"]["message"]+""
        consumption_sql_value = float(0)
    
    # Get Subscription Forecast Usage Details
    print("Getting Forecast Usage Details for Subscription ID - "+subscription_id+"")
    payload = {"type": "Usage", "timeframe": "BillingMonthToDate", "dataset": { "granularity": "None", "aggregation": { "totalCost": { "name": "PreTaxCost", "function": "Sum" } }, "grouping": [ ] } }
    get_subscription_forecast_details = requests.post(url = "https://management.azure.com/subscriptions/"+subscription_id+"/providers/Microsoft.CostManagement/forecast?api-version=2022-10-01", headers = header, json = payload)
    subscription_forecast_response_to_json = get_subscription_forecast_details.json()
    if get_subscription_forecast_details.status_code == 200 or get_subscription_forecast_details.status_code == 204:
        if subscription_forecast_response_to_json["properties"]["rows"]:
            for usage in subscription_forecast_response_to_json["properties"]["rows"]:
                forecast_csv_value = float("{:.2f}".format(usage[0]))
                forecast_sql_value = float("{:.2f}".format(usage[0]))
        else:
            forecast_csv_value = str()
            forecast_sql_value = float(0)
    else:
        print("Unable to get Subscription Forecast Usage Details. Please check the error..")
        forecast_csv_value = ""+subscription_forecast_response_to_json["error"]["code"]+" - "+subscription_forecast_response_to_json["error"]["message"]+""
        forecast_sql_value = float(0)
    
    # Get No of Resource Group and unique locations in Subscription
    print("Getting number of Resource Group and unique location for Subscription ID - "+subscription_id+"")
    get_rg_details = requests.get(url = "https://management.azure.com/subscriptions/"+subscription_id+"/resourcegroups?api-version=2021-04-01", headers = header)
    rg_response_to_json = get_rg_details.json()
    rg_number_csv_value = len(rg_response_to_json["value"])
    rg_all_location_list = []
    for all_rg_location in rg_response_to_json["value"]:
        rg_location = all_rg_location["location"]
        rg_all_location_list.append(rg_location)
    rg_unique_location_set = set(rg_all_location_list)
    rg_unique_locaton_number_csv_value = len(rg_unique_location_set)
    rg_unique_location_list = list(rg_unique_location_set)
    rg_unique_locations_csv_value = ','.join(rg_unique_location_list)

    # Get No of Resources and unique locations in Subscription
    print("Getting number of Resources and unique location for Subscription ID - "+subscription_id+"")
    get_resources_details = requests.get(url = "https://management.azure.com/subscriptions/"+subscription_id+"/resources?api-version=2021-04-01", headers = header)
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

    # Get Compliance Summary for Subscription
    print("Getting Compliance Summary for ", subscription_id)
    get_summary = requests.post(url = "https://management.azure.com/subscriptions/"+subscription_id+"/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01", headers = header)
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

    # Create CSV file
    print("Writing Subscription information to CSV file")
    subscription_excel_header = ['Name', 'ID', 'State', 'Scope', 'Tags', 'Locks', 'Total Resource Groups', 'Unique Resource Group Location', 'Resource Group Locations', 'Total Resources', 'Unique Resource Location', 'Resource Locations', 'Current Billing Period Cost', 'Forecast Billing Period Cost', 'Non Compliant Resources', 'Non Compliant Policy']
    subscription_sql_header = ['name', 'id', 'status', 'scope', 'tags', 'locks', 'total_rg', 'unique_rg_loc', 'rg_loc', 'total_resource', 'unique_resource_loc', 'resource_loc', 'current_cost', 'forecast_cost', 'non_compliant_resources', 'non_compliant_policy']
    subscription_excel_data = [sub_alias,sub_id,sub_status,sub_scope,tag_csv_value,lock_csv_value,rg_number_csv_value,rg_unique_locaton_number_csv_value,rg_unique_locations_csv_value,resource_number_csv_value,resource_unique_locaton_number_csv_value,resource_unique_locations_csv_value,consumption_csv_value,forecast_csv_value,non_compliant_resources,non_compliant_policy]
    subscription_sql_data = [str(sub_alias),str(sub_id),str(sub_status),str(sub_scope),str(tag_sql_value),str(lock_sql_value),int(rg_number_csv_value),int(rg_unique_locaton_number_csv_value),str(rg_unique_locations_csv_value),int(resource_number_csv_value),int(resource_unique_locaton_number_csv_value),str(resource_unique_locations_csv_value),consumption_sql_value,forecast_sql_value,non_compliant_resources,non_compliant_policy]

    # Create Excel CSV File
    with open('Subscription.csv', mode='w', newline='') as subscription_csv_file_header:
        csvwriter = csv.writer(subscription_csv_file_header, delimiter=',')
        csvwriter.writerow(subscription_excel_header)
    with open('Subscription.csv', mode='a', newline='') as subscription_csv_file_data:
        csvwriter = csv.writer(subscription_csv_file_data, delimiter=',')
        csvwriter.writerow(subscription_excel_data)
    # Create SQL CSV File
    with open('sql_subscription.csv', mode='w', newline='') as subscription_sql_file_header:
        csvwriter = csv.writer(subscription_sql_file_header, delimiter=',')
        csvwriter.writerow(subscription_sql_header)
    with open('sql_subscription.csv', mode='a', newline='') as subscription_sql_file_data:
        csvwriter = csv.writer(subscription_sql_file_data, delimiter=',')
        csvwriter.writerow(subscription_sql_data)
                