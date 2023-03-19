import requests
import json
import sys
import csv
import os

# Get Virtual Network Details
def get_vn(subscription_name, header):
    # Open Saved Resource Group json file
    with open("rg.json") as rg_saved_json:
        rg_json = json.load(rg_saved_json)
    # Write some csv file headers
    vnet_excel_header = ["Subscription", "Resource Group", "Name", "Location", "Provisioning State", "DDOS Protection", "Address Space", "DNS Servers", "Number of Subnets", "Number of Peering", "Tags", "Locks"]
    vnet_sql_header = ["sub", "rg_name", "name", "location", "provisioning_state", "ddos_protection", "address_space", "dns_servers", "total_subnets", "total_peering", "tags", "locks"]
    subnet_excel_header = ["Subscription", "Resource Group", "Virtual Network", "Name", "Provisioning State", "Address Space", "NSG Name", "UDR Name"]
    subnet_sql_header = ["sub", "rg_name", "vnet_name", "name", "provisioning_state", "address_space", "nsg_name", "udr_name"]
    peering_excel_header = ["Subscription","Source VNET RG Name","Source VNET Name", "Peering Name", "Destination VNET Name", "Destination VNET RG Name", "Peering Status", "Forward Traffic", "Gateway Transit", "Network Access"]
    peering_sql_header = ["sub","source_vnet_rg_name","source_vnet_name", "peering_name", "dest_vnet_name", "dest_vnet_rg_name", "peering_status", "forward_traffic", "gateway_transit", "network_access"]
    nsg_excel_header = ["Subscription", "Resource Group", "Name", "Associated Subnet", "Rule Name", "Priority", "Direction", "Access", "Protocol", "Source Port Range", "Destination Port Range", "Source Address Prefix", "Source Port Ranges", "Destination Port Ranges", "Source Address Prefixes", "Destination Address Prefixes", "Provisioning State"]
    nsg_sql_header = ["sub", "rg_name", "name", "associated_subnet", "rule_name", "priority", "direction", "access", "protocol", "source_port_range", "destination_port_range", "source_address_prefix", "source_port_ranges", "destination_port_ranges", "source_address_prefixes", "destination_address_prefixes", "provisioning_state"]
    udr_excel_header = ["Subscription", "Resource Group", "Route Table Name", "Associated Subnet", "Route Name", "Address Prefix", "Next Hop Type", "Next Hop IP Address", "BGP Overrides", "Provisioning State"]
    udr_sql_header = ["sub", "rg_name", "route_table_name", "associated_subnet", "route_name", "address_prefix", "next_hop_type", "next_hop_ip_address", "bgp_overrides", "provisioning_state"]
    with open('Virtual Network.csv', mode = 'w', newline='') as vnet_excel_file_header:
        csvwriter = csv.writer(vnet_excel_file_header, delimiter=',')
        csvwriter.writerow(vnet_excel_header)
    with open('sql_vn.csv', mode = 'w', newline='') as vnet_sql_file_header:
        csvwriter = csv.writer(vnet_sql_file_header, delimiter=',')
        csvwriter.writerow(vnet_sql_header)
    with open('Subnet.csv', mode = 'w', newline='') as subnet_excel_file_header:
        csvwriter = csv.writer(subnet_excel_file_header, delimiter=',')
        csvwriter.writerow(subnet_excel_header)
    with open('sql_subnet.csv', mode = 'w', newline='') as subnet_sql_file_header:
        csvwriter = csv.writer(subnet_sql_file_header, delimiter=',')
        csvwriter.writerow(subnet_sql_header)
    with open('Virtual Network Peering.csv', mode = 'w', newline='') as peering_excel_file_header:
        csvwriter = csv.writer(peering_excel_file_header, delimiter=',')
        csvwriter.writerow(peering_excel_header)
    with open('sql_peering.csv', mode = 'w', newline='') as peering_sql_file_header:
        csvwriter = csv.writer(peering_sql_file_header, delimiter=',')
        csvwriter.writerow(peering_sql_header)
    with open('Network Security Groups.csv', mode = 'w', newline='') as nsg_excel_file_header:
        csvwriter = csv.writer(nsg_excel_file_header, delimiter=',')
        csvwriter.writerow(nsg_excel_header)
    with open('sql_nsg.csv', mode = 'w', newline='') as nsg_sql_file_header:
        csvwriter = csv.writer(nsg_sql_file_header, delimiter=',')
        csvwriter.writerow(nsg_sql_header)
    with open('Route Tables.csv', mode = 'w', newline='') as udr_excel_file_header:
        csvwriter = csv.writer(udr_excel_file_header, delimiter=',')
        csvwriter.writerow(udr_excel_header)
    with open('sql_udr.csv', mode = 'w', newline='') as udr_sql_file_header:
        csvwriter = csv.writer(udr_sql_file_header, delimiter=',')
        csvwriter.writerow(udr_sql_header)
    # Query Virtual Network APIs
    for vnet_rg in rg_json["value"]:
        print("Getting Virtual Network Details for ", vnet_rg["name"])
        rg_id = vnet_rg["id"]
        vnet_list = requests.get(url = "https://management.azure.com"+rg_id+"/providers/Microsoft.Network/virtualNetworks?api-version=2022-07-01", headers = header)
        vnet_list_to_json = vnet_list.json()
        if vnet_list.status_code == 200 or vnet_list.status_code == 204:
            if "value" in vnet_list_to_json:
                for vnet in vnet_list_to_json["value"]:
                    # Get Virtual Network Tags
                    get_vn_tags = requests.get(url = "https://management.azure.com"+vnet["id"]+"/providers/Microsoft.Resources/tags/default?api-version=2021-04-01", headers = header)
                    get_vn_tags_to_json = get_vn_tags.json()
                    if get_vn_tags.status_code == 200 or get_vn_tags.status_code == 204:
                        if "properties" in get_vn_tags_to_json:
                            if "tags" in get_vn_tags_to_json["properties"]:
                                vn_tags = []
                                for key,value in get_vn_tags_to_json["properties"]["tags"].items():
                                    vn_tag_value = ""+key+"="+value+""
                                    vn_tags.append(vn_tag_value)
                                vn_tag_excel_value = '\n'.join(vn_tags)
                                vn_tag_sql_value = ','.join(vn_tags)
                            else:
                                vn_tag_excel_value = None
                                vn_tag_sql_value = "No Tags"
                        else:
                            vn_tag_excel_value = None
                            vn_tag_sql_value = "No Tags"
                    else:
                        vn_tag_excel_value = ""+get_vn_tags_to_json["error"]["code"]+" - "+get_vn_tags_to_json["error"]["message"]+""
                        vn_tag_sql_value = ""+get_vn_tags_to_json["error"]["code"]+" - "+get_vn_tags_to_json["error"]["message"]+""
                    # Get Virtual Network Locks
                    get_vn_lock_details = requests.get(url = "https://management.azure.com"+vnet["id"]+"/providers/Microsoft.Authorization/locks?api-version=2016-09-01", headers = header)
                    get_vn_lock_resonse_to_json = get_vn_lock_details.json()
                    if get_vn_lock_details.status_code == 200 or get_vn_lock_details.status_code == 204:
                        if "value" in get_vn_lock_resonse_to_json:
                            vn_locks = []
                            for lock in get_vn_lock_resonse_to_json["value"]:
                                lock_level = lock["properties"]["level"]
                                lock_name = lock["name"]
                                lock_scope = lock["id"]
                                lock_value = "Level="+lock_level+", Name="+lock_name+", Scope="+lock_scope+""
                                vn_locks.append(lock_value)
                            vn_lock_excel_value = '\n'.join(vn_locks)
                            vn_lock_sql_value = ','.join(vn_locks)
                        else:
                            vn_lock_excel_value = None
                            vn_lock_sql_value = "No Locks"
                    else:
                        vn_lock_excel_value = ""+get_vn_lock_resonse_to_json["error"]["code"]+" - "+get_vn_lock_resonse_to_json["error"]["message"]+""
                        vn_lock_sql_value = ""+get_vn_lock_resonse_to_json["error"]["code"]+" - "+get_vn_lock_resonse_to_json["error"]["message"]+""
                    # Get Virtual Network DNS Servers
                    if "dhcpOptions" in vnet["properties"]:
                        if "dnsServers" in vnet["properties"]["dhcpOptions"]:
                            dns_servers = ','.join(vnet["properties"]["dhcpOptions"]["dnsServers"])
                        else:
                            dns_servers = None
                    else:
                        dns_servers = None
                    # Write Virtual Network Data to Excel and SQL Table
                    print("Writing Virtual Network Details for ", vnet_rg["name"])
                    vnet_excel_data = [subscription_name,vnet_rg["name"],vnet["name"],vnet["location"],vnet["properties"]["provisioningState"],vnet["properties"]["enableDdosProtection"], ','.join(vnet["properties"]["addressSpace"]["addressPrefixes"]), dns_servers, len(vnet["properties"]["subnets"]), len(vnet["properties"]["virtualNetworkPeerings"]), vn_tag_excel_value, vn_lock_excel_value]
                    vnet_sql_data = [subscription_name,vnet_rg["name"],vnet["name"],vnet["location"],vnet["properties"]["provisioningState"],vnet["properties"]["enableDdosProtection"], ','.join(vnet["properties"]["addressSpace"]["addressPrefixes"]), dns_servers, len(vnet["properties"]["subnets"]), len(vnet["properties"]["virtualNetworkPeerings"]), vn_tag_sql_value, vn_lock_sql_value]
                    with open('Virtual Network.csv', mode='a', newline='') as vn_excel_file_data:
                        csvwriter = csv.writer(vn_excel_file_data, delimiter=',')
                        csvwriter.writerow(vnet_excel_data)
                    with open('sql_vn.csv', mode='a', newline='') as vn_sql_file_data:
                        csvwriter = csv.writer(vn_sql_file_data, delimiter=',')
                        csvwriter.writerow(vnet_sql_data)
                    # Write Subnet Data to Excel and SQL Table
                    if "subnets" in vnet["properties"]:
                        for subnet in vnet["properties"]["subnets"]:
                            print("Getting Subnet ", subnet["name"])
                            if "networkSecurityGroup" in subnet["properties"]:
                                subnet_nsg_name = subnet["properties"]["networkSecurityGroup"]["id"].split('/')[-1]
                                print("Getting NSG details for ", subnet["name"])
                                nsg_details = requests.get(url = "https://management.azure.com"+subnet["properties"]["networkSecurityGroup"]["id"]+"?api-version=2022-07-01", headers = header)
                                nsg_details_to_json = nsg_details.json()
                                if nsg_details.status_code == 200 or nsg_details.status_code == 204:
                                    if "securityRules" in nsg_details_to_json["properties"]:
                                        print("Writing NSG Data for ", subnet_nsg_name)
                                        for rules in nsg_details_to_json["properties"]["securityRules"]:
                                            if "sourcePortRange" in rules["properties"]:
                                                nsg_source_port_range = rules["properties"]["sourcePortRange"]
                                            else:
                                                nsg_source_port_range = None
                                            if "destinationPortRange" in rules["properties"]:
                                                nsg_destination_port_range = rules["properties"]["destinationPortRange"]
                                            else:
                                                nsg_destination_port_range = None
                                            if "sourceAddressPrefix" in rules["properties"]:
                                                nsg_source_address_prefix = rules["properties"]["sourceAddressPrefix"]
                                            else:
                                                nsg_source_address_prefix = None
                                            if "sourcePortRanges" in rules["properties"]:
                                                nsg_source_port_ranges = ','.join(rules["properties"]["sourcePortRanges"])
                                            else:
                                                nsg_source_port_ranges = None
                                            if "destinationPortRanges" in rules["properties"]:
                                                nsg_destination_port_ranges = ','.join(rules["properties"]["destinationPortRanges"])
                                            else:
                                                nsg_destination_port_ranges = None
                                            if "sourceAddressPrefixes" in rules["properties"]:
                                                nsg_source_address_prefixes = ','.join(rules["properties"]["sourceAddressPrefixes"])
                                            else:
                                                nsg_source_address_prefixes = None
                                            if "destinationAddressPrefixes" in rules["properties"]:
                                                nsg_destination_address_prefixes = ','.join(rules["properties"]["destinationAddressPrefixes"])
                                            else:
                                                nsg_destination_address_prefixes = None
                                            nsg_excel_data = [subscription_name, rules["id"].split('/')[4], subnet_nsg_name, subnet["name"], rules["name"], rules["properties"]["priority"], rules["properties"]["direction"], rules["properties"]["access"], rules["properties"]["protocol"], nsg_source_port_range, nsg_destination_port_range, nsg_source_address_prefix, nsg_source_port_ranges, nsg_destination_port_ranges, nsg_source_address_prefixes, nsg_destination_address_prefixes, rules["properties"]["provisioningState"]]
                                            nsg_sql_data = [subscription_name, rules["id"].split('/')[4], subnet_nsg_name, subnet["name"], rules["name"], rules["properties"]["priority"], rules["properties"]["direction"], rules["properties"]["access"], rules["properties"]["protocol"], nsg_source_port_range, nsg_destination_port_range, nsg_source_address_prefix, nsg_source_port_ranges, nsg_destination_port_ranges, nsg_source_address_prefixes, nsg_destination_address_prefixes, rules["properties"]["provisioningState"]]
                                            with open('Network Security Groups.csv', mode='a', newline='') as nsg_excel_file_data:
                                                csvwriter = csv.writer(nsg_excel_file_data, delimiter=',')
                                                csvwriter.writerow(nsg_excel_data)
                                            with open('sql_nsg.csv', mode='a', newline='') as nsg_sql_file_data:
                                                csvwriter = csv.writer(nsg_sql_file_data, delimiter=',')
                                                csvwriter.writerow(nsg_sql_data)
                                    else:
                                        print("No NSG Rule Found in ", subnet_nsg_name)
                                        pass
                                else:
                                    print("Error getting NSG details for ", subnet_nsg_name)
                                    pass
                            else:
                                subnet_nsg_name = None
                            if "routeTable" in subnet["properties"]:
                                subnet_udr_name = subnet["properties"]["routeTable"]["id"].split('/')[-1]
                                print("Getting UDR details for ", subnet["name"])
                                udr_details = requests.get(url = "https://management.azure.com"+subnet["properties"]["routeTable"]["id"]+"?api-version=2022-07-01", headers = header)
                                udr_details_to_json = udr_details.json()
                                if udr_details.status_code == 200 or udr_details.status_code == 204:
                                    if "routes" in udr_details_to_json["properties"]:
                                        print("Writing UDR Data for ", subnet_udr_name)
                                        for routes in udr_details_to_json["properties"]["routes"]:
                                            if "nextHopIpAddress" in routes["properties"]:
                                                udr_next_hop_ip_address = routes["properties"]["nextHopIpAddress"]
                                            else:
                                                udr_next_hop_ip_address = None
                                            if "hasBgpOverride" in routes["properties"]:
                                                udr_bgp_overrides = routes["properties"]["hasBgpOverride"]
                                            else:
                                                udr_bgp_overrides = None
                                            udr_excel_data = [subscription_name, routes["id"].split('/')[4],subnet_udr_name, subnet["name"], routes["name"], routes["properties"]["addressPrefix"], routes["properties"]["nextHopType"],udr_next_hop_ip_address, udr_bgp_overrides, routes["properties"]["provisioningState"]]
                                            udr_sql_data = [subscription_name, routes["id"].split('/')[4],subnet_udr_name, subnet["name"], routes["name"], routes["properties"]["addressPrefix"], routes["properties"]["nextHopType"], udr_next_hop_ip_address, udr_bgp_overrides, routes["properties"]["provisioningState"]]
                                            with open('Route Tables.csv', mode='a', newline='') as udr_excel_file_data:
                                                csvwriter = csv.writer(udr_excel_file_data, delimiter=',')
                                                csvwriter.writerow(udr_excel_data)
                                            with open('sql_udr.csv', mode='a', newline='') as udr_sql_file_data:
                                                csvwriter = csv.writer(udr_sql_file_data, delimiter=',')
                                                csvwriter.writerow(udr_sql_data)
                                    else:
                                        print("No UDR Rule Found in ", subnet_udr_name)
                                        pass
                                else:
                                    print("Error getting UDR details for ", subnet_udr_name)
                                    pass
                            else:
                                subnet_udr_name = None
                            subnet_excel_data = [subscription_name,vnet_rg["name"],vnet["name"],subnet["name"], subnet["properties"]["provisioningState"], subnet["properties"]["addressPrefix"], subnet_nsg_name, subnet_udr_name]
                            subnet_sql_data = [subscription_name,vnet_rg["name"],vnet["name"],subnet["name"], subnet["properties"]["provisioningState"], subnet["properties"]["addressPrefix"], subnet_nsg_name, subnet_udr_name]
                            print("Writing Subnet Data for ", vnet["name"])
                            with open('Subnet.csv', mode='a', newline='') as subnet_excel_file_data:
                                csvwriter = csv.writer(subnet_excel_file_data, delimiter=',')
                                csvwriter.writerow(subnet_excel_data)
                            with open('sql_subnet.csv', mode='a', newline='') as subnet_sql_file_data:
                                csvwriter = csv.writer(subnet_sql_file_data, delimiter=',')
                                csvwriter.writerow(subnet_sql_data)
                    else:
                        print("No Subnets Found in ", vnet["name"])
                        pass
                    # Write Virtual Network Peering to Excel and SQL Table
                    if "virtualNetworkPeerings" in vnet["properties"]:
                        for peering in vnet["properties"]["virtualNetworkPeerings"]:
                            print("Getting Virtual Network Peering Details for ", vnet["name"])
                            peering_excel_data = [subscription_name,vnet_rg["name"],vnet["name"], peering["name"], peering["properties"]["remoteVirtualNetwork"]["id"].split('/')[-1], peering["properties"]["remoteVirtualNetwork"]["id"].split('/')[4], peering["properties"]["peeringState"], peering["properties"]["allowForwardedTraffic"], peering["properties"]["allowGatewayTransit"], peering["properties"]["allowVirtualNetworkAccess"]]
                            peering_sql_data = [subscription_name,vnet_rg["name"],vnet["name"], peering["name"], peering["properties"]["remoteVirtualNetwork"]["id"].split('/')[-1], peering["properties"]["remoteVirtualNetwork"]["id"].split('/')[4], peering["properties"]["peeringState"], peering["properties"]["allowForwardedTraffic"], peering["properties"]["allowGatewayTransit"], peering["properties"]["allowVirtualNetworkAccess"]]
                            print("Writing Peering Data for ", peering["name"])
                            with open('Virtual Network Peering.csv', mode='a', newline='') as peering_excel_file_data:
                                csvwriter = csv.writer(peering_excel_file_data, delimiter=',')
                                csvwriter.writerow(peering_excel_data)
                            with open('sql_peering.csv', mode='a', newline='') as peering_sql_file_data:
                                csvwriter = csv.writer(peering_sql_file_data, delimiter=',')
                                csvwriter.writerow(peering_sql_data)
                    else:
                        print("No Virtual Network Peering Found in ", vnet["name"])
                        pass 
            else:
                print("No Virtual Network Found for Resource Group ", vnet_rg["name"])
                pass
        else:
            print("No Virtual Network Found for Resource Group ", vnet_rg["name"])
            pass

def get_pip(subscription_id, subscription_name, header):
    print("Getting Public IP Address for ", subscription_name)
    # Create the headers
    pip_excel_header = ["Subscription", "Resource Group", "Name", "Location", "Used", "Provisioning State", "Version", "Allocation", "SKU Name", "SKU Tier", "Idle Timeout(Minutes)", "DDOS Protection Mode", "FQDN", "Tags"]
    pip_sql_header = ["sub", "rg_name", "pip_name", "pip_location", "pip_used", "pip_provisioning_state", "pip_version", "pip_allocation", "pip_sku_name", "pip_sku_tier", "pip_idle_timeout_min", "pip_ddos_mode", "pip_fqdn", "tags"]
    with open('Public IP Address.csv', mode = 'w', newline='') as pip_excel_file_header:
        csvwriter = csv.writer(pip_excel_file_header, delimiter=',')
        csvwriter.writerow(pip_excel_header)
    with open('sql_pip.csv', mode = 'w', newline='') as pip_sql_file_header:
        csvwriter = csv.writer(pip_sql_file_header, delimiter=',')
        csvwriter.writerow(pip_sql_header)
    get_pip_details = requests.get(url = "https://management.azure.com/subscriptions/"+subscription_id+"/providers/Microsoft.Network/publicIPAddresses?api-version=2022-07-01", headers = header)
    get_pip_details_to_json = get_pip_details.json()
    print(get_pip_details_to_json)
    if get_pip_details.status_code == 200 or get_pip_details.status_code == 204:
        if "value" in get_pip_details_to_json:
            for pip in get_pip_details_to_json["value"]:
                pip_name = pip["name"]
                pip_rg_name_split = pip["id"].split('/')
                pip_rg_name = pip_rg_name_split[4]
                pip_location = pip["location"]
                if "tags" in pip:
                    all_tags = []
                    for key,value in pip["tags"].items():
                        tag_value = ""+key+"="+value+""
                        all_tags.append(tag_value)
                    tag_csv_value = '\n'.join(all_tags)
                    tag_sql_value = ','.join(all_tags)
                else:
                    tag_csv_value = str()
                    tag_sql_value = "No Tags"
                if "sku" in pip:
                    if "name" in pip["sku"]:
                        pip_sku_name = pip["sku"]["name"]
                    else:
                        pip_sku_name = None
                    if "tier" in pip["sku"]:
                        pip_sku_tier = pip["sku"]["tier"]
                    else:
                        pip_sku_tier = None
                else:
                    pip_sku_name = None
                    pip_sku_tier = None
                if "properties" in pip:
                    if "provisioningState" in pip["properties"]:
                        pip_provisioning_state = pip["properties"]["provisioningState"]
                    else:
                        pip_provisioning_state = None
                    if "publicIPAddressVersion" in pip["properties"]:
                        pip_version = pip["properties"]["publicIPAddressVersion"]
                    else:
                        pip_version = None
                    if "publicIPAllocationMethod" in pip["properties"]:
                        pip_allocation = pip["properties"]["publicIPAllocationMethod"]
                    else:
                        pip_allocation = None
                    if "idleTimeoutInMinutes" in pip["properties"]:
                        pip_idle_timeout = pip["properties"]["idleTimeoutInMinutes"]
                    else:
                        pip_idle_timeout = None
                    if "ipConfiguration" in pip["properties"]:
                        pip_attached = "Yes"
                    else:
                        pip_attached = "No"
                    if "ddosSettings" in pip["properties"]:
                        if "protectionMode" in pip["properties"]["ddosSettings"]:
                            pip_ddos = pip["properties"]["ddosSettings"]["protectionMode"]
                        else:
                            pip_ddos = None
                    else:
                        pip_ddos = None
                    if "dnsSettings" in pip["properties"]:
                        if "fqdn" in pip["properties"]["dnsSettings"]:
                            pip_fqdn = pip["properties"]["dnsSettings"]["fqdn"]
                        else:
                            pip_fqdn = None
                    else:
                        pip_fqdn = None
                    
                    # Write Data to CSV
                    print("Writing Public IP Details for ", pip_name)
                    pip_excel_data = [subscription_name, pip_rg_name, pip_name, pip_location, pip_attached, pip_provisioning_state, pip_version, pip_allocation, pip_sku_name, pip_sku_tier, pip_idle_timeout, pip_ddos, pip_fqdn, tag_csv_value]
                    pip_sql_data = [subscription_name, pip_rg_name, pip_name, pip_location, pip_attached, pip_provisioning_state, pip_version, pip_allocation, pip_sku_name, pip_sku_tier, pip_idle_timeout, pip_ddos, pip_fqdn, tag_sql_value]
                    with open('Public IP Address.csv', mode = 'a', newline='') as pip_excel_file_data:
                        csvwriter = csv.writer(pip_excel_file_data, delimiter=',')
                        csvwriter.writerow(pip_excel_data)
                    with open('sql_pip.csv', mode = 'a', newline='') as pip_sql_file_data:
                        csvwriter = csv.writer(pip_sql_file_data, delimiter=',')
                        csvwriter.writerow(pip_sql_data)
        else:
            print("No Public Ip Address Found for ", subscription_name)
            pass
    else:
        print("Error Getting Public IP Details for ", subscription_name)
        pass