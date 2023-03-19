import requests
import json
import sys
import csv
import os

def get_lb(subscription_id,subscription_name,header):
    print("Getting Load Balancer Details for ", subscription_name)
    # Create CSV headers
    lb_excel_header = ["Subscription", "Resource Group", "Name", "Location", "Provisioning State", "SKU Name", "SKU Tier", "Frontend IP Config", "Backend Address Pool", "Load Balancing Rules", "Health Probes", "Inbound NAT Rules", "Outbound Rules", "Inbound NAT Pools", "Tags"]
    lb_sql_header = ["sub", "rg_name", "lb_name", "lb_location", "lb_provisioning_state", "lb_sku_name", "lb_sku_tier", "lb_frontend_ip_config", "lb_backend_address_pool", "lb_rules", "lb_health_probes", "lb_inbound_nat_rules", "lb_outbound_rules", "lb_inbound_nat_pools", "tags"]
    lb_fip_excel_header = ["Subscription", "Resource Group", "Load balancer", "Name", "Type", "Provisioning State", "Private IP Address", "Virtual Network", "Subnet", "Public IP Address", "No of Outbound Rules", "No of LB Rules", "No of Inbound NAT Rules"]
    lb_fip_sql_header = ["sub", "rg_name", "lb_name", "fip_name", "fip_type", "fip_provisioning_state", "fip_private_ip", "fip_vn", "fip_subnet", "fip_pip", "fip_outbound_rules_no", "fip_lb_rules_no", "fip_inbound_nat_rules_no"]
    with open('Load Balancer.csv', mode='w', newline='') as lb_excel_file_header:
        csvwriter = csv.writer(lb_excel_file_header, delimiter=',')
        csvwriter.writerow(lb_excel_header)
    with open('sql_lb.csv', mode='w', newline='') as lb_sql_file_header:
        csvwriter = csv.writer(lb_sql_file_header, delimiter=',')
        csvwriter.writerow(lb_sql_header)
    with open('LB Frontend Config.csv', mode='w', newline='') as lb_fip_excel_file_header:
        csvwriter = csv.writer(lb_fip_excel_file_header, delimiter=',')
        csvwriter.writerow(lb_fip_excel_header)
    with open('sql_lb_fip.csv', mode='w', newline='') as lb_fip_sql_file_header:
        csvwriter = csv.writer(lb_fip_sql_file_header, delimiter=',')
        csvwriter.writerow(lb_fip_sql_header)
    # Get Started
    get_lb_details = requests.get(url = "https://management.azure.com/subscriptions/"+subscription_id+"/providers/Microsoft.Network/loadBalancers?api-version=2022-07-01", headers = header)
    get_lb_details_to_json = get_lb_details.json()
    if get_lb_details.status_code == 200 or get_lb_details.status_code == 204:
        if "value" in get_lb_details_to_json:
            for lb in get_lb_details_to_json["value"]:
                lb_name = lb["name"]
                lb_location = lb["location"]
                lb_rg_name_split = lb["id"].split('/')
                lb_rg_name = lb_rg_name_split[4]
                if "tags" in lb:
                    all_tags = []
                    for key,value in lb["tags"].items():
                        tag_value = ""+key+"="+value+""
                        all_tags.append(tag_value)
                    tag_csv_value = '\n'.join(all_tags)
                    tag_sql_value = ','.join(all_tags)
                else:
                    tag_csv_value = str()
                    tag_sql_value = "No Tags"
                if "sku" in lb:
                    if "name" in lb["sku"]:
                        lb_sku_name = lb["sku"]["name"]
                    else:
                        lb_sku_name = None
                    if "tier" in lb["sku"]:
                        lb_sku_tier = lb["sku"]["tier"]
                    else:
                        lb_sku_tier = None
                else:
                    lb_sku_name = None
                    lb_sku_tier = None
                if "properties" in lb:
                    if "provisioningState" in lb["properties"]:
                        lb_provisioning_state = lb["properties"]["provisioningState"]
                    else:
                        lb_provisioning_state = None
                    if "frontendIPConfigurations" in lb["properties"]:
                        lb_fip = len(lb["properties"]["frontendIPConfigurations"])
                    else:
                        lb_fip = 0
                    if "backendAddressPools" in lb["properties"]:
                        lb_bap = len(lb["properties"]["backendAddressPools"])
                    else:
                        lb_bap = 0
                    if "loadBalancingRules" in lb["properties"]:
                        lb_rules = len(lb["properties"]["loadBalancingRules"])
                    else:
                        lb_rules = 0
                    if "probes" in lb["properties"]:
                        lb_probes = len(lb["properties"]["probes"])
                    else:
                        lb_probes = 0
                    if "inboundNatRules" in lb["properties"]:
                        lb_inr = len(lb["properties"]["inboundNatRules"])
                    else:
                        lb_inr = 0
                    if "outboundRules" in lb["properties"]:
                        lb_or = len(lb["properties"]["outboundRules"])
                    else:
                        lb_or = 0
                    if "inboundNatPools" in lb["properties"]:
                        lb_inp = len(lb["properties"]["inboundNatPools"])
                    else:
                        lb_inp = 0
                else:
                    lb_provisioning_state = None
                    lb_fip = 0
                    lb_bap = 0
                    lb_rules = 0
                    lb_inr = 0
                    lb_or = 0
                    lb_inp = 0
                # Write Data to CSV
                print("Writing Load Balancer Details for ", lb_name)
                lb_excel_data = [subscription_name, lb_rg_name, lb_name, lb_location, lb_provisioning_state, lb_sku_name, lb_sku_tier, lb_fip, lb_bap, lb_rules, lb_probes, lb_inr, lb_or, lb_inp, tag_csv_value]
                lb_sql_data = [subscription_name, lb_rg_name, lb_name, lb_location, lb_provisioning_state, lb_sku_name, lb_sku_tier, lb_fip, lb_bap, lb_rules, lb_probes, lb_inr, lb_or, lb_inp, tag_sql_value]
                with open('Load Balancer.csv', mode='a', newline='') as lb_excel_file_data:
                    csvwriter = csv.writer(lb_excel_file_data, delimiter=',')
                    csvwriter.writerow(lb_excel_data)
                with open('sql_lb.csv', mode='a', newline='') as lb_sql_file_data:
                    csvwriter = csv.writer(lb_sql_file_data, delimiter=',')
                    csvwriter.writerow(lb_sql_data)

                # Get Load Balancer Properties
                print("Getting Load Balancer Frontend Config for ", lb_name)
                if "properties" in lb:
                    if "frontendIPConfigurations" in lb["properties"]:
                        for lb_fip in lb["properties"]["frontendIPConfigurations"]:
                            lb_fip_name = lb_fip["name"]
                            if "properties" in lb_fip:
                                if "provisioningState" in lb_fip["properties"]:
                                    lb_fip_provisioning_state = lb_fip["properties"]["provisioningState"]
                                else:
                                    lb_fip_provisioning_state = None
                                if "privateIPAddress" in lb_fip["properties"]:
                                    lb_fip_private_ip_address = lb_fip["properties"]["privateIPAddress"]
                                    lb_fip_type = "Internal"
                                else:
                                    lb_fip_private_ip_address = None
                                    lb_fip_type = "External"
                                if "subnet" in lb_fip["properties"]:
                                    lb_fip_vn_split = lb_fip["properties"]["subnet"]["id"].split('/')
                                    lb_fip_vn = lb_fip_vn_split[-3]
                                    lb_fip_subnet = lb_fip_vn_split[-1]
                                else:
                                    lb_fip_vn = None
                                    lb_fip_subnet = None
                                if "loadBalancingRules" in lb_fip["properties"]:
                                    lb_fip_lb_rules = len(lb_fip["properties"]["loadBalancingRules"])
                                else:
                                    lb_fip_lb_rules = 0
                                if "publicIPAddress" in lb_fip["properties"]:
                                    lb_pip_split = lb_fip["properties"]["publicIPAddress"]["id"].split('/')
                                    lb_pip_name = lb_pip_split[-1]
                                else:
                                    lb_pip_name = None
                                if "outboundRules" in lb_fip["properties"]:
                                    lb_fip_outbound_rules = len(lb_fip["properties"]["outboundRules"])
                                else:
                                    lb_fip_outbound_rules = 0
                                if "inboundNatRules" in lb_fip["properties"]:
                                    lb_fip_inbound_nat_rules = len(lb_fip["properties"]["inboundNatRules"])
                                else:
                                    lb_fip_inbound_nat_rules = 0
                            else:
                                lb_fip_provisioning_state = None
                                lb_fip_private_ip_address = None
                                lb_fip_type = None
                                lb_fip_vn = None
                                lb_fip_subnet = None
                                lb_fip_lb_rules = 0
                                lb_pip_name = None
                                lb_fip_outbound_rules = 0
                                lb_fip_inbound_nat_rules = 0
                            # Write Data to CSV
                            print("Writing Frontend Config Details for ", lb_name)
                            lb_fip_excel_data = [subscription_name, lb_rg_name, lb_name, lb_fip_name, lb_fip_type, lb_fip_provisioning_state, lb_fip_private_ip_address, lb_fip_vn, lb_fip_subnet, lb_pip_name, lb_fip_outbound_rules, lb_fip_lb_rules, lb_fip_inbound_nat_rules]
                            lb_fip_sql_data = [subscription_name, lb_rg_name, lb_name, lb_fip_name, lb_fip_type, lb_fip_provisioning_state, lb_fip_private_ip_address, lb_fip_vn, lb_fip_subnet, lb_pip_name, lb_fip_outbound_rules, lb_fip_lb_rules, lb_fip_inbound_nat_rules]
                            with open('LB Frontend Config.csv', mode='a', newline='') as lb_fip_excel_file_data:
                                csvwriter = csv.writer(lb_fip_excel_file_data, delimiter=',')
                                csvwriter.writerow(lb_fip_excel_data)
                            with open('sql_lb_fip.csv', mode='a', newline='') as lb_fip_sql_file_data:
                                csvwriter = csv.writer(lb_fip_sql_file_data, delimiter=',')
                                csvwriter.writerow(lb_fip_sql_data)
                    else:
                        print("No Frontend IP Config found for ", lb_name)
                        pass
                else:
                    print("No Properties Found in Load Balancer APi Response for ", lb_name)
                    pass

            while "nextLink" in get_lb_details_to_json:
                print("Next Link Found. Querying API for more data")
                get_lb_details = requests.get(url = get_lb_details_to_json["nextLink"], headers = header)
                get_lb_details_to_json = get_lb_details.json()
                if get_lb_details.status_code == 200 or get_lb_details.status_code == 204:
                    if "value" in get_lb_details_to_json:
                        for lb in get_lb_details_to_json["value"]:
                            lb_name = lb["name"]
                            lb_location = lb["location"]
                            lb_rg_name_split = lb["id"].split('/')
                            lb_rg_name = lb_rg_name_split[4]
                            if "tags" in lb:
                                all_tags = []
                                for key,value in lb["tags"].items():
                                    tag_value = ""+key+"="+value+""
                                    all_tags.append(tag_value)
                                tag_csv_value = '\n'.join(all_tags)
                                tag_sql_value = ','.join(all_tags)
                            else:
                                tag_csv_value = str()
                                tag_sql_value = "No Tags"
                            if "sku" in lb:
                                if "name" in lb["sku"]:
                                    lb_sku_name = lb["sku"]["name"]
                                else:
                                    lb_sku_name = None
                                if "tier" in lb["sku"]:
                                    lb_sku_tier = lb["sku"]["tier"]
                                else:
                                    lb_sku_tier = None
                            else:
                                lb_sku_name = None
                                lb_sku_tier = None
                            if "properties" in lb:
                                if "provisioningState" in lb["properties"]:
                                    lb_provisioning_state = lb["properties"]["provisioningState"]
                                else:
                                    lb_provisioning_state = None
                                if "frontendIPConfigurations" in lb["properties"]:
                                    lb_fip = len(lb["properties"]["frontendIPConfigurations"])
                                else:
                                    lb_fip = 0
                                if "backendAddressPools" in lb["properties"]:
                                    lb_bap = len(lb["properties"]["backendAddressPools"])
                                else:
                                    lb_bap = 0
                                if "loadBalancingRules" in lb["properties"]:
                                    lb_rules = len(lb["properties"]["loadBalancingRules"])
                                else:
                                    lb_rules = 0
                                if "probes" in lb["properties"]:
                                    lb_probes = len(lb["properties"]["probes"])
                                else:
                                    lb_probes = 0
                                if "inboundNatRules" in lb["properties"]:
                                    lb_inr = len(lb["properties"]["inboundNatRules"])
                                else:
                                    lb_inr = 0
                                if "outboundRules" in lb["properties"]:
                                    lb_or = len(lb["properties"]["outboundRules"])
                                else:
                                    lb_or = 0
                                if "inboundNatPools" in lb["properties"]:
                                    lb_inp = len(lb["properties"]["inboundNatPools"])
                                else:
                                    lb_inp = 0
                            else:
                                lb_provisioning_state = None
                                lb_fip = 0
                                lb_bap = 0
                                lb_rules = 0
                                lb_inr = 0
                                lb_or = 0
                                lb_inp = 0
                            # Write Data to CSV
                            print("Writing Load Balancer Details for ", lb_name)
                            lb_excel_data = [subscription_name, lb_rg_name, lb_name, lb_location, lb_provisioning_state, lb_sku_name, lb_sku_tier, lb_fip, lb_bap, lb_rules, lb_probes, lb_inr, lb_or, lb_inp, tag_csv_value]
                            lb_sql_data = [subscription_name, lb_rg_name, lb_name, lb_location, lb_provisioning_state, lb_sku_name, lb_sku_tier, lb_fip, lb_bap, lb_rules, lb_probes, lb_inr, lb_or, lb_inp, tag_sql_value]
                            with open('Load Balancer.csv', mode='a', newline='') as lb_excel_file_data:
                                csvwriter = csv.writer(lb_excel_file_data, delimiter=',')
                                csvwriter.writerow(lb_excel_data)
                            with open('sql_lb.csv', mode='a', newline='') as lb_sql_file_data:
                                csvwriter = csv.writer(lb_sql_file_data, delimiter=',')
                                csvwriter.writerow(lb_sql_data)
                            
                            # Get Load Balancer Properties
                            print("Getting Load Balancer Frontend Config for ", lb_name)
                            if "properties" in lb:
                                # Get Frontend Config
                                if "frontendIPConfigurations" in lb["properties"]:
                                    for lb_fip in lb["properties"]["frontendIPConfigurations"]:
                                        lb_fip_name = lb_fip["name"]
                                        if "properties" in lb_fip:
                                            if "provisioningState" in lb_fip["properties"]:
                                                lb_fip_provisioning_state = lb_fip["properties"]["provisioningState"]
                                            else:
                                                lb_fip_provisioning_state = None
                                            if "privateIPAddress" in lb_fip["properties"]:
                                                lb_fip_private_ip_address = lb_fip["properties"]["privateIPAddress"]
                                                lb_fip_type = "Internal"
                                            else:
                                                lb_fip_private_ip_address = None
                                                lb_fip_type = "External"
                                            if "subnet" in lb_fip["properties"]:
                                                lb_fip_vn_split = lb_fip["properties"]["subnet"]["id"].split('/')
                                                lb_fip_vn = lb_fip_vn_split[-3]
                                                lb_fip_subnet = lb_fip_vn_split[-1]
                                            else:
                                                lb_fip_vn = None
                                                lb_fip_subnet = None
                                            if "loadBalancingRules" in lb_fip["properties"]:
                                                lb_fip_lb_rules = len(lb_fip["properties"]["loadBalancingRules"])
                                            else:
                                                lb_fip_lb_rules = 0
                                            if "publicIPAddress" in lb_fip["properties"]:
                                                lb_pip_split = lb_fip["properties"]["publicIPAddress"]["id"].split('/')
                                                lb_pip_name = lb_pip_split[-1]
                                            else:
                                                lb_pip_name = None
                                            if "outboundRules" in lb_fip["properties"]:
                                                lb_fip_outbound_rules = len(lb_fip["properties"]["outboundRules"])
                                            else:
                                                lb_fip_outbound_rules = 0
                                            if "inboundNatRules" in lb_fip["properties"]:
                                                lb_fip_inbound_nat_rules = len(lb_fip["properties"]["inboundNatRules"])
                                            else:
                                                lb_fip_inbound_nat_rules = 0
                                        else:
                                            lb_fip_provisioning_state = None
                                            lb_fip_private_ip_address = None
                                            lb_fip_type = None
                                            lb_fip_vn = None
                                            lb_fip_subnet = None
                                            lb_fip_lb_rules = 0
                                            lb_pip_name = None
                                            lb_fip_outbound_rules = 0
                                            lb_fip_inbound_nat_rules = 0
                                        # Write Data to CSV
                                        print("Writing Frontend Config Details for ", lb_name)
                                        lb_fip_excel_data = [subscription_name, lb_rg_name, lb_name, lb_fip_name, lb_fip_type, lb_fip_provisioning_state, lb_fip_private_ip_address, lb_fip_vn, lb_fip_subnet, lb_pip_name, lb_fip_outbound_rules, lb_fip_lb_rules, lb_fip_inbound_nat_rules]
                                        lb_fip_sql_data = [subscription_name, lb_rg_name, lb_name, lb_fip_name, lb_fip_type, lb_fip_provisioning_state, lb_fip_private_ip_address, lb_fip_vn, lb_fip_subnet, lb_pip_name, lb_fip_outbound_rules, lb_fip_lb_rules, lb_fip_inbound_nat_rules]
                                        with open('LB Frontend Config.csv', mode='a', newline='') as lb_fip_excel_file_data:
                                            csvwriter = csv.writer(lb_fip_excel_file_data, delimiter=',')
                                            csvwriter.writerow(lb_fip_excel_data)
                                        with open('sql_lb_fip.csv', mode='a', newline='') as lb_fip_sql_file_data:
                                            csvwriter = csv.writer(lb_fip_sql_file_data, delimiter=',')
                                            csvwriter.writerow(lb_fip_sql_data)
                                else:
                                    print("No Frontend IP Config found for ", lb_name)
                                    pass
                            else:
                                print("No Properties Found in Load Balancer APi Response for ", lb_name)
                                pass
                    else:
                        print("No Load Balancer Found for ", subscription_name)
                        pass
                else:
                    print("Error Getting Load Balancer Details for ", subscription_name)
                    pass    
        else:
            print("No Load Balancer Found for ", subscription_name)
            pass
    else:
        print("Error Getting Load Balancer Details for ", subscription_name)
        pass