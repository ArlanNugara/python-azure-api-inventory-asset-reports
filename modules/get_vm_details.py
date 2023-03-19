import requests
import json
import sys
import csv
import os
from datetime import date, timedelta

# Get VM details
def get_vm(subscription_id, subscription_name, header):
    print("Getting Virtual Machine Details for ", subscription_name)
    # Write CSV Header
    vm_excel_header = ['Subscription', 'Name', 'ID', 'Location', 'Resource Group', 'Status', 'Creation Time', 'Size', 'OS Publisher', 'OS offer', 'OS SKU', 'OS Version', 'OS Exact Version', 'OS Patch Mode', 'OS Automatic Updates', 'Boot Diagnostic Settings', 'Boot Diagnostic Settings URI', 'VM Extension Number', 'VM Extension Names', 'OS Disk Name', 'OS Disk Location', 'OS Disk SKU Name', 'OS Disk SKU Tier', 'OS Disk Size(GB)', 'OS Disk Status', 'No of Additional Disk', 'No of Network Interfaces', 'Tags', 'Locks']
    vm_sql_header = ['sub', 'name', 'id', 'location', 'rg_name', 'status', 'creation_date', 'size', 'os_publisher', 'os_offer', 'os_sku', 'os_version', 'os_exact_version', 'os_patch_mode', 'os_automatic_update', 'boot_diag_settings', 'boot_diag_setting_uri', 'extension_num', 'extension_names', 'os_disk_name', 'os_disk_location', 'os_disk_sku_name', 'os_disk_sku_tier', 'os_disk_size_gb', 'os_disk_status', 'num_data_disk', 'num_ni', 'tags', 'locks']
    with open('Virtual Machines.csv', mode='w', newline='') as vm_excel_file_header:
        csvwriter = csv.writer(vm_excel_file_header, delimiter=',')
        csvwriter.writerow(vm_excel_header)
    with open('sql_vm_general.csv', mode='w', newline='') as vm_sql_file_header:
        csvwriter = csv.writer(vm_sql_file_header, delimiter=',')
        csvwriter.writerow(vm_sql_header)
    # Get Started
    get_vm_list = requests.get(url = "https://management.azure.com/subscriptions/"+subscription_id+"/providers/Microsoft.Compute/virtualMachines?api-version=2022-08-01", headers = header)
    vm_list_response_to_json = get_vm_list.json()
    with open("vm.json", "w", encoding="utf-8") as vm_json:
        json.dump(vm_list_response_to_json, vm_json, ensure_ascii=False, indent=4)
    if get_vm_list.status_code == 200 or get_vm_list.status_code == 204:
        if "value" in vm_list_response_to_json:
            for vm in vm_list_response_to_json["value"]:
                print("Getting details for ", vm["name"])
                get_vm_details = requests.get(url = "https://management.azure.com"+vm["id"]+"?api-version=2022-08-01", headers = header)
                vm_response_to_json = get_vm_details.json()
                vm_name = vm["name"]
                vm_location = vm["location"]
                vm_rg_name_split = vm["id"].split('/')
                vm_rg_name = vm_rg_name_split[4]
                vm_size = vm["properties"]["hardwareProfile"]["vmSize"]
                vm_id = vm["properties"]["vmId"]
                if "imageReference" in vm["properties"]["storageProfile"]:
                    if "publisher" in vm["properties"]["storageProfile"]["imageReference"]:
                        vm_os_publisher = vm["properties"]["storageProfile"]["imageReference"]["publisher"]
                    else:
                        vm_os_publisher = None
                    if "offer" in vm["properties"]["storageProfile"]["imageReference"]:
                        vm_os_offer = vm["properties"]["storageProfile"]["imageReference"]["offer"]
                    else:
                        vm_os_offer = None
                    if "version" in vm["properties"]["storageProfile"]["imageReference"]:
                        vm_os_version = vm["properties"]["storageProfile"]["imageReference"]["version"]
                    else:
                        vm_os_version = None
                    if "sku" in vm["properties"]["storageProfile"]["imageReference"]:
                        vm_os_sku = vm["properties"]["storageProfile"]["imageReference"]["sku"]
                    else:
                        vm_os_sku = None
                    if "exactVersion" in vm["properties"]["storageProfile"]["imageReference"]:
                        vm_os_exact_version = vm["properties"]["storageProfile"]["imageReference"]["exactVersion"]
                    else:
                        vm_os_exact_version = None
                else:
                    vm_os_publisher = None
                    vm_os_offer = None
                    vm_os_version = None
                    vm_os_sku = None
                    vm_os_exact_version = None
                if "osProfile" in vm["properties"]:
                    if "windowsConfiguration" in vm["properties"]["osProfile"]:
                        if "patchSettings" in vm["properties"]["osProfile"]["windowsConfiguration"]:
                            vm_os_patch_mode = vm["properties"]["osProfile"]["windowsConfiguration"]["patchSettings"]["patchMode"]
                            vm_os_automatic_updates = vm["properties"]["osProfile"]["windowsConfiguration"]["enableAutomaticUpdates"]
                        else:
                            vm_os_patch_mode = None
                            vm_os_automatic_updates = None
                    elif "linuxConfiguration" in vm["properties"]["osProfile"]:
                        if "patchSettings" in vm["properties"]["osProfile"]["linuxConfiguration"]:
                            vm_os_patch_mode = vm["properties"]["osProfile"]["linuxConfiguration"]["patchSettings"]["patchMode"]
                            vm_os_automatic_updates = None
                    else:
                        vm_os_patch_mode = None
                        vm_os_automatic_updates = None
                else:
                    vm_os_patch_mode = None
                    vm_os_automatic_updates = None
                vm_creation_time = vm["properties"]["timeCreated"]
                # Get VM Diagnostic Details
                if "diagnosticsProfile" in vm["properties"]:
                    if "bootDiagnostics" in vm["properties"]["diagnosticsProfile"]:
                        vm_os_boot_diag = vm["properties"]["diagnosticsProfile"]["bootDiagnostics"]["enabled"]
                    else:
                        vm_os_boot_diag = None
                    if "storageUri" in vm["properties"]["diagnosticsProfile"]["bootDiagnostics"]:
                        vm_os_boot_diag_sa_uri = vm["properties"]["diagnosticsProfile"]["bootDiagnostics"]["storageUri"]
                    else:
                        vm_os_boot_diag_sa_uri = None
                else:
                    vm_os_boot_diag = None
                    vm_os_boot_diag_sa_uri = None
                # Get VM Extension Details
                if "resources" in vm_response_to_json:
                    vm_extension_number = len(vm_response_to_json["resources"])
                    if vm_extension_number > 0:
                        vm_extension_list = []
                        for extensions in vm_response_to_json["resources"]:
                            vm_extension_list.append(extensions["name"])
                        vm_extension_name = ','.join(vm_extension_list)
                    else:
                        vm_extension_name = None
                else:
                    vm_extension_number = None
                    vm_extension_name = None
                # Get OS Disk Details
                if "osDisk" in vm["properties"]["storageProfile"]:
                    vm_os_disk_name = vm["properties"]["storageProfile"]["osDisk"]["name"]
                    if "managedDisk" in vm["properties"]["storageProfile"]["osDisk"]:
                        get_os_disk_details = requests.get(url = "https://management.azure.com"+vm["properties"]["storageProfile"]["osDisk"]["managedDisk"]["id"]+"?api-version=2021-12-01", headers = header)
                        get_os_disk_details_to_json = get_os_disk_details.json()
                        if get_os_disk_details.status_code == 200 or get_os_disk_details.status_code == 204:
                            vm_os_disk_location = get_os_disk_details_to_json["location"]
                            vm_os_disk_sku_name = get_os_disk_details_to_json["sku"]["name"]
                            vm_os_disk_sku_tier = get_os_disk_details_to_json["sku"]["tier"]
                            vm_os_disk_size = get_os_disk_details_to_json["properties"]["diskSizeGB"]
                            vm_os_disk_state = get_os_disk_details_to_json["properties"]["diskState"]
                        else:
                            vm_os_disk_location = None
                            vm_os_disk_sku_name = None
                            vm_os_disk_sku_tier = None
                            vm_os_disk_size = None
                            vm_os_disk_state = None
                    else:
                        vm_os_disk_location = None
                        vm_os_disk_sku_name = None
                        vm_os_disk_sku_tier = None
                        vm_os_disk_size = None
                        vm_os_disk_state = None
                else:
                    print("Unable to get VM os disk details - ", vm["name"])
                    vm_os_disk_name = ""+get_os_disk_details_to_json["error"]["code"]+" - "+get_os_disk_details_to_json["error"]["message"]+""
                # Get Additional Hard Disk Count
                if "dataDisks" in vm["properties"]["storageProfile"]:
                    vm_data_disk_num = len(vm["properties"]["storageProfile"]["dataDisks"])
                else:
                    vm_data_disk_num = None
                # Get Network Interfaces Count
                if "networkProfile" in vm["properties"]:
                    if "networkInterfaces" in vm["properties"]["networkProfile"]:
                        vm_ni_num = len(vm["properties"]["networkProfile"]["networkInterfaces"])
                    else:
                        vm_ni_num = None
                else:
                    vm_ni_num = None
                # Get VM Status
                get_vm_status = requests.get(url = "https://management.azure.com"+vm["id"]+"/instanceView?api-version=2022-08-01", headers = header)
                get_vm_status_to_json = get_vm_status.json()
                if get_vm_status.status_code == 200 or get_vm_status.status_code == 204:
                    if "statuses" in get_vm_status_to_json:
                        vm_status_list = []
                        for status_codes in get_vm_status_to_json["statuses"]:
                            vm_status_list.append(status_codes["displayStatus"])
                        vm_status = ','.join(vm_status_list)
                        vm_sql_status = ','.join(vm_status_list)
                    else:
                        vm_status = None
                        vm_sql_status = "Undefined"
                else:
                    print("Unable to get VM Status for - ", vm["name"])
                    vm_status = ""+get_vm_status_to_json["error"]["code"]+" - "+get_vm_status_to_json["error"]["message"]+""
                    vm_sql_status = ""+get_vm_status_to_json["error"]["code"]+" - "+get_vm_status_to_json["error"]["message"]+""
                # Get VM Tags
                get_vm_tags = requests.get(url = "https://management.azure.com"+vm["id"]+"/providers/Microsoft.Resources/tags/default?api-version=2021-04-01", headers = header)
                get_vm_tags_to_json = get_vm_tags.json()
                if get_vm_tags.status_code == 200 or get_vm_tags.status_code == 204:
                    if "properties" in get_vm_tags_to_json:
                        if "tags" in get_vm_tags_to_json["properties"]:
                            vm_tags = []
                            for key,value in get_vm_tags_to_json["properties"]["tags"].items():
                                vm_tag_value = ""+key+"="+value+""
                                vm_tags.append(vm_tag_value)
                            vm_tag_csv_value = '\n'.join(vm_tags)
                            vm_tag_sql_value = ','.join(vm_tags)
                        else:
                            vm_tag_csv_value = None
                            vm_tag_sql_value = "No Tags"
                    else:
                        vm_tag_csv_value = None
                        vm_tag_sql_value = "No Tags"
                else:
                    print("Unable to Get VM Tags for - ", vm["name"])
                    vm_tag_csv_value = ""+get_vm_tags_to_json["error"]["code"]+" - "+get_vm_tags_to_json["error"]["message"]+""
                    vm_tag_sql_value = ""+get_vm_tags_to_json["error"]["code"]+" - "+get_vm_tags_to_json["error"]["message"]+""
                # Get VM Locks
                get_vm_lock_details = requests.get(url = "https://management.azure.com"+vm["id"]+"/providers/Microsoft.Authorization/locks?api-version=2016-09-01", headers = header)
                get_vm_lock_resonse_to_json = get_vm_lock_details.json()
                if get_vm_lock_details.status_code == 200 or get_vm_lock_details.status_code == 204:
                    if get_vm_lock_resonse_to_json["value"]:
                        vm_locks = []
                        for lock in get_vm_lock_resonse_to_json["value"]:
                            lock_level = lock["properties"]["level"]
                            lock_name = lock["name"]
                            lock_scope = lock["id"]
                            lock_value = "Level="+lock_level+", Name="+lock_name+", Scope="+lock_scope+""
                            vm_locks.append(lock_value)
                        vm_lock_csv_value = '\n'.join(vm_locks)
                        vm_lock_sql_value = ','.join(vm_locks)
                    else:
                        vm_lock_csv_value = None
                        vm_lock_sql_value = "No Locks"
                else:
                    print("Unable to get VM Locks Details. Please check error..")
                    vm_lock_csv_value = ""+get_vm_lock_resonse_to_json["error"]["code"]+" - "+get_vm_lock_resonse_to_json["error"]["message"]+""
                    vm_lock_sql_value = ""+get_vm_lock_resonse_to_json["error"]["code"]+" - "+get_vm_lock_resonse_to_json["error"]["message"]+""
                # Write to CSV
                vm_excel_data = [subscription_name,vm_name,vm_id,vm_location,vm_rg_name,vm_status,vm_creation_time,vm_size,vm_os_publisher,vm_os_offer,vm_os_sku,vm_os_version,vm_os_exact_version,vm_os_patch_mode,vm_os_automatic_updates,vm_os_boot_diag,vm_os_boot_diag_sa_uri,vm_extension_number,vm_extension_name,vm_os_disk_name,vm_os_disk_location,vm_os_disk_sku_name,vm_os_disk_sku_tier,vm_os_disk_size,vm_os_disk_state,vm_data_disk_num,vm_ni_num,vm_tag_csv_value,vm_lock_csv_value]
                vm_sql_data = [subscription_name,vm_name,vm_id,vm_location,vm_rg_name,vm_sql_status,vm_creation_time,vm_size,vm_os_publisher,vm_os_offer,vm_os_sku,vm_os_version,vm_os_exact_version,vm_os_patch_mode,vm_os_automatic_updates,vm_os_boot_diag,vm_os_boot_diag_sa_uri,vm_extension_number,vm_extension_name,vm_os_disk_name,vm_os_disk_location,vm_os_disk_sku_name,vm_os_disk_sku_tier,vm_os_disk_size,vm_os_disk_state,vm_data_disk_num,vm_ni_num,vm_tag_sql_value,vm_lock_sql_value]
                print("Writing VM Details for - ", vm["name"])
                with open('Virtual Machines.csv', mode='a', newline='') as vm_excel_file_data:
                    csvwriter = csv.writer(vm_excel_file_data, delimiter=',')
                    csvwriter.writerow(vm_excel_data)
                with open('sql_vm_general.csv', mode='a', newline='') as vm_sql_file_data:
                    csvwriter = csv.writer(vm_sql_file_data, delimiter=',')
                    csvwriter.writerow(vm_sql_data)
        else:
            print("Blank API response received")
    else:
        print("Unable to get VM details")

def get_vm_data_disk(subscription_name, header):
    # Load the Saved Json file
    with open("vm.json") as vm_saved_json:
        vm_saved_json = json.load(vm_saved_json)
    # Create the CSV header
    vm_data_disk_excel_header = ['Subscription', 'VM Resource Group', 'Virtual Machine', 'Disk Resource Group', 'Disk Name', 'Disk Location', 'Disk Size(GB)', 'Disk Provisioning State', 'Disk State', 'Disk SKU Name', 'Disk SKu Tier', 'Disk Network Access Policy', 'Disk Public Network Access', 'Disk Encryption']
    vm_data_disk_sql_header = ['sub', 'vm_rg_name', 'vm_name', 'disk_rg_name', 'disk_name', 'disk_location', 'disk_size_gb', 'disk_provisioning_state', 'disk_state', 'disk_sku_name', 'disk_sku_tier', 'disk_nap', 'disk_pub_access_policy', 'disk_encryption']
    with open('Virtual Machine Data Disk.csv', mode='w', newline='') as vm_data_disk_excel_file_header:
        csvwriter = csv.writer(vm_data_disk_excel_file_header, delimiter=',')
        csvwriter.writerow(vm_data_disk_excel_header)
    with open('sql_vm_data_disk.csv', mode='w', newline='') as vm_data_disk_sql_file_header:
        csvwriter = csv.writer(vm_data_disk_sql_file_header, delimiter=',')
        csvwriter.writerow(vm_data_disk_sql_header)
    # Call the Disk API
    for vms in vm_saved_json["value"]:
        print("Getting Data Disk details of ", vms["name"])
        vm_name = vms["name"]
        vm_rg_name_split = vms["id"].split('/')
        vm_rg_name = vm_rg_name_split[4]
        if "dataDisks" in vms["properties"]["storageProfile"]:
            for disk in vms["properties"]["storageProfile"]["dataDisks"]:
                if "managedDisk" in disk:
                    get_vm_data_disk_details = requests.get(url = "https://management.azure.com"+disk["managedDisk"]["id"]+"?api-version=2021-12-01", headers = header)
                    get_vm_data_disk_details_to_json = get_vm_data_disk_details.json()
                    if get_vm_data_disk_details.status_code == 200 or get_vm_data_disk_details.status_code == 204:
                        data_disk_name = get_vm_data_disk_details_to_json["name"]
                        data_disk_rg_name_split = get_vm_data_disk_details_to_json["id"].split('/')
                        data_disk_rg_name = data_disk_rg_name_split[4]
                        data_disk_location = get_vm_data_disk_details_to_json["location"]
                        data_disk_sku_name = get_vm_data_disk_details_to_json["sku"]["name"]
                        data_disk_sku_tier = get_vm_data_disk_details_to_json["sku"]["tier"]
                        data_disk_size = get_vm_data_disk_details_to_json["properties"]["diskSizeGB"]
                        data_disk_encryption = get_vm_data_disk_details_to_json["properties"]["encryption"]["type"]
                        data_disk_network_access_policy = get_vm_data_disk_details_to_json["properties"]["networkAccessPolicy"]
                        data_disk_public_network_access = get_vm_data_disk_details_to_json["properties"]["publicNetworkAccess"]
                        data_disk_provisioning_state = get_vm_data_disk_details_to_json["properties"]["provisioningState"]
                        data_disk_state = get_vm_data_disk_details_to_json["properties"]["diskState"]
                        # Write to CSV
                        vm_data_disk_excel_data = [subscription_name,vm_rg_name,vm_name,data_disk_rg_name,data_disk_name,data_disk_location,data_disk_size,data_disk_provisioning_state,data_disk_state,data_disk_sku_name,data_disk_sku_tier,data_disk_network_access_policy,data_disk_public_network_access,data_disk_encryption]
                        vm_data_disk_sql_data = [subscription_name,vm_rg_name,vm_name,data_disk_rg_name,data_disk_name,data_disk_location,data_disk_size,data_disk_provisioning_state,data_disk_state,data_disk_sku_name,data_disk_sku_tier,data_disk_network_access_policy,data_disk_public_network_access,data_disk_encryption]
                        print("Writing Data Disk details for ", vms["name"])
                        with open('Virtual Machine Data Disk.csv', mode='a', newline='') as vm_data_disk_excel_file_data:
                            csvwriter = csv.writer(vm_data_disk_excel_file_data, delimiter=',')
                            csvwriter.writerow(vm_data_disk_excel_data)
                        with open('sql_vm_data_disk.csv', mode='a', newline='') as vm_data_disk_sql_file_data:
                            csvwriter = csv.writer(vm_data_disk_sql_file_data, delimiter=',')
                            csvwriter.writerow(vm_data_disk_sql_data)
                    else:
                        print("Error in API response for ", vm_name)
                        pass
                else:
                    print("No managed disk found for ", vm_name)
                    pass
        else:
            print("No Data Disk is found for ", vm_name)
            pass

def get_vm_network_interfaces(subscription_name, header):
    # Load the Saved Json file
    with open("vm.json") as vm_saved_json:
        vm_saved_json = json.load(vm_saved_json)
    # Create the CSV header
    vm_network_interface_excel_header = ['Subscription', 'VM Resource Group', 'Virtual Machine', 'NI Name', 'NI Resource Group', 'NI Primary', 'NI Location', 'NI Provisioning State', 'NI Accelarated Networking', 'NI VNET Encryption', 'NI IP Forwarding', 'NI NSG Name', 'NI NSG Resource Group', 'NI IP Config Name', 'NI IP Config Resource group', 'NI IP Config State', 'NI Private IP Address', 'NI DNS Servers', 'NI Private IP Allocation', 'NI IP Primary', 'NI Private IP Version', 'NI VNET Resource Group', 'NI VNET Name', 'NI Subnet Name', 'NI Public IP Resource Group', 'NI Public IP Name', 'NI Public IP Location', 'NI Public IP State', 'NI Public IP FQDN', 'NI Public IP Address', 'NI Public IP Version', 'NI Public IP Allocation', 'NI Public IP SKU Name', 'NI Public IP SKU Tier']
    vm_network_interface_sql_header = ['sub', 'vm_rg_name', 'vm_name', 'ni_name', 'ni_rg_name', 'ni_primary', 'ni_location', 'ni_provisioning_state', 'ni_accelarated_networking', 'ni_vnet_encryption', 'ni_ip_forwarding', 'ni_nsg_name', 'ni_nsg_rg_name', 'ni_ip_config_name', 'ni_ip_config_rg_name', 'ni_ip_config_state', 'ni_private_ip', 'ni_dns_server', 'ni_private_ip_allocation', 'ni_ip_primary', 'ni_private_ip_version', 'ni_vnet_rg_name', 'ni_vnet_name', 'ni_subnet_name', 'ni_pip_rg_name', 'ni_pip_name', 'ni_pip_location', 'ni_pip_state', 'ni_pip_fqdn', 'ni_pip_address', 'ni_pip_version', 'ni_pip_allocation', 'ni_pip_sku_name', 'ni_pip_sku_tier']
    with open('VM Network Interfaces.csv', mode='w', newline='') as vm_ni_excel_file_header:
        csvwriter = csv.writer(vm_ni_excel_file_header, delimiter=',')
        csvwriter.writerow(vm_network_interface_excel_header)
    with open('sql_vm_network_interfaces.csv', mode='w', newline='') as vm_ni_sql_file_header:
        csvwriter = csv.writer(vm_ni_sql_file_header, delimiter=',')
        csvwriter.writerow(vm_network_interface_sql_header)
    for vms in vm_saved_json["value"]:
        print("Getting Network Interface details of ", vms["name"])
        vm_name = vms["name"]
        vm_rg_name_split = vms["id"].split('/')
        vm_rg_name = vm_rg_name_split[4]
        if "networkProfile" in vms["properties"]:
            for ni in vms["properties"]["networkProfile"]["networkInterfaces"]:
                get_vm_ni_details = requests.get(url = "https://management.azure.com"+ni["id"]+"?api-version=2022-07-01", headers = header)
                get_vm_ni_details_to_json = get_vm_ni_details.json()
                if get_vm_ni_details.status_code == 200 or get_vm_ni_details.status_code == 204:
                    ni_name = get_vm_ni_details_to_json["name"]
                    ni_rg_name_split = get_vm_ni_details_to_json["id"].split('/')
                    ni_rg_name = ni_rg_name_split[4]
                    ni_location = get_vm_ni_details_to_json["location"]
                    ni_provisioning_state = get_vm_ni_details_to_json["properties"]["provisioningState"]
                    if "dnsServers" in get_vm_ni_details_to_json["properties"]["dnsSettings"]:
                        ni_dns_servers = ''.join(get_vm_ni_details_to_json["properties"]["dnsSettings"]["dnsServers"])
                    else:
                        ni_dns_servers = None
                    ni_accelerated_networking = str(get_vm_ni_details_to_json["properties"]["enableAcceleratedNetworking"])
                    ni_vnet_encryption = str(get_vm_ni_details_to_json["properties"]["vnetEncryptionSupported"])
                    ni_ip_forwarding = get_vm_ni_details_to_json["properties"]["enableIPForwarding"]
                    if "networkSecurityGroup" in get_vm_ni_details_to_json["properties"]:
                        ni_nsg_name_split = get_vm_ni_details_to_json["properties"]["networkSecurityGroup"]["id"].split('/')
                        ni_nsg_rg_name = ni_nsg_name_split[4]
                        ni_nsg_name = ni_nsg_name_split[-1]
                    else:
                        ni_nsg_rg_name = None
                        ni_nsg_name = None
                    ni_primary = get_vm_ni_details_to_json["properties"]["primary"]
                    if "ipConfigurations" in get_vm_ni_details_to_json["properties"]:
                        for ip in get_vm_ni_details_to_json["properties"]["ipConfigurations"]:
                            ni_ip_name = ip["name"]
                            ni_ip_rg_name_split = ip["id"].split('/')
                            ni_ip_rg_name = ni_ip_rg_name_split[4]
                            ni_ip_provisioning_state = ip["properties"]["provisioningState"]
                            ni_ip_private_ip_address = ip["properties"]["privateIPAddress"]
                            ni_ip_private_ip_allocation = ip["properties"]["privateIPAllocationMethod"]
                            ni_ip_primary = ip["properties"]["primary"]
                            ni_ip_private_ip_version = ip["properties"]["privateIPAddressVersion"]
                            ni_ip_vnet_subnet_name_split = ip["properties"]["subnet"]["id"].split('/')
                            ni_ip_vnet_rg_name = ni_ip_vnet_subnet_name_split[4]
                            ni_ip_subnet_name = ni_ip_vnet_subnet_name_split[-1]
                            ni_ip_vnet_name = ni_ip_vnet_subnet_name_split[8]
                            if "publicIPAddress" in ip["properties"]:
                                get_ni_public_ip_details = requests.get(url = "https://management.azure.com"+ip["properties"]["publicIPAddress"]["id"]+"?api-version=2022-07-01", headers = header)
                                get_ni_public_ip_details_to_json = get_ni_public_ip_details.json()
                                if get_ni_public_ip_details.status_code == 200 or get_ni_public_ip_details.status_code == 204:
                                    ni_pip_name = get_ni_public_ip_details_to_json["name"]
                                    ni_pip_location = get_ni_public_ip_details_to_json["location"]
                                    ni_pip_rg_name_split = get_ni_public_ip_details_to_json["id"].split('/')
                                    ni_pip_rg_name = ni_pip_rg_name_split[4]
                                    ni_pip_provisioning_state = get_ni_public_ip_details_to_json["properties"]["provisioningState"]
                                    if "ipAddress" in get_ni_public_ip_details_to_json["properties"]:
                                        ni_pip_address = get_ni_public_ip_details_to_json["properties"]["ipAddress"]
                                    else:
                                        ni_pip_address = None
                                    if "publicIPAddressVersion" in get_ni_public_ip_details_to_json["properties"]:
                                        ni_pip_version = get_ni_public_ip_details_to_json["properties"]["publicIPAddressVersion"]
                                    else:
                                        ni_pip_version = None
                                    if "publicIPAllocationMethod" in get_ni_public_ip_details_to_json["properties"]:
                                        ni_pip_allocation = get_ni_public_ip_details_to_json["properties"]["publicIPAllocationMethod"]
                                    else:
                                        ni_pip_allocation = None
                                    ni_pip_sku_name = get_ni_public_ip_details_to_json["sku"]["name"]
                                    ni_pip_sku_tier = get_ni_public_ip_details_to_json["sku"]["tier"]
                                    if "dnsSettings" in get_ni_public_ip_details_to_json["properties"]:
                                        ni_pip_fqdn = get_ni_public_ip_details_to_json["properties"]["dnsSettings"]["fqdn"]
                                    else:
                                        ni_pip_fqdn = None
                                else:
                                    ni_pip_name = None
                                    ni_pip_location = None
                                    ni_pip_rg_name = None
                                    ni_pip_provisioning_state = None
                                    ni_pip_address = None
                                    ni_pip_version = None
                                    ni_pip_allocation = None
                                    ni_pip_sku_name = None
                                    ni_pip_sku_tier = None
                                    ni_pip_fqdn = None
                            else:
                                ni_pip_name = None
                                ni_pip_location = None
                                ni_pip_rg_name = None
                                ni_pip_provisioning_state = None
                                ni_pip_address = None
                                ni_pip_version = None
                                ni_pip_allocation = None
                                ni_pip_sku_name = None
                                ni_pip_sku_tier = None
                                ni_pip_fqdn = None
                        # Write to CSV
                        vm_ni_excel_data = [subscription_name,vm_rg_name,vm_name,ni_name,ni_rg_name,ni_primary,ni_location,ni_provisioning_state,ni_accelerated_networking,ni_vnet_encryption,ni_ip_forwarding,ni_nsg_name,ni_nsg_rg_name,ni_ip_name,ni_ip_rg_name,ni_ip_provisioning_state,ni_ip_private_ip_address,ni_dns_servers,ni_ip_private_ip_allocation,ni_ip_primary,ni_ip_private_ip_version,ni_ip_vnet_rg_name,ni_ip_vnet_name,ni_ip_subnet_name,ni_pip_rg_name,ni_pip_name,ni_pip_location,ni_pip_provisioning_state,ni_pip_fqdn,ni_pip_address,ni_pip_version,ni_pip_allocation,ni_pip_sku_name,ni_pip_sku_tier]
                        vm_ni_sql_data = [subscription_name,vm_rg_name,vm_name,ni_name,ni_rg_name,ni_primary,ni_location,ni_provisioning_state,ni_accelerated_networking,ni_vnet_encryption,ni_ip_forwarding,ni_nsg_name,ni_nsg_rg_name,ni_ip_name,ni_ip_rg_name,ni_ip_provisioning_state,ni_ip_private_ip_address,ni_dns_servers,ni_ip_private_ip_allocation,ni_ip_primary,ni_ip_private_ip_version,ni_ip_vnet_rg_name,ni_ip_vnet_name,ni_ip_subnet_name,ni_pip_rg_name,ni_pip_name,ni_pip_location,ni_pip_provisioning_state,ni_pip_fqdn,ni_pip_address,ni_pip_version,ni_pip_allocation,ni_pip_sku_name,ni_pip_sku_tier]
                        print("Writing Network Interface details for ", vm_name)
                        with open('VM Network Interfaces.csv', mode='a', newline='') as vm_network_interface_excel_file_data:
                            csvwriter = csv.writer(vm_network_interface_excel_file_data, delimiter=',')
                            csvwriter.writerow(vm_ni_excel_data)
                        with open('sql_vm_network_interfaces.csv', mode='a', newline='') as vm_network_interface_sql_file_data:
                            csvwriter = csv.writer(vm_network_interface_sql_file_data, delimiter=',')
                            csvwriter.writerow(vm_ni_sql_data)
                    else:
                        ni_ip_name = None
                        ni_ip_rg_name = None
                        ni_ip_provisioning_state = None
                        ni_ip_private_ip_address = None
                        ni_ip_private_ip_allocation = None
                        ni_ip_primary = None
                        ni_ip_private_ip_version = None
                        ni_ip_vnet_rg_name = None
                        ni_ip_subnet_name = None
                        ni_ip_vnet_name = None
                        ni_pip_name = None
                        ni_pip_location = None
                        ni_pip_rg_name = None
                        ni_pip_provisioning_state = None
                        ni_pip_address = None
                        ni_pip_version = None
                        ni_pip_allocation = None
                        ni_pip_sku_name = None
                        ni_pip_sku_tier = None
                        ni_pip_fqdn = None
                        # Write to CSV
                        vm_ni_excel_data = [subscription_name,vm_rg_name,vm_name,ni_name,ni_rg_name,ni_primary,ni_location,ni_provisioning_state,ni_accelerated_networking,ni_vnet_encryption,ni_ip_forwarding,ni_nsg_name,ni_nsg_rg_name,ni_ip_name,ni_ip_rg_name,ni_ip_provisioning_state,ni_ip_private_ip_address,ni_dns_servers,ni_ip_private_ip_allocation,ni_ip_primary,ni_ip_private_ip_version,ni_ip_vnet_rg_name,ni_ip_vnet_name,ni_ip_subnet_name,ni_pip_rg_name,ni_pip_name,ni_pip_location,ni_pip_provisioning_state,ni_pip_fqdn,ni_pip_address,ni_pip_version,ni_pip_allocation,ni_pip_sku_name,ni_pip_sku_tier]
                        vm_ni_sql_data = [subscription_name,vm_rg_name,vm_name,ni_name,ni_rg_name,ni_primary,ni_location,ni_provisioning_state,ni_accelerated_networking,ni_vnet_encryption,ni_ip_forwarding,ni_nsg_name,ni_nsg_rg_name,ni_ip_name,ni_ip_rg_name,ni_ip_provisioning_state,ni_ip_private_ip_address,ni_dns_servers,ni_ip_private_ip_allocation,ni_ip_primary,ni_ip_private_ip_version,ni_ip_vnet_rg_name,ni_ip_vnet_name,ni_ip_subnet_name,ni_pip_rg_name,ni_pip_name,ni_pip_location,ni_pip_provisioning_state,ni_pip_fqdn,ni_pip_address,ni_pip_version,ni_pip_allocation,ni_pip_sku_name,ni_pip_sku_tier]
                        print("Writing Network Interface details for ", vm_name)
                        with open('VM Network Interfaces.csv', mode='a', newline='') as vm_network_interface_excel_file_data:
                            csvwriter = csv.writer(vm_network_interface_excel_file_data, delimiter=',')
                            csvwriter.writerow(vm_ni_excel_data)
                        with open('sql_vm_network_interfaces.csv', mode='a', newline='') as vm_network_interface_sql_file_data:
                            csvwriter = csv.writer(vm_network_interface_sql_file_data, delimiter=',')
                            csvwriter.writerow(vm_ni_sql_data)
                else:
                    print("Unable to get VM Network Interface Details")
                    pass
        else:
            print("No Network Interface Details Found")

def get_vm_metrics(subscription_name,header):
    # Load the Saved Json file
    with open("vm.json") as vm_saved_json:
        vm_saved_json = json.load(vm_saved_json)
    # Create CSV header
    vm_metrics_excel_header = ["Subscription", "Resource Group", "VM Name", "Metrics Name", "Metrics Description", "Timestamp", "Minimum", "Average", "Maximum"]
    vm_metrics_sql_header = ["sub", "rg_name", "vm_name", "metrics_name", "metrics_description", "timestamp", "minimum", "average", "maximum"]
    with open('VM Metrics.csv', mode='w', newline='') as vm_metrics_excel_file_header:
        csvwriter = csv.writer(vm_metrics_excel_file_header, delimiter=',')
        csvwriter.writerow(vm_metrics_excel_header)
    with open('sql_vm_metrics.csv', mode='w', newline='') as vm_metrics_sql_file_header:
        csvwriter = csv.writer(vm_metrics_sql_file_header, delimiter=',')
        csvwriter.writerow(vm_metrics_sql_header)
    # Some Dates to begin with
    date_today = date.today()
    date_yesterday = date_today - timedelta(days = 1)
    for vms in vm_saved_json["value"]:
        vm_name = vms["name"]
        vm_rg_name_split = vms["id"].split('/')
        vm_rg_name = vm_rg_name_split[4]
        # CPU and Memory Usage Percentage
        print("Getting VM Metrics for ", vms["name"])
        get_vm_metrics = requests.get(url = "https://management.azure.com"+vms["id"]+"/providers/Microsoft.Insights/metrics?api-version=2018-01-01&timespan="+str(date_yesterday)+"T00:00:00Z/"+str(date_today)+"T00:00:00Z&interval=PT1H&metricnames=Percentage CPU,Available memory Bytes&aggregation=Maximum,Minimum,Average", headers = header)
        get_vm_metrics_to_json = get_vm_metrics.json()
        if get_vm_metrics.status_code == 200 or get_vm_metrics.status_code == 204:
            if "value" in get_vm_metrics_to_json:
                for metric_type in get_vm_metrics_to_json["value"]:
                    if metric_type["name"]["value"] == "Percentage CPU":
                        for metrics in metric_type["timeseries"]:
                            if "data" in metrics:
                                for data in metrics["data"]:
                                    if "minimum" in data:
                                        minimum = data["minimum"]
                                    else:
                                        minimum = float(0)
                                    if "average" in data:
                                        average = data["average"]
                                    else:
                                        average = float(0)
                                    if "maximum" in data:
                                        maximum = data["maximum"]
                                    else:
                                        maximum = float(0)
                                    vm_metrics_excel_data = [subscription_name, vm_rg_name, vm_name, metric_type["name"]["value"],metric_type["displayDescription"], data["timeStamp"], minimum, average, maximum]
                                    vm_metrics_sql_data = [subscription_name, vm_rg_name, vm_name, metric_type["name"]["value"],metric_type["displayDescription"], data["timeStamp"], minimum, average, maximum]
                                    with open('VM Metrics.csv', mode='a', newline='') as vm_metrics_excel_file_data:
                                        csvwriter = csv.writer(vm_metrics_excel_file_data, delimiter=',')
                                        csvwriter.writerow(vm_metrics_excel_data)
                                    with open('sql_vm_metrics.csv', mode='a', newline='') as vm_metrics_sql_file_data:
                                        csvwriter = csv.writer(vm_metrics_sql_file_data, delimiter=',')
                                        csvwriter.writerow(vm_metrics_sql_data)
                            else:
                                print("No Metrics Found in API Response for ", vms["name"])
                                pass
                    elif metric_type["name"]["value"] == "Available Memory Bytes":
                        for metrics in metric_type["timeseries"]:
                            if "data" in metrics:
                                for data in metrics["data"]:
                                    if "minimum" in data:
                                        minimum = data["minimum"] / 1024 / 1024 / 1024
                                    else:
                                        minimum = float(0)
                                    if "average" in data:
                                        average = data["average"] / 1024 / 1024 / 1024
                                    else:
                                        average = float(0)
                                    if "maximum" in data:
                                        maximum = data["maximum"] / 1024 / 1024 / 1024
                                    else:
                                        maximum = float(0)
                                    vm_metrics_excel_data = [subscription_name, vm_rg_name, vm_name, metric_type["name"]["value"],metric_type["displayDescription"], data["timeStamp"], minimum, average, maximum]
                                    vm_metrics_sql_data = [subscription_name, vm_rg_name, vm_name, metric_type["name"]["value"],metric_type["displayDescription"], data["timeStamp"], minimum, average, maximum]
                                    with open('VM Metrics.csv', mode='a', newline='') as vm_metrics_excel_file_data:
                                        csvwriter = csv.writer(vm_metrics_excel_file_data, delimiter=',')
                                        csvwriter.writerow(vm_metrics_excel_data)
                                    with open('sql_vm_metrics.csv', mode='a', newline='') as vm_metrics_sql_file_data:
                                        csvwriter = csv.writer(vm_metrics_sql_file_data, delimiter=',')
                                        csvwriter.writerow(vm_metrics_sql_data)
                            else:
                                print("No Metrics Found in API Response for ", vms["name"])
                                pass
            else:
                print("No Value found in API Response for ", vms["name"])
                pass
        else:
            print("Error Getting VM Metrics Details for ", vms["name"])
            pass


