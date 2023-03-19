import requests
import json
import sys
import csv
import os

def get_sa(subscription_id, subscription_name, header):
    print("Getting Storage Accounts for ", subscription_name)
    get_sa_list = requests.get(url = "https://management.azure.com/subscriptions/"+subscription_id+"/providers/Microsoft.Storage/storageAccounts?api-version=2022-09-01", headers = header)
    get_sa_list_to_json = get_sa_list.json()
    if get_sa_list.status_code == 200 or get_sa_list.status_code == 204:
        with open("sa.json", "w", encoding="utf-8") as sa_json:
            json.dump(get_sa_list_to_json, sa_json, ensure_ascii=False, indent=4)
        if "value" in get_sa_list_to_json:
            sa_excel_header = ["Subscription", "Resource Group", "Name", "Location", "Kind", "SKU Name", "SKU Tier", "TLS Version", "Blob Public Access", "Access Tier", "Number of Containers", "Number of File Shares", "Number of Tables", "Number of Queues", "Provisioning State", "Tags"]
            sa_sql_header = ["sub", "rg_name", "name", "location", "kind", "sku_name", "sku_tier", "tls_version", "blob_public_access", "access_tier", "num_container", "num_file_share", "num_tables", "num_queues", "provisioning_state", "tags"]
            with open('Storage Accounts.csv', mode='w', newline='') as sa_excel_file_header:
                csvwriter = csv.writer(sa_excel_file_header, delimiter=',')
                csvwriter.writerow(sa_excel_header)
            with open('sql_sa.csv', mode='w', newline='') as sa_sql_file_header:
                csvwriter = csv.writer(sa_sql_file_header, delimiter=',')
                csvwriter.writerow(sa_sql_header)
            for sa in get_sa_list_to_json["value"]:
                # Get Tags
                if "tags" in sa:
                    sa_tags = []
                    for key,value in sa["tags"].items():
                        sa_tag_value = ""+key+"="+value+""
                        sa_tags.append(sa_tag_value)
                    sa_tag_excel_value = '\n'.join(sa_tags)
                    sa_tag_sql_value = ','.join(sa_tags)
                else:
                    sa_tag_excel_value = None
                    sa_tag_sql_value = "No Tags"
                
                # Get some validations
                if "accessTier" in sa["properties"]:
                    access_tier = sa["properties"]["accessTier"]
                else:
                    access_tier = None
                
                # Get Number of Containers
                get_container_list = requests.get(url = "https://management.azure.com"+sa["id"]+"/blobServices/default/containers?api-version=2022-09-01", headers = header)
                get_container_list_to_json = get_container_list.json()
                if get_container_list.status_code == 200 or get_container_list.status_code == 204:
                    num_of_container = len(get_container_list_to_json["value"])
                else:
                    num_of_container = 0
                
                # Get Number of File Shares
                get_fs_list = requests.get(url = "https://management.azure.com"+sa["id"]+"/fileServices/default/shares?api-version=2022-09-01", headers = header)
                get_fs_list_to_json = get_fs_list.json()
                if get_fs_list.status_code == 200 or get_fs_list.status_code == 204:
                    num_of_fs = len(get_fs_list_to_json["value"])
                else:
                    num_of_fs = 0
                
                # Get Number of Tables
                get_tables_list = requests.get(url = "https://management.azure.com"+sa["id"]+"/tableServices/default/tables?api-version=2022-09-01", headers = header)
                get_tables_list_to_json = get_tables_list.json()
                if get_tables_list.status_code == 200 or get_tables_list.status_code == 204:
                    num_of_tables = len(get_tables_list_to_json["value"])
                else:
                    num_of_tables = 0
                
                # Get Number of Queues
                get_queues_list = requests.get(url = "https://management.azure.com"+sa["id"]+"/queueServices/default/queues?api-version=2022-09-01", headers = header)
                get_queues_list_to_json = get_queues_list.json()
                if get_queues_list.status_code == 200 or get_queues_list.status_code == 204:
                    num_of_queues = len(get_queues_list_to_json["value"])
                else:
                    num_of_queues = 0

                # Write Data to CSV files
                print("Writing Data for ", sa["name"])
                sa_excel_data = [subscription_name, sa["id"].split('/')[4], sa["name"], sa["location"], sa["kind"], sa["sku"]["name"], sa["sku"]["tier"], sa["properties"]["minimumTlsVersion"], sa["properties"]["allowBlobPublicAccess"], access_tier, num_of_container, num_of_fs, num_of_tables, num_of_queues, sa["properties"]["provisioningState"], sa_tag_excel_value]
                sa_sql_data = [subscription_name, sa["id"].split('/')[4], sa["name"], sa["location"], sa["kind"], sa["sku"]["name"], sa["sku"]["tier"], sa["properties"]["minimumTlsVersion"], sa["properties"]["allowBlobPublicAccess"], access_tier, num_of_container, num_of_fs, num_of_tables, num_of_queues, sa["properties"]["provisioningState"], sa_tag_sql_value]
                with open('Storage Accounts.csv', mode='a', newline='') as sa_excel_file_data:
                    csvwriter = csv.writer(sa_excel_file_data, delimiter=',')
                    csvwriter.writerow(sa_excel_data)
                with open('sql_sa.csv', mode='a', newline='') as sa_sql_file_data:
                    csvwriter = csv.writer(sa_sql_file_data, delimiter=',')
                    csvwriter.writerow(sa_sql_data)
        else:
            print("No Storage account for ", subscription_name)
            os.exit(1)
    else:
        print("Unable to get Storage Account for ", subscription_name)
        os.exit(1)

def get_sa_blob(subscription_name, header):
    # Load the Saved Json file
    with open("sa.json") as sa_saved_json:
        sa_saved_json = json.load(sa_saved_json)
    if "value" in sa_saved_json:
        # Write CSV File Header
        blob_excel_header = ["Subscription", "Resource Group", "Storage Account", "Name", "Deleted", "Versioning", "Public Access", "Lease Status", "Lease State"]
        blob_sql_header = ["sub", "rg_name", "sa_name", "name", "deleted", "versioning", "public_access", "lease_status", "lease_state"]
        with open('Storage Account Containers.csv', mode='w', newline='') as blob_excel_file_header:
            csvwriter = csv.writer(blob_excel_file_header, delimiter=',')
            csvwriter.writerow(blob_excel_header)
        with open('sql_blob.csv', mode='w', newline='') as blob_sql_file_header:
            csvwriter = csv.writer(blob_sql_file_header, delimiter=',')
            csvwriter.writerow(blob_sql_header)
        for sa in sa_saved_json["value"]:
            print("Getting Blob Details for ", sa["name"])
            get_blob_list = requests.get(url = "https://management.azure.com"+sa["id"]+"/blobServices/default/containers?api-version=2022-09-01", headers = header)
            get_blob_list_to_json = get_blob_list.json()
            if get_blob_list.status_code == 200 or get_blob_list.status_code == 204:
                if "value" in get_blob_list_to_json:
                    for blob in get_blob_list_to_json["value"]:
                        if "immutableStorageWithVersioning" in blob["properties"]:
                            if "enabled" in blob["properties"]["immutableStorageWithVersioning"]:
                                blob_versioning = blob["properties"]["immutableStorageWithVersioning"]["enabled"]
                            else:
                                blob_versioning = None
                        else:
                            blob_versioning = None
                        
                        # Write Data to Excel and SQL
                        print("Writing Container Details for ", blob["name"])
                        blob_excel_data = [subscription_name, sa["id"].split('/')[4], sa["name"], blob["name"], blob["properties"]["deleted"], blob_versioning, blob["properties"]["publicAccess"], blob["properties"]["leaseStatus"], blob["properties"]["leaseState"]]
                        blob_sql_data = [subscription_name, sa["id"].split('/')[4], sa["name"], blob["name"], blob["properties"]["deleted"], blob_versioning, blob["properties"]["publicAccess"], blob["properties"]["leaseStatus"], blob["properties"]["leaseState"]]
                        with open('Storage Account Containers.csv', mode='a', newline='') as blob_excel_file_data:
                            csvwriter = csv.writer(blob_excel_file_data, delimiter=',')
                            csvwriter.writerow(blob_excel_data)
                        with open('sql_blob.csv', mode='a', newline='') as blob_sql_file_data:
                            csvwriter = csv.writer(blob_sql_file_data, delimiter=',')
                            csvwriter.writerow(blob_sql_data)
                else:
                    print("No Blob found for ", sa["name"])
                    pass
            else:
                print("No blob found for ", sa["name"])
                pass
    else:
        print("No Storage Account found for ", subscription_name)
        pass

def get_sa_file_share(subscription_name, header):
    # Load the Saved Json file
    with open("sa.json") as sa_saved_json:
        sa_saved_json = json.load(sa_saved_json)
    if "value" in sa_saved_json:
        # Write CSV file header
        file_share_excel_header = ["Subscription", "Resource Group", "Storage Account", "Name", "Quota(GB)", "Protocol", "Lease Status", "Lease State", "Access Tier"]
        file_share_sql_header = ["sub", "rg_name", "sa_name", "name", "quota_in_gb", "protocol", "lease_status", "lease_state", "access_tier"]
        with open('Storage Account File Shares.csv', mode='w', newline='') as file_share_excel_file_header:
            csvwriter = csv.writer(file_share_excel_file_header, delimiter=',')
            csvwriter.writerow(file_share_excel_header)
        with open('sql_file_share.csv', mode='w', newline='') as file_share_sql_file_header:
            csvwriter = csv.writer(file_share_sql_file_header, delimiter=',')
            csvwriter.writerow(file_share_sql_header)
        for sa in sa_saved_json["value"]:
            print("Getting File Share details for ", sa["name"])
            get_file_share_list = requests.get(url = "https://management.azure.com"+sa["id"]+"/fileServices/default/shares?api-version=2022-09-01", headers = header)
            get_file_share_list_to_json = get_file_share_list.json()
            if get_file_share_list.status_code == 200 or get_file_share_list.status_code == 204:
                if "value" in get_file_share_list_to_json:
                    for shares in get_file_share_list_to_json["value"]:
                        # Write Data to Excel and SQL
                        print("Writing File Share Details for ", shares["name"])
                        file_share_excel_data = [subscription_name, shares["id"].split('/')[4], sa["name"], shares["name"], shares["properties"]["shareQuota"]/1024, shares["properties"]["enabledProtocols"], shares["properties"]["leaseStatus"], shares["properties"]["leaseState"], shares["properties"]["accessTier"]]
                        file_share_sql_data = [subscription_name, shares["id"].split('/')[4], sa["name"], shares["name"], shares["properties"]["shareQuota"]/1024, shares["properties"]["enabledProtocols"], shares["properties"]["leaseStatus"], shares["properties"]["leaseState"], shares["properties"]["accessTier"]]
                        with open('Storage Account File Shares.csv', mode='a', newline='') as file_share_excel_file_data:
                            csvwriter = csv.writer(file_share_excel_file_data, delimiter=',')
                            csvwriter.writerow(file_share_excel_data)
                        with open('sql_file_share.csv', mode='a', newline='') as file_share_sql_file_data:
                            csvwriter = csv.writer(file_share_sql_file_data, delimiter=',')
                            csvwriter.writerow(file_share_sql_data)
                else:
                    print("No File Share found for ", sa["name"])
            else:
                print("No File Share found for ", sa["name"])
                pass
    else:
        print("No Storage Account found for ", subscription_name)
        pass

def get_sa_table(subscription_name, header):
    # Load the Saved Json file
    with open("sa.json") as sa_saved_json:
        sa_saved_json = json.load(sa_saved_json)
    if "value" in sa_saved_json:
        # Write CSV file header
        table_excel_header = ["Subscription", "Resource Group", "Storage Account", "Name", "Table Name"]
        table_sql_header = ["sub", "rg_name", "sa_name", "name", "table_name"]
        with open('Storage Account Tables.csv', mode='w', newline='') as table_excel_file_header:
            csvwriter = csv.writer(table_excel_file_header, delimiter=',')
            csvwriter.writerow(table_excel_header)
        with open('sql_tables.csv', mode='w', newline='') as table_sql_file_header:
            csvwriter = csv.writer(table_sql_file_header, delimiter=',')
            csvwriter.writerow(table_sql_header)
        for sa in sa_saved_json["value"]:
            print("Getting Table Details for ", sa["name"])
            get_table_list = requests.get(url = "https://management.azure.com"+sa["id"]+"/tableServices/default/tables?api-version=2022-09-01", headers = header)
            get_table_list_to_json = get_table_list.json()
            if get_table_list.status_code == 200 or get_table_list.status_code == 204:
                if "value" in get_table_list_to_json:
                    for tables in get_table_list_to_json["value"]:
                        # Write Data to Excel and SQL
                        print("Writing Table Details for ", tables["name"])
                        table_excel_data = [subscription_name, tables["id"].split('/')[4], sa["name"], tables["name"], tables["properties"]["tableName"]]
                        table_sql_data = [subscription_name, tables["id"].split('/')[4], sa["name"], tables["name"], tables["properties"]["tableName"]]
                        with open('Storage Account Tables.csv', mode='a', newline='') as table_excel_file_data:
                            csvwriter = csv.writer(table_excel_file_data, delimiter=',')
                            csvwriter.writerow(table_excel_data)
                        with open('sql_tables.csv', mode='a', newline='') as table_sql_file_data:
                            csvwriter = csv.writer(table_sql_file_data, delimiter=',')
                            csvwriter.writerow(table_sql_data)
                else:
                    print("No Tables found for ", sa["name"])
                    pass
            else:
                print("No Tables found for ", sa["name"])
                pass
    else:
        print("No Storage Account found for ", subscription_name)
        pass

def get_sa_queue(subscription_name, header):
    # Load the Saved Json file
    with open("sa.json") as sa_saved_json:
        sa_saved_json = json.load(sa_saved_json)
    if "value" in sa_saved_json:
        # Write CSV file header
        queue_excel_header = ["Subscription", "Resource Group", "Storage Account", "Name"]
        queue_sql_header = ["sub", "rg_name", "sa_name", "name"]
        with open('Storage Account Queue.csv', mode='w', newline='') as queue_excel_file_header:
            csvwriter = csv.writer(queue_excel_file_header, delimiter=',')
            csvwriter.writerow(queue_excel_header)
        with open('sql_queue.csv', mode='w', newline='') as table_sql_file_header:
            csvwriter = csv.writer(table_sql_file_header, delimiter=',')
            csvwriter.writerow(queue_sql_header)
        for sa in sa_saved_json["value"]:
            print("Getting Queue Details for ", sa["name"])
            get_queue_list = requests.get(url = "https://management.azure.com"+sa["id"]+"/queueServices/default/queues?api-version=2022-09-01", headers = header)
            get_queue_list_to_json = get_queue_list.json()
            if get_queue_list.status_code == 200 or get_queue_list.status_code == 204:
                if "value" in get_queue_list_to_json:
                    for queue in get_queue_list_to_json["value"]:
                        # Write Data to Excel and SQL
                        print("Writing Queue Details for ", queue["name"])
                        queue_excel_data = [subscription_name, queue["id"].split('/')[4], sa["name"], queue["name"]]
                        queue_sql_data = [subscription_name, queue["id"].split('/')[4], sa["name"], queue["name"]]
                        with open('Storage Account Queue.csv', mode='a', newline='') as queue_excel_file_data:
                            csvwriter = csv.writer(queue_excel_file_data, delimiter=',')
                            csvwriter.writerow(queue_excel_data)
                        with open('sql_queue.csv', mode='a', newline='') as queue_sql_file_data:
                            csvwriter = csv.writer(queue_sql_file_data, delimiter=',')
                            csvwriter.writerow(queue_sql_data)
                else:
                    print("No Queue Found for ", sa["name"])
                    pass
            else:
                print("No Queue Found for ", sa["name"])
                pass
    else:
        print("No Storage Account found for ", subscription_name)
        pass