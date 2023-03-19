import requests
import json
import sys
import csv
import os

def get_ag(subscription_id,subscription_name,header):
    print("Getting Applicaton Gateway Details for ", subscription_name)
    # Write the Headers
    ag_excel_header = ["Subscription", "Resource Group", "Name", "Location", "Provisioning State", "Operational State", "Http2 Status", "SKU Name", "SKU Tier", "SKU Capacity", "Firewall Status", "Firewall Mode", "Firewall Rule Set", "Firewall Rule Version", "SSL Certificate", "Tags"]
    ag_sql_header = ["sub", "rg_name", "ag_name", "ag_location", "ag_provisioning_state", "ag_operational_state", "ag_http2_status", "ag_sku_name", "ag_sku_tier", "ag_sku_capacity", "ag_firewall_status", "ag_firewall_mode", "ag_firewall_rule_set", "ag_firewall_rule_version", "ag_ssl_certificate", "tags"]
    with open('Application Gateway.csv', mode='w', newline='') as ag_excel_file_header:
        csvwriter = csv.writer(ag_excel_file_header, delimiter=',')
        csvwriter.writerow(ag_excel_header)
    with open('sql_ag.csv', mode='w', newline='') as ag_sql_file_header:
        csvwriter = csv.writer(ag_sql_file_header, delimiter=',')
        csvwriter.writerow(ag_sql_header)
    # Get Started
    get_ag_details = requests.get(url = "https://management.azure.com/subscriptions/"+subscription_id+"/providers/Microsoft.Network/applicationGateways?api-version=2022-07-01", headers = header)
    get_ag_details_to_json = get_ag_details.json()
    if get_ag_details.status_code == 200 or get_ag_details.status_code == 204:
        if "value" in get_ag_details_to_json:
            for ag in get_ag_details_to_json["value"]:
                ag_name = ag["name"]
                ag_rg_name_split = ag["id"].split('/')
                ag_rg_name = ag_rg_name_split[4]
                ag_location = ag["location"]
                if "tags" in ag:
                    all_tags = []
                    for key,value in ag["tags"].items():
                        tag_value = ""+key+"="+value+""
                        all_tags.append(tag_value)
                    tag_csv_value = '\n'.join(all_tags)
                    tag_sql_value = ','.join(all_tags)
                else:
                    tag_csv_value = str()
                    tag_sql_value = "No Tags"
                if "properties" in ag:
                    if "provisioningState" in ag["properties"]:
                        ag_provisioning_state = ag["properties"]["provisioningState"]
                    else:
                        ag_provisioning_state = None
                    if "operationalState" in ag["properties"]:
                        ag_operational_state = ag["properties"]["operationalState"]
                    else:
                        ag_operational_state = None
                    if "enableHttp2" in ag["properties"]:
                        ag_http2 = ag["properties"]["enableHttp2"]
                    else:
                        ag_http2 = None
                    if "sku" in ag["properties"]:
                        if "name" in ag["properties"]["sku"]:
                            ag_sku_name = ag["properties"]["sku"]["name"]
                        else:
                            ag_sku_name = None
                        if "tier" in ag["properties"]["sku"]:
                            ag_sku_tier = ag["properties"]["sku"]["tier"]
                        else:
                            ag_sku_tier = None
                        if "capacity" in ag["properties"]["sku"]:
                            ag_sku_capacity = ag["properties"]["sku"]["capacity"]
                        else:
                            ag_sku_capacity = None
                    else:
                        ag_sku_name = None
                        ag_sku_tier = None
                        ag_sku_capacity = None
                    if "webApplicationFirewallConfiguration" in ag["properties"]:
                        if "enabled" in ag["properties"]["webApplicationFirewallConfiguration"]:
                            ag_fw_status = ag["properties"]["webApplicationFirewallConfiguration"]["enabled"]
                        else:
                            ag_fw_status = None
                        if "firewallMode" in ag["properties"]["webApplicationFirewallConfiguration"]:
                            ag_fw_mode = ag["properties"]["webApplicationFirewallConfiguration"]["firewallMode"]
                        else:
                            ag_fw_mode = None
                        if "ruleSetType" in ag["properties"]["webApplicationFirewallConfiguration"]:
                            ag_fw_rule_type = ag["properties"]["webApplicationFirewallConfiguration"]["ruleSetType"]
                        else:
                            ag_fw_rule_type = None
                        if "ruleSetVersion" in ag["properties"]["webApplicationFirewallConfiguration"]:
                            ag_fw_rule_version = ag["properties"]["webApplicationFirewallConfiguration"]["ruleSetVersion"]
                        else:
                            ag_fw_rule_version = None
                    else:
                        ag_fw_status = None
                        ag_fw_mode = None
                        ag_fw_rule_type = None
                        ag_fw_rule_version = None
                    if "sslCertificates" in ag["properties"]:
                        ag_ssl_cert = "Yes"
                    else:
                        ag_ssl_cert = "No"
                else:
                    ag_provisioning_state = None
                    ag_operational_state = None
                    ag_http2 = None
                    ag_sku_name = None
                    ag_sku_tier = None
                    ag_sku_capacity = None
                    ag_fw_status = None
                    ag_fw_mode = None
                    ag_fw_rule_type = None
                    ag_fw_rule_version = None
                    ag_ssl_cert = None
                # Write Data to CSV
                print("Writing Applciation Gateway Details for ", subscription_name)
                ag_excel_data = [subscription_name, ag_rg_name, ag_name,ag_location, ag_provisioning_state, ag_operational_state, ag_http2, ag_sku_name, ag_sku_tier, ag_sku_capacity, ag_fw_status, ag_fw_mode, ag_fw_rule_type, ag_fw_rule_version, ag_ssl_cert, tag_csv_value]
                ag_sql_data = [subscription_name, ag_rg_name, ag_name,ag_location, ag_provisioning_state, ag_operational_state, ag_http2, ag_sku_name, ag_sku_tier, ag_sku_capacity, ag_fw_status, ag_fw_mode, ag_fw_rule_type, ag_fw_rule_version, ag_ssl_cert, tag_sql_value]
                with open('Application Gateway.csv', mode='a', newline='') as ag_excel_file_data:
                    csvwriter = csv.writer(ag_excel_file_data, delimiter=',')
                    csvwriter.writerow(ag_excel_data)
                with open('sql_ag.csv', mode='a', newline='') as ag_sql_file_data:
                    csvwriter = csv.writer(ag_sql_file_data, delimiter=',')
                    csvwriter.writerow(ag_sql_data)
                
            while "nextLink" in get_ag_details_to_json:
                print("Next Link Found. Querying API for more data")
                get_ag_details = requests.get(url = get_ag_details_to_json["nextLink"], headers = header)
                get_ag_details_to_json = get_ag_details.json()
                if get_ag_details.status_code == 200 or get_ag_details.status_code == 204:
                    if "value" in get_ag_details_to_json:
                        for ag in get_ag_details_to_json["value"]:
                            ag_name = ag["name"]
                            ag_rg_name_split = ag["id"].split('/')
                            ag_rg_name = ag_rg_name_split[4]
                            ag_location = ag["location"]
                            if "tags" in ag:
                                all_tags = []
                                for key,value in ag["tags"].items():
                                    tag_value = ""+key+"="+value+""
                                    all_tags.append(tag_value)
                                tag_csv_value = '\n'.join(all_tags)
                                tag_sql_value = ','.join(all_tags)
                            else:
                                tag_csv_value = str()
                                tag_sql_value = "No Tags"
                            if "properties" in ag:
                                if "provisioningState" in ag["properties"]:
                                    ag_provisioning_state = ag["properties"]["provisioningState"]
                                else:
                                    ag_provisioning_state = None
                                if "operationalState" in ag["properties"]:
                                    ag_operational_state = ag["properties"]["operationalState"]
                                else:
                                    ag_operational_state = None
                                if "enableHttp2" in ag["properties"]:
                                    ag_http2 = ag["properties"]["enableHttp2"]
                                else:
                                    ag_http2 = None
                                if "sku" in ag["properties"]:
                                    if "name" in ag["properties"]["sku"]:
                                        ag_sku_name = ag["properties"]["sku"]
                                    else:
                                        ag_sku_name = None
                                    if "tier" in ag["properties"]["sku"]:
                                        ag_sku_tier = ag["properties"]["tier"]
                                    else:
                                        ag_sku_tier = None
                                    if "capacity" in ag["properties"]["sku"]:
                                        ag_sku_capacity = ag["properties"]["capacity"]
                                    else:
                                        ag_sku_capacity = None
                                else:
                                    ag_sku_name = None
                                    ag_sku_tier = None
                                    ag_sku_capacity = None
                                if "webApplicationFirewallConfiguration" in ag["properties"]:
                                    if "enabled" in ag["properties"]["webApplicationFirewallConfiguration"]:
                                        ag_fw_status = ag["properties"]["webApplicationFirewallConfiguration"]["enabled"]
                                    else:
                                        ag_fw_status = None
                                    if "firewallMode" in ag["properties"]["webApplicationFirewallConfiguration"]:
                                        ag_fw_mode = ag["properties"]["webApplicationFirewallConfiguration"]["firewallMode"]
                                    else:
                                        ag_fw_mode = None
                                    if "ruleSetType" in ag["properties"]["webApplicationFirewallConfiguration"]:
                                        ag_fw_rule_type = ag["properties"]["webApplicationFirewallConfiguration"]["ruleSetType"]
                                    else:
                                        ag_fw_rule_type = None
                                    if "ruleSetVersion" in ag["properties"]["webApplicationFirewallConfiguration"]:
                                        ag_fw_rule_version = ag["properties"]["webApplicationFirewallConfiguration"]["ruleSetVersion"]
                                    else:
                                        ag_fw_rule_version = None
                                else:
                                    ag_fw_status = None
                                    ag_fw_mode = None
                                    ag_fw_rule_type = None
                                    ag_fw_rule_version = None
                                if "sslCertificates" in ag["properties"]:
                                    ag_ssl_cert = "Yes"
                                else:
                                    ag_ssl_cert = "No"
                            else:
                                ag_provisioning_state = None
                                ag_operational_state = None
                                ag_http2 = None
                                ag_sku_name = None
                                ag_sku_tier = None
                                ag_sku_capacity = None
                                ag_fw_status = None
                                ag_fw_mode = None
                                ag_fw_rule_type = None
                                ag_fw_rule_version = None
                                ag_ssl_cert = None
                            # Write Data to CSV
                            print("Writing Applciation Gateway Details for ", subscription_name)
                            ag_excel_data = [subscription_name, ag_rg_name, ag_name,ag_location, ag_provisioning_state, ag_operational_state, ag_http2, ag_sku_name, ag_sku_tier, ag_sku_capacity, ag_fw_status, ag_fw_mode, ag_fw_rule_type, ag_fw_rule_version, ag_ssl_cert, tag_csv_value]
                            ag_sql_data = [subscription_name, ag_rg_name, ag_name,ag_location, ag_provisioning_state, ag_operational_state, ag_http2, ag_sku_name, ag_sku_tier, ag_sku_capacity, ag_fw_status, ag_fw_mode, ag_fw_rule_type, ag_fw_rule_version, ag_ssl_cert, tag_sql_value]
                            with open('Application Gateway.csv', mode='a', newline='') as ag_excel_file_data:
                                csvwriter = csv.writer(ag_excel_file_data, delimiter=',')
                                csvwriter.writerow(ag_excel_data)
                            with open('sql_ag.csv', mode='a', newline='') as ag_sql_file_data:
                                csvwriter = csv.writer(ag_sql_file_data, delimiter=',')
                                csvwriter.writerow(ag_sql_data)
                    else:
                        print("No Application Gateway found for ", subscription_name)
                        pass
                else:
                    print("Error Getting Application Gateway for ", subscription_name)
                    pass
        else:
            print("No Application Gateway found for ", subscription_name)
            pass
    else:
        print("Error Getting Application Gateway for ", subscription_name)
        pass