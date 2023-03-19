import requests
import json
import sys
import csv
import os

def get_vmss(subscription_id,subscription_name,header):
    print("Getting Virtual Machine Scale Set Details for ", subscription_name)
    # Write CSV Header
    vmss_excel_header = ["Subscription", "Resource Group", "Name", "Location", "Provisioning State", "SKU Name", "SKU Tier", "SKU Capacity", "Fault Domain Count", "Upgrade Policy", "Creation Time", "Tags"]
    vmss_sql_header = ["sub", "rg_name", "vmss_name", "vmss_location", "vmss_provisioning_state", "vmss_sku_name", "vmss_sku_tier", "vmss_sku_capacity", "vmss_fault_domain_count", "vmss_upgrade_policy", "vmss_creation_time", "tags"]
    vmss_vm_excel_header = ["Subscription", "Resource Group", "Scale Set Name", "Name", "Location", "SKU Name", "SKU Tier", "Size", "OS Publisher", "OS Offer", "OS SKU", "OS Version", "OS Exact Version", "Tags"]
    vmss_vm_sql_header = ["sub", "rg_name", "vmss_name", "vm_name", "vm_location", "vm_sku_name", "vm_sku_tier", "vm_size", "vm_os_publisher", "vm_os_offer", "vm_os_sku", "vm_os_version", "vm_os_exact_version", "tags"]
    with open('Virtual Machine Scale Set.csv', mode='w', newline='') as vmss_excel_file_header:
        csvwriter = csv.writer(vmss_excel_file_header, delimiter=',')
        csvwriter.writerow(vmss_excel_header)
    with open('sql_vmss.csv', mode='w', newline='') as vmss_sql_file_header:
        csvwriter = csv.writer(vmss_sql_file_header, delimiter=',')
        csvwriter.writerow(vmss_sql_header)
    with open('VMSS Virtual Machines.csv', mode='w', newline='') as vmss_vm_excel_file_header:
        csvwriter = csv.writer(vmss_vm_excel_file_header, delimiter=',')
        csvwriter.writerow(vmss_vm_excel_header)
    with open('sql_vmss_vm.csv', mode='w', newline='') as vmss_vm_sql_file_header:
        csvwriter = csv.writer(vmss_vm_sql_file_header, delimiter=',')
        csvwriter.writerow(vmss_vm_sql_header)
    # Get Started
    get_vmss_details = requests.get(url = "https://management.azure.com/subscriptions/"+subscription_id+"/providers/Microsoft.Compute/virtualMachineScaleSets?api-version=2022-11-01", headers = header)
    get_vmss_details_to_json = get_vmss_details.json()
    if get_vmss_details.status_code == 200 or get_vmss_details.status_code == 204:
        if "value" in get_vmss_details_to_json:
            for vmss in get_vmss_details_to_json["value"]:
                vmss_name = vmss["name"]
                vmss_rg_name_split = vmss["id"].split('/')
                vmss_rg_name = vmss_rg_name_split[4]
                vmss_location = vmss["location"]
                if "tags" in vmss:
                    all_tags = []
                    for key,value in vmss["tags"].items():
                        tag_value = ""+key+"="+value+""
                        all_tags.append(tag_value)
                    tag_csv_value = '\n'.join(all_tags)
                    tag_sql_value = ','.join(all_tags)
                else:
                    tag_csv_value = str()
                    tag_sql_value = "No Tags"
                if "sku" in vmss:
                    if "name" in vmss["sku"]:
                        vmss_sku_name = vmss["sku"]["name"]
                    else:
                        vmss_sku_name = None
                    if "tier" in vmss["sku"]:
                        vmss_sku_tier = vmss["sku"]["tier"]
                    else:
                        vmss_sku_tier = None
                    if "capacity" in vmss["sku"]:
                        vmss_sku_capacity = vmss["sku"]["capacity"]
                    else:
                        vmss_sku_capacity = None
                else:
                    vmss_sku_name = None
                    vmss_sku_tier = None
                    vmss_sku_capacity = None
                if "properties" in vmss:
                    if "provisioningState" in vmss["properties"]:
                        vmss_provisioning_state = vmss["properties"]["provisioningState"]
                    else:
                        vmss_provisioning_state = None
                    if "platformFaultDomainCount" in vmss["properties"]:
                        vmss_fault_domain_count = vmss["properties"]["platformFaultDomainCount"]
                    else:
                        vmss_fault_domain_count = None
                    if "timeCreated" in vmss["properties"]:
                        vmss_creation_time = vmss["properties"]["timeCreated"]
                    else:
                        vmss_creation_time = None
                    if "upgradePolicy" in vmss["properties"]:
                        if "mode" in vmss["properties"]["upgradePolicy"]:
                            vmss_upgrade_policy = vmss["properties"]["upgradePolicy"]["mode"]
                        else:
                            vmss_upgrade_policy = None
                    else:
                        vmss_upgrade_policy = None
                else:
                    vmss_provisioning_state = None
                    vmss_fault_domain_count = None
                    vmss_creation_time = None
                    vmss_upgrade_policy = None
                # Write Data to CSV
                print("Writing VMSS Data for ", vmss_name)
                vmss_excel_data = [subscription_name, vmss_rg_name, vmss_name, vmss_location, vmss_provisioning_state, vmss_sku_name, vmss_sku_tier, vmss_sku_capacity, vmss_fault_domain_count, vmss_upgrade_policy, vmss_creation_time, tag_csv_value]
                vmss_sql_data = [subscription_name, vmss_rg_name, vmss_name, vmss_location, vmss_provisioning_state, vmss_sku_name, vmss_sku_tier, vmss_sku_capacity, vmss_fault_domain_count, vmss_upgrade_policy, vmss_creation_time, tag_sql_value]
                with open('Virtual Machine Scale Set.csv', mode='a', newline='') as vmss_excel_file_data:
                    csvwriter = csv.writer(vmss_excel_file_data, delimiter=',')
                    csvwriter.writerow(vmss_excel_data)
                with open('sql_vmss.csv', mode='a', newline='') as vmss_sql_file_data:
                    csvwriter = csv.writer(vmss_sql_file_data, delimiter=',')
                    csvwriter.writerow(vmss_sql_data)
                
                # Get VM OS Details
                print("Getting Scale Set Virtual Machine Details for ", vmss_name)
                get_vmss_vm_details = requests.get(url = "https://management.azure.com"+vmss["id"]+"/virtualMachines?api-version=2022-11-01", headers = header)
                get_vmss_vm_details_to_json = get_vmss_vm_details.json()
                if get_vmss_vm_details.status_code == 200 or get_vmss_vm_details.status_code == 204:
                    if "value" in get_vmss_vm_details_to_json:
                        for vmss_vm in get_vmss_vm_details_to_json["value"]:
                            vmss_vm_name = vmss_vm["name"]
                            vmss_vm_location = vmss_vm["location"]
                            if "tags" in vmss_vm:
                                all_tags = []
                                for key,value in vmss_vm["tags"].items():
                                    tag_value = ""+key+"="+value+""
                                    all_tags.append(tag_value)
                                tag_csv_value = '\n'.join(all_tags)
                                tag_sql_value = ','.join(all_tags)
                            else:
                                tag_csv_value = str()
                                tag_sql_value = "No Tags"
                            if "sku" in vmss_vm:
                                if "name" in vmss_vm["sku"]:
                                    vmss_vm_sku_name = vmss_vm["sku"]["name"]
                                else:
                                    vmss_vm_sku_name = None
                                if "tier" in vmss_vm["sku"]:
                                    vmss_vm_sku_tier = vmss_vm["sku"]["tier"]
                                else:
                                    vmss_vm_sku_tier = None
                            else:
                                vmss_vm_sku_name = None
                                vmss_vm_sku_tier = None
                            if "properties" in vmss_vm:
                                if "hardwareProfile" in vmss_vm["properties"]:
                                    if "vmSize" in vmss_vm["properties"]["hardwareProfile"]:
                                        vmss_vm_size = vmss_vm["properties"]["hardwareProfile"]["vmSize"]
                                    else:
                                        vmss_vm_size = None
                                else:
                                    vmss_vm_size = None
                                if "storageProfile" in vmss_vm["properties"]:
                                    if "imageReference" in vmss_vm["properties"]["storageProfile"]:
                                        if "publisher" in vmss_vm["properties"]["storageProfile"]["imageReference"]:
                                            vmss_vm_os_publisher = vmss_vm["properties"]["storageProfile"]["imageReference"]["publisher"]
                                        else:
                                            vmss_vm_os_publisher = None
                                        if "offer" in vmss_vm["properties"]["storageProfile"]["imageReference"]:
                                            vmss_vm_os_offer = vmss_vm["properties"]["storageProfile"]["imageReference"]["offer"]
                                        else:
                                            vmss_vm_os_offer = None
                                        if "sku" in vmss_vm["properties"]["storageProfile"]["imageReference"]:
                                            vmss_vm_os_sku = vmss_vm["properties"]["storageProfile"]["imageReference"]["sku"]
                                        else:
                                            vmss_vm_os_sku = None
                                        if "version" in vmss_vm["properties"]["storageProfile"]["imageReference"]:
                                            vmss_vm_os_version = vmss_vm["properties"]["storageProfile"]["imageReference"]["version"]
                                        else:
                                            vmss_vm_os_version = None
                                        if "exactVersion" in vmss_vm["properties"]["storageProfile"]["imageReference"]:
                                            vmss_vm_os_exact_version = vmss_vm["properties"]["storageProfile"]["imageReference"]["exactVersion"]
                                        else:
                                            vmss_vm_os_exact_version = None
                                    else:
                                        vmss_vm_os_publisher = None
                                        vmss_vm_os_offer = None
                                        vmss_vm_os_sku = None
                                        vmss_vm_os_version = None
                                        vmss_vm_os_exact_version = None
                                else:
                                    vmss_vm_os_publisher = None
                                    vmss_vm_os_offer = None
                                    vmss_vm_os_sku = None
                                    vmss_vm_os_version = None
                                    vmss_vm_os_exact_version = None
                            else:
                                vmss_vm_size = None
                                vmss_vm_os_publisher = None
                                vmss_vm_os_offer = None
                                vmss_vm_os_sku = None
                                vmss_vm_os_version = None
                                vmss_vm_os_exact_version = None
                            # Write Data to CSV
                            print("Writing Scale Set Virtual Machine Details for ", vmss_name)
                            vmss_vm_excel_data = [subscription_name, vmss_rg_name, vmss_name, vmss_vm_name, vmss_vm_location, vmss_vm_sku_name, vmss_vm_sku_tier, vmss_vm_size, vmss_vm_os_publisher, vmss_vm_os_offer, vmss_vm_os_sku, vmss_vm_os_version, vmss_vm_os_exact_version, tag_csv_value]
                            vmss_vm_sql_data = [subscription_name, vmss_rg_name, vmss_name, vmss_vm_name, vmss_vm_location, vmss_vm_sku_name, vmss_vm_sku_tier, vmss_vm_size, vmss_vm_os_publisher, vmss_vm_os_offer, vmss_vm_os_sku, vmss_vm_os_version, vmss_vm_os_exact_version, tag_sql_value]
                            with open('VMSS Virtual Machines.csv', mode='a', newline='') as vmss_vm_excel_file_data:
                                csvwriter = csv.writer(vmss_vm_excel_file_data, delimiter=',')
                                csvwriter.writerow(vmss_vm_excel_data)
                            with open('sql_vmss_vm.csv', mode='a', newline='') as vmss_vm_sql_file_data:
                                csvwriter = csv.writer(vmss_vm_sql_file_data, delimiter=',')
                                csvwriter.writerow(vmss_vm_sql_data)
                    else:
                        print("No Virtual Machine found for VMMS ", vmss_name)
                        pass
                else:
                    print("Error Getting API Response for VMSS VM for ", vmss_name)
                    pass

            while "nextLink" in get_vmss_details_to_json:
                print("Next Link Found. Querying API for more Data")
                get_vmss_details = requests.get(url = get_vmss_details_to_json["nextLink"], headers = header)
                get_vmss_details_to_json = get_vmss_details.json()
                if get_vmss_details.status_code == 200 or get_vmss_details.status_code == 204:
                    if "value" in get_vmss_details_to_json:
                        for vmss in get_vmss_details_to_json["value"]:
                            vmss_name = vmss["name"]
                            vmss_rg_name_split = vmss["id"].split('/')
                            vmss_rg_name = vmss_rg_name_split[4]
                            vmss_location = vmss["location"]
                            if "tags" in vmss:
                                all_tags = []
                                for key,value in vmss["tags"].items():
                                    tag_value = ""+key+"="+value+""
                                    all_tags.append(tag_value)
                                tag_csv_value = '\n'.join(all_tags)
                                tag_sql_value = ','.join(all_tags)
                            else:
                                tag_csv_value = str()
                                tag_sql_value = "No Tags"
                            if "sku" in vmss:
                                if "name" in vmss["sku"]:
                                    vmss_sku_name = vmss["sku"]["name"]
                                else:
                                    vmss_sku_name = None
                                if "tier" in vmss["sku"]:
                                    vmss_sku_tier = vmss["sku"]["tier"]
                                else:
                                    vmss_sku_tier = None
                                if "capacity" in vmss["sku"]:
                                    vmss_sku_capacity = vmss["sku"]["capacity"]
                                else:
                                    vmss_sku_capacity = None
                            else:
                                vmss_sku_name = None
                                vmss_sku_tier = None
                                vmss_sku_capacity = None
                            if "properties" in vmss:
                                if "provisioningState" in vmss["properties"]:
                                    vmss_provisioning_state = vmss["properties"]["provisioningState"]
                                else:
                                    vmss_provisioning_state = None
                                if "platformFaultDomainCount" in vmss["properties"]:
                                    vmss_fault_domain_count = vmss["properties"]["platformFaultDomainCount"]
                                else:
                                    vmss_fault_domain_count = None
                                if "timeCreated" in vmss["properties"]:
                                    vmss_creation_time = vmss["properties"]["timeCreated"]
                                else:
                                    vmss_creation_time = None
                                if "upgradePolicy" in vmss["properties"]:
                                    if "mode" in vmss["properties"]["upgradePolicy"]:
                                        vmss_upgrade_policy = vmss["properties"]["upgradePolicy"]["mode"]
                                    else:
                                        vmss_upgrade_policy = None
                                else:
                                    vmss_upgrade_policy = None
                            else:
                                vmss_provisioning_state = None
                                vmss_fault_domain_count = None
                                vmss_creation_time = None
                                vmss_upgrade_policy = None
                            # Write Data to CSV
                            print("Writing VMSS Data for ", vmss_name)
                            vmss_excel_data = [subscription_name, vmss_rg_name, vmss_name, vmss_location, vmss_provisioning_state, vmss_sku_name, vmss_sku_tier, vmss_sku_capacity, vmss_fault_domain_count, vmss_upgrade_policy, vmss_creation_time, tag_csv_value]
                            vmss_sql_data = [subscription_name, vmss_rg_name, vmss_name, vmss_location, vmss_provisioning_state, vmss_sku_name, vmss_sku_tier, vmss_sku_capacity, vmss_fault_domain_count, vmss_upgrade_policy, vmss_creation_time, tag_sql_value]
                            with open('Virtual Machine Scale Set.csv', mode='a', newline='') as vmss_excel_file_data:
                                csvwriter = csv.writer(vmss_excel_file_data, delimiter=',')
                                csvwriter.writerow(vmss_excel_data)
                            with open('sql_vmss.csv', mode='a', newline='') as vmss_sql_file_data:
                                csvwriter = csv.writer(vmss_sql_file_data, delimiter=',')
                                csvwriter.writerow(vmss_sql_data)
                            
                            # Get VM OS Details
                            print("Getting Scale Set Virtual Machine Details for ", vmss_name)
                            get_vmss_vm_details = requests.get(url = "https://management.azure.com"+vmss["id"]+"/virtualMachines?api-version=2022-11-01", headers = header)
                            get_vmss_vm_details_to_json = get_vmss_vm_details.json()
                            if get_vmss_vm_details.status_code == 200 or get_vmss_vm_details.status_code == 204:
                                if "value" in get_vmss_vm_details_to_json:
                                    for vmss_vm in get_vmss_vm_details_to_json["value"]:
                                        vmss_vm_name = vmss_vm["name"]
                                        vmss_vm_location = vmss_vm["location"]
                                        if "tags" in vmss_vm:
                                            all_tags = []
                                            for key,value in vmss_vm["tags"].items():
                                                tag_value = ""+key+"="+value+""
                                                all_tags.append(tag_value)
                                            tag_csv_value = '\n'.join(all_tags)
                                            tag_sql_value = ','.join(all_tags)
                                        else:
                                            tag_csv_value = str()
                                            tag_sql_value = "No Tags"
                                        if "sku" in vmss_vm:
                                            if "name" in vmss_vm["sku"]:
                                                vmss_vm_sku_name = vmss_vm["sku"]["name"]
                                            else:
                                                vmss_vm_sku_name = None
                                            if "tier" in vmss_vm["sku"]:
                                                vmss_vm_sku_tier = vmss_vm["sku"]["tier"]
                                            else:
                                                vmss_vm_sku_tier = None
                                        else:
                                            vmss_vm_sku_name = None
                                            vmss_vm_sku_tier = None
                                        if "properties" in vmss_vm:
                                            if "hardwareProfile" in vmss_vm["properties"]:
                                                if "vmSize" in vmss_vm["properties"]["hardwareProfile"]:
                                                    vmss_vm_size = vmss_vm["properties"]["hardwareProfile"]["vmSize"]
                                                else:
                                                    vmss_vm_size = None
                                            else:
                                                vmss_vm_size = None
                                            if "storageProfile" in vmss_vm["properties"]:
                                                if "imageReference" in vmss_vm["properties"]["storageProfile"]:
                                                    if "publisher" in vmss_vm["properties"]["storageProfile"]["imageReference"]:
                                                        vmss_vm_os_publisher = vmss_vm["properties"]["storageProfile"]["imageReference"]["publisher"]
                                                    else:
                                                        vmss_vm_os_publisher = None
                                                    if "offer" in vmss_vm["properties"]["storageProfile"]["imageReference"]:
                                                        vmss_vm_os_offer = vmss_vm["properties"]["storageProfile"]["imageReference"]["offer"]
                                                    else:
                                                        vmss_vm_os_offer = None
                                                    if "sku" in vmss_vm["properties"]["storageProfile"]["imageReference"]:
                                                        vmss_vm_os_sku = vmss_vm["properties"]["storageProfile"]["imageReference"]["sku"]
                                                    else:
                                                        vmss_vm_os_sku = None
                                                    if "version" in vmss_vm["properties"]["storageProfile"]["imageReference"]:
                                                        vmss_vm_os_version = vmss_vm["properties"]["storageProfile"]["imageReference"]["version"]
                                                    else:
                                                        vmss_vm_os_version = None
                                                    if "exactVersion" in vmss_vm["properties"]["storageProfile"]["imageReference"]:
                                                        vmss_vm_os_exact_version = vmss_vm["properties"]["storageProfile"]["imageReference"]["exactVersion"]
                                                    else:
                                                        vmss_vm_os_exact_version = None
                                                else:
                                                    vmss_vm_os_publisher = None
                                                    vmss_vm_os_offer = None
                                                    vmss_vm_os_sku = None
                                                    vmss_vm_os_version = None
                                                    vmss_vm_os_exact_version = None
                                            else:
                                                vmss_vm_os_publisher = None
                                                vmss_vm_os_offer = None
                                                vmss_vm_os_sku = None
                                                vmss_vm_os_version = None
                                                vmss_vm_os_exact_version = None
                                        else:
                                            vmss_vm_size = None
                                            vmss_vm_os_publisher = None
                                            vmss_vm_os_offer = None
                                            vmss_vm_os_sku = None
                                            vmss_vm_os_version = None
                                            vmss_vm_os_exact_version = None
                                        # Write Data to CSV
                                        print("Writing Scale Set Virtual Machine Details for ", vmss_name)
                                        vmss_vm_excel_data = [subscription_name, vmss_rg_name, vmss_name, vmss_vm_name, vmss_vm_location, vmss_vm_sku_name, vmss_vm_sku_tier, vmss_vm_size, vmss_vm_os_publisher, vmss_vm_os_offer, vmss_vm_os_sku, vmss_vm_os_version, vmss_vm_os_exact_version, tag_csv_value]
                                        vmss_vm_sql_data = [subscription_name, vmss_rg_name, vmss_name, vmss_vm_name, vmss_vm_location, vmss_vm_sku_name, vmss_vm_sku_tier, vmss_vm_size, vmss_vm_os_publisher, vmss_vm_os_offer, vmss_vm_os_sku, vmss_vm_os_version, vmss_vm_os_exact_version, tag_sql_value]
                                        with open('VMSS Virtual Machines.csv', mode='a', newline='') as vmss_vm_excel_file_data:
                                            csvwriter = csv.writer(vmss_vm_excel_file_data, delimiter=',')
                                            csvwriter.writerow(vmss_vm_excel_data)
                                        with open('sql_vmss_vm.csv', mode='a', newline='') as vmss_vm_sql_file_data:
                                            csvwriter = csv.writer(vmss_vm_sql_file_data, delimiter=',')
                                            csvwriter.writerow(vmss_vm_sql_data)
                                else:
                                    print("No Virtual Machine found for VMMS ", vmss_name)
                                    pass
                            else:
                                print("Error Getting API Response for VMSS VM for ", vmss_name)
                                pass
                    else:
                        print("No Virtual Machine Scale Set found for ", subscription_name)
                        pass
                else:
                    print("Error getting API responses for Virtual Machine Scale Set for ", subscription_name)
                    pass
        else:
            print("No Virtual Machine Scale Set found for ", subscription_name)
            pass
    else:
        print("Error getting API responses for Virtual Machine Scale Set for ", subscription_name)
        pass