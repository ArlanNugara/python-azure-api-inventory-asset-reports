import requests
import json
import sys
import csv
import os

def get_active_kv(subscription_id, subscription_name,header):
    print("Getting Active Key vault details for ", subscription_name)
    # Create the header
    kv_excel_header = ["Subscription", "Resource Group", "Name", "Location", "Provisioning State", "Public Network Access", "Total Access Policy", "SKU Family", "SKU Name", "Created By", "Created At", "Last Modified By", "Last Modified At", "Deployment Enabled", "Disk Encryption Enabled", "Template Deployment Enabled", "Soft Delete Enabled", "Soft Delete Retension Days", "RBAC Auth Enabled", "Vault URI", "Tags"]
    kv_sql_header = ["sub", "rg_name", "kv_name", "kv_location", "kv_provisioning_state", "kv_public_network_access", "kv_access_policy_num", "kv_sku_family", "kv_sku_name", "kv_created_by", "kv_created_at", "kv_last_modified_by", "kv_last_modified_at", "kv_deployment_enabled", "kv_disk_encryption_enabled", "kv_template_deployment_enabled", "kv_soft_delete_enabled", "kv_soft_delete_retension_days", "kv_rbac_auth_enabled", "kv_vault_uri", "tags"]
    with open('Active Key Vaults.csv', mode = 'w', newline='') as kv_excel_file_header:
        csvwriter = csv.writer(kv_excel_file_header, delimiter=',')
        csvwriter.writerow(kv_excel_header)
    with open('sql_kv_active.csv', mode = 'w', newline='') as kv_sql_file_header:
        csvwriter = csv.writer(kv_sql_file_header, delimiter=',')
        csvwriter.writerow(kv_sql_header)
    # Get Active Key Vaults
    get_kv_details = requests.get(url = "https://management.azure.com/subscriptions/"+subscription_id+"/providers/Microsoft.KeyVault/vaults?api-version=2022-07-01", headers = header)
    get_kv_details_to_json = get_kv_details.json()
    if get_kv_details.status_code == 200 or get_kv_details.status_code == 204:
        if "value" in get_kv_details_to_json:
            for kv in get_kv_details_to_json["value"]:
                kv_name = kv["name"]
                kv_location = kv["location"]
                kv_rg_name_split = kv["id"].split('/')
                kv_rg_name = kv_rg_name_split[4]
                if "tags" in kv:
                    all_tags = []
                    for key,value in kv["tags"].items():
                        tag_value = ""+key+"="+value+""
                        all_tags.append(tag_value)
                    tag_csv_value = '\n'.join(all_tags)
                    tag_sql_value = ','.join(all_tags)
                else:
                    tag_csv_value = str()
                    tag_sql_value = "No Tags"
                if "systemData" in kv:
                    if "createdBy" in kv["systemData"]:
                        kv_created_by = kv["systemData"]["createdBy"]
                    else:
                        kv_created_by = None
                    if "createdAt" in kv["systemData"]:
                        kv_created_at = kv["systemData"]["createdAt"]
                    else:
                        kv_created_at = None
                    if "lastModifiedBy" in kv["systemData"]:
                        kv_modified_by = kv["systemData"]["lastModifiedBy"]
                    else:
                        kv_modified_by = None
                    if "lastModifiedAt" in kv["systemData"]:
                        kv_modified_at = kv["systemData"]["lastModifiedAt"]
                    else:
                        kv_modified_at = None
                else:
                    kv_created_by = None
                    kv_created_at = None
                    kv_modified_by = None
                    kv_modified_at = None
                if "properties" in kv:
                    if "sku" in kv["properties"]:
                        if "family" in kv["properties"]["sku"]:
                            kv_sku_family = kv["properties"]["sku"]["family"]
                        else:
                            kv_sku_family = None
                        if "name" in kv["properties"]["sku"]:
                            kv_sku_name = kv["properties"]["sku"]["name"]
                        else:
                            kv_sku_name = None
                    else:
                        kv_sku_family = None
                        kv_sku_name = None
                    if "enabledForDeployment" in kv["properties"]:
                        kv_deployment_enabled = kv["properties"]["enabledForDeployment"]
                    else:
                        kv_deployment_enabled = None
                    if "enabledForDiskEncryption" in kv["properties"]:
                        kv_disk_encrypt_enabled = kv["properties"]["enabledForDiskEncryption"]
                    else:
                        kv_disk_encrypt_enabled = None
                    if "enabledForTemplateDeployment" in kv["properties"]:
                        kv_template_deployment_enabled = kv["properties"]["enabledForTemplateDeployment"]
                    else:
                        kv_template_deployment_enabled = None
                    if "enableSoftDelete" in kv["properties"]:
                        kv_soft_delete_enabled = kv["properties"]["enableSoftDelete"]
                    else:
                        kv_soft_delete_enabled = None
                    if "softDeleteRetentionInDays" in kv["properties"]:
                        kv_soft_delete_retension = kv["properties"]["softDeleteRetentionInDays"]
                    else:
                        kv_soft_delete_retension = None
                    if "enableRbacAuthorization" in kv["properties"]:
                        kv_rbac_auth_enabled = kv["properties"]["enableRbacAuthorization"]
                    else:
                        kv_rbac_auth_enabled = None
                    if "vaultUri" in kv["properties"]:
                        kv_vault_uri = kv["properties"]["vaultUri"]
                    else:
                        kv_vault_uri = None
                    if "provisioningState" in kv["properties"]:
                        kv_provisioning_state = kv["properties"]["provisioningState"]
                    else:
                        kv_provisioning_state = None
                    if "publicNetworkAccess" in kv["properties"]:
                        kv_public_network_enabled = kv["properties"]["publicNetworkAccess"]
                    else:
                        kv_public_network_enabled = None
                    if "accessPolicies" in kv["properties"]:
                        kv_access_policy_num = len(kv["properties"]["accessPolicies"])
                    else:
                        kv_access_policy_num = 0
                else:
                    kv_sku_family = None
                    kv_sku_name = None
                    kv_deployment_enabled = None
                    kv_disk_encrypt_enabled = None
                    kv_template_deployment_enabled = None
                    kv_soft_delete_enabled = None
                    kv_soft_delete_retension = None
                    kv_rbac_auth_enabled = None
                    kv_vault_uri = None
                    kv_provisioning_state = None
                    kv_public_network_enabled = None
                    kv_access_policy_num = 0
                # Write Details to CSV
                print("Writing Active Key vault Details for ", kv_name)
                kv_excel_data = [subscription_name, kv_rg_name, kv_name, kv_location, kv_provisioning_state, kv_public_network_enabled, kv_access_policy_num, kv_sku_family, kv_sku_name, kv_created_by, kv_created_at, kv_modified_by, kv_modified_at, kv_deployment_enabled, kv_disk_encrypt_enabled, kv_template_deployment_enabled, kv_soft_delete_enabled, kv_soft_delete_retension, kv_rbac_auth_enabled, kv_vault_uri, tag_csv_value]
                kv_sql_data = [subscription_name, kv_rg_name, kv_name, kv_location, kv_provisioning_state, kv_public_network_enabled, kv_access_policy_num, kv_sku_family, kv_sku_name, kv_created_by, kv_created_at, kv_modified_by, kv_modified_at, kv_deployment_enabled, kv_disk_encrypt_enabled, kv_template_deployment_enabled, kv_soft_delete_enabled, kv_soft_delete_retension, kv_rbac_auth_enabled, kv_vault_uri, tag_sql_value]
                with open('Active Key Vaults.csv', mode = 'a', newline='') as kv_excel_file_data:
                    csvwriter = csv.writer(kv_excel_file_data, delimiter=',')
                    csvwriter.writerow(kv_excel_data)
                with open('sql_kv_active.csv', mode = 'a', newline='') as kv_sql_file_data:
                    csvwriter = csv.writer(kv_sql_file_data, delimiter=',')
                    csvwriter.writerow(kv_sql_data)
                
            while 'nextLink' in get_kv_details_to_json:
                print("Next Link Found. Querying API for more data")
                get_kv_details = requests.get(url = get_kv_details_to_json["nextLink"], headers = header)
                get_kv_details_to_json = get_kv_details.json()
                if get_kv_details.status_code == 200 or get_kv_details.status_code == 204:
                    if "value" in get_kv_details_to_json:
                        for kv in get_kv_details_to_json["value"]:
                            kv_name = kv["name"]
                            kv_location = kv["location"]
                            kv_rg_name_split = kv["id"].split('/')
                            kv_rg_name = kv_rg_name_split[4]
                            if "tags" in kv:
                                all_tags = []
                                for key,value in kv["tags"].items():
                                    tag_value = ""+key+"="+value+""
                                    all_tags.append(tag_value)
                                tag_csv_value = '\n'.join(all_tags)
                                tag_sql_value = ','.join(all_tags)
                            else:
                                tag_csv_value = str()
                                tag_sql_value = "No Tags"
                            if "systemData" in kv:
                                if "createdBy" in kv["systemData"]:
                                    kv_created_by = kv["systemData"]["createdBy"]
                                else:
                                    kv_created_by = None
                                if "createdAt" in kv["systemData"]:
                                    kv_created_at = kv["systemData"]["createdAt"]
                                else:
                                    kv_created_at = None
                                if "lastModifiedBy" in kv["systemData"]:
                                    kv_modified_by = kv["systemData"]["lastModifiedBy"]
                                else:
                                    kv_modified_by = None
                                if "lastModifiedAt" in kv["systemData"]:
                                    kv_modified_at = kv["systemData"]["lastModifiedAt"]
                                else:
                                    kv_modified_at = None
                            else:
                                kv_created_by = None
                                kv_created_at = None
                                kv_modified_by = None
                                kv_modified_at = None
                            if "properties" in kv:
                                if "sku" in kv["properties"]:
                                    if "family" in kv["properties"]["sku"]:
                                        kv_sku_family = kv["properties"]["sku"]["family"]
                                    else:
                                        kv_sku_family = None
                                    if "name" in kv["properties"]["sku"]:
                                        kv_sku_name = kv["properties"]["sku"]["name"]
                                    else:
                                        kv_sku_name = None
                                else:
                                    kv_sku_family = None
                                    kv_sku_name = None
                                if "enabledForDeployment" in kv["properties"]:
                                    kv_deployment_enabled = kv["properties"]["enabledForDeployment"]
                                else:
                                    kv_deployment_enabled = None
                                if "enabledForDiskEncryption" in kv["properties"]:
                                    kv_disk_encrypt_enabled = kv["properties"]["enabledForDiskEncryption"]
                                else:
                                    kv_disk_encrypt_enabled = None
                                if "enabledForTemplateDeployment" in kv["properties"]:
                                    kv_template_deployment_enabled = kv["properties"]["enabledForTemplateDeployment"]
                                else:
                                    kv_template_deployment_enabled = None
                                if "enableSoftDelete" in kv["properties"]:
                                    kv_soft_delete_enabled = kv["properties"]["enableSoftDelete"]
                                else:
                                    kv_soft_delete_enabled = None
                                if "softDeleteRetentionInDays" in kv["properties"]:
                                    kv_soft_delete_retension = kv["properties"]["softDeleteRetentionInDays"]
                                else:
                                    kv_soft_delete_retension = None
                                if "enableRbacAuthorization" in kv["properties"]:
                                    kv_rbac_auth_enabled = kv["properties"]["enableRbacAuthorization"]
                                else:
                                    kv_rbac_auth_enabled = None
                                if "vaultUri" in kv["properties"]:
                                    kv_vault_uri = kv["properties"]["vaultUri"]
                                else:
                                    kv_vault_uri = None
                                if "provisioningState" in kv["properties"]:
                                    kv_provisioning_state = kv["properties"]["provisioningState"]
                                else:
                                    kv_provisioning_state = None
                                if "publicNetworkAccess" in kv["properties"]:
                                    kv_public_network_enabled = kv["properties"]["publicNetworkAccess"]
                                else:
                                    kv_public_network_enabled = None
                                if "accessPolicies" in kv["properties"]:
                                    kv_access_policy_num = len(kv["properties"]["accessPolicies"])
                                else:
                                    kv_access_policy_num = 0
                            else:
                                kv_sku_family = None
                                kv_sku_name = None
                                kv_deployment_enabled = None
                                kv_disk_encrypt_enabled = None
                                kv_template_deployment_enabled = None
                                kv_soft_delete_enabled = None
                                kv_soft_delete_retension = None
                                kv_rbac_auth_enabled = None
                                kv_vault_uri = None
                                kv_provisioning_state = None
                                kv_public_network_enabled = None
                                kv_access_policy_num = 0
                            # Write Details to CSV
                            print("Writing Active Key vault Details for ", kv_name)
                            kv_excel_data = [subscription_name, kv_rg_name, kv_name, kv_location, kv_provisioning_state, kv_public_network_enabled, kv_access_policy_num, kv_sku_family, kv_sku_name, kv_created_by, kv_created_at, kv_modified_by, kv_modified_at, kv_deployment_enabled, kv_disk_encrypt_enabled, kv_template_deployment_enabled, kv_soft_delete_enabled, kv_soft_delete_retension, kv_rbac_auth_enabled, kv_vault_uri, tag_csv_value]
                            kv_sql_data = [subscription_name, kv_rg_name, kv_name, kv_location, kv_provisioning_state, kv_public_network_enabled, kv_access_policy_num, kv_sku_family, kv_sku_name, kv_created_by, kv_created_at, kv_modified_by, kv_modified_at, kv_deployment_enabled, kv_disk_encrypt_enabled, kv_template_deployment_enabled, kv_soft_delete_enabled, kv_soft_delete_retension, kv_rbac_auth_enabled, kv_vault_uri, tag_sql_value]
                            with open('Active Key Vaults.csv', mode = 'a', newline='') as kv_excel_file_data:
                                csvwriter = csv.writer(kv_excel_file_data, delimiter=',')
                                csvwriter.writerow(kv_excel_data)
                            with open('sql_kv_active.csv', mode = 'a', newline='') as kv_sql_file_data:
                                csvwriter = csv.writer(kv_sql_file_data, delimiter=',')
                                csvwriter.writerow(kv_sql_data)
                    else:
                        print("No Active Key vault found for ", subscription_name)
                        pass
                else:
                    print("Error getting Active Key Vault details for ", subscription_name)
                    pass
        else:
            print("No Active Key vault found for ", subscription_name)
            pass
    else:
        print("Error getting Active Key Vault details for ", subscription_name)
        pass

def get_deleted_kv(subscription_id, subscription_name,header):
    print("Getting Deleted Key vault details for ", subscription_name)
    # Create the headers
    kv_excel_header = ["Subscription", "Resource Group", "Name", "Location", "Deletion Date", "Purge Date", "Purge Protection", "Vault ID", "Tags"]
    kv_sql_header = ["sub", "rg_name", "kv_name", "kv_location", "kv_deletion_date", "kv_purge_date", "kv_purge_protection", "kv_vault_id", "tags"]
    with open('Deleted Key Vaults.csv', mode = 'w', newline='') as kv_excel_file_header:
        csvwriter = csv.writer(kv_excel_file_header, delimiter=',')
        csvwriter.writerow(kv_excel_header)
    with open('sql_kv_deleted.csv', mode = 'w', newline='') as kv_sql_file_header:
        csvwriter = csv.writer(kv_sql_file_header, delimiter=',')
        csvwriter.writerow(kv_sql_header)
    # Get Deleted Key Vault Data
    get_kv_details = requests.get(url = "https://management.azure.com/subscriptions/"+subscription_id+"/providers/Microsoft.KeyVault/deletedVaults?api-version=2022-07-01", headers = header)
    get_kv_details_to_json = get_kv_details.json()
    if get_kv_details.status_code == 200 or get_kv_details.status_code == 204:
        if "value" in get_kv_details_to_json:
            for kv in get_kv_details_to_json["value"]:
                kv_name = kv["name"]
                if "properties" in kv:
                    if "tags" in kv["properties"]:
                        all_tags = []
                        for key,value in kv["properties"]["tags"].items():
                            tag_value = ""+key+"="+value+""
                            all_tags.append(tag_value)
                        tag_csv_value = '\n'.join(all_tags)
                        tag_sql_value = ','.join(all_tags)
                    else:
                        tag_csv_value = str()
                        tag_sql_value = "No Tags"
                    if "vaultId" in kv["properties"]:
                        kv_vault_id = kv["properties"]["vaultId"]
                        kv_rg_name_split = kv["properties"]["vaultId"].split('/')
                        kv_rg_name = kv_rg_name_split[4]
                    else:
                        kv_vault_id = None
                        kv_rg_name = None
                    if "location" in kv["properties"]:
                        kv_location = kv["properties"]["location"]
                    else:
                        kv_location = None
                    if "deletionDate" in kv["properties"]:
                        kv_deletion_date = kv["properties"]["deletionDate"]
                    else:
                        kv_deletion_date = None
                    if "scheduledPurgeDate" in kv["properties"]:
                        kv_purge_date = kv["properties"]["scheduledPurgeDate"]
                    else:
                        kv_purge_date = None
                    if "purgeProtectionEnabled" in kv["properties"]:
                        kv_purge_protection = kv["properties"]["purgeProtectionEnabled"]
                    else:
                        kv_purge_protection = None
                else:
                    tag_csv_value = str()
                    tag_sql_value = "No Tags"
                    kv_vault_id = None
                    kv_rg_name = None
                    kv_location = None
                    kv_deletion_date = None
                    kv_purge_date = None
                    kv_purge_protection = None
                # Write Data to CSV
                print("Writing Deleted Key Vault Details for ", kv_name)
                kv_excel_data = [subscription_name, kv_rg_name, kv_name, kv_location, kv_deletion_date, kv_purge_date, kv_purge_protection, kv_vault_id, tag_csv_value]
                kv_sql_data = [subscription_name, kv_rg_name, kv_name, kv_location, kv_deletion_date, kv_purge_date, kv_purge_protection, kv_vault_id, tag_sql_value]
                with open('Deleted Key Vaults.csv', mode = 'a', newline='') as kv_excel_file_data:
                    csvwriter = csv.writer(kv_excel_file_data, delimiter=',')
                    csvwriter.writerow(kv_excel_data)
                with open('sql_kv_deleted.csv', mode = 'a', newline='') as kv_sql_file_data:
                    csvwriter = csv.writer(kv_sql_file_data, delimiter=',')
                    csvwriter.writerow(kv_sql_data)
            
            while 'nextLink' in get_kv_details_to_json:
                print("Next Link Found. Querying API for more data")
                get_kv_details = requests.get(url = get_kv_details_to_json["nextLink"], headers = header)
                get_kv_details_to_json = get_kv_details.json()
                if get_kv_details.status_code == 200 or get_kv_details.status_code == 204:
                    if "value" in get_kv_details_to_json:
                        for kv in get_kv_details_to_json["value"]:
                            kv_name = kv["name"]
                            if "properties" in kv:
                                if "tags" in kv["properties"]:
                                    all_tags = []
                                    for key,value in kv["properties"]["tags"].items():
                                        tag_value = ""+key+"="+value+""
                                        all_tags.append(tag_value)
                                    tag_csv_value = '\n'.join(all_tags)
                                    tag_sql_value = ','.join(all_tags)
                                else:
                                    tag_csv_value = str()
                                    tag_sql_value = "No Tags"
                                if "vaultId" in kv["properties"]:
                                    kv_vault_id = kv["properties"]["vaultId"]
                                    kv_rg_name_split = kv["properties"]["vaultId"].split('/')
                                    kv_rg_name = kv_rg_name_split[4]
                                else:
                                    kv_vault_id = None
                                    kv_rg_name = None
                                if "location" in kv["properties"]:
                                    kv_location = kv["properties"]["location"]
                                else:
                                    kv_location = None
                                if "deletionDate" in kv["properties"]:
                                    kv_deletion_date = kv["properties"]["deletionDate"]
                                else:
                                    kv_deletion_date = None
                                if "scheduledPurgeDate" in kv["properties"]:
                                    kv_purge_date = kv["properties"]["scheduledPurgeDate"]
                                else:
                                    kv_purge_date = None
                                if "purgeProtectionEnabled" in kv["properties"]:
                                    kv_purge_protection = kv["properties"]["purgeProtectionEnabled"]
                                else:
                                    kv_purge_protection = None
                            else:
                                tag_csv_value = str()
                                tag_sql_value = "No Tags"
                                kv_vault_id = None
                                kv_rg_name = None
                                kv_location = None
                                kv_deletion_date = None
                                kv_purge_date = None
                                kv_purge_protection = None
                            # Write Data to CSV
                            print("Writing Deleted Key Vault Details for ", kv_name)
                            kv_excel_data = [subscription_name, kv_rg_name, kv_name, kv_location, kv_deletion_date, kv_purge_date, kv_purge_protection, kv_vault_id, tag_csv_value]
                            kv_sql_data = [subscription_name, kv_rg_name, kv_name, kv_location, kv_deletion_date, kv_purge_date, kv_purge_protection, kv_vault_id, tag_sql_value]
                            with open('Deleted Key Vaults.csv', mode = 'a', newline='') as kv_excel_file_data:
                                csvwriter = csv.writer(kv_excel_file_data, delimiter=',')
                                csvwriter.writerow(kv_excel_data)
                            with open('sql_kv_deleted.csv', mode = 'a', newline='') as kv_sql_file_data:
                                csvwriter = csv.writer(kv_sql_file_data, delimiter=',')
                                csvwriter.writerow(kv_sql_data)
                    else:
                        print("No Deleted Key vault found for ", subscription_name)
                        pass
                else:
                    print("Eror getting Deleted Key Vault details for ", subscription_name)
                    pass
        else:
            print("No Deleted Key vault found for ", subscription_name)
            pass
    else:
        print("Eror getting Deleted Key Vault details for ", subscription_name)
        pass