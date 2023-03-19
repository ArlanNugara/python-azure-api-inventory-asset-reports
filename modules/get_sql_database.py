import requests
import json
import sys
import csv
import os

def get_sql_server(subscription_id, subscription_name, header):
    print("Getting SQL Server Details for ", subscription_name)
    # Write CSV Headers
    sql_server_excel_header = ["Subscription", "Resource Group", "Name", "Location", "Kind", "Version", "Status", "FQDN", "Public Network Access"]
    sql_server_sql_header = ["sub", "rg_name", "name", "location", "kind", "version", "status", "fqdn", "public_network_access"]
    sql_database_excel_header = ["Subscription", "Resource Group", "SQL Server", "Name", "Location", "Status", "Max Size(GB)", "Collation", "Zone Redundancy", "Creation Date", "SKU Name", "SKU Tier", "SKU Capacity", "Read Scale", "Backup Storage Redundancy"]
    sql_database_sql_header = ["sub", "rg_name", "srv_name", "name", "location", "status", "max_size_gb", "collation", "zone_redundancy", "creation_date", "sku_name", "sku_tier", "sku_capacity", "read_scale", "backup_storage_redundancy"]
    sql_server_firewall_rules_excel_header = ["Subscription", "Resource Group", "SQL Server", "Name", "Start IP Address", "End IP Address"]
    sql_server_firewall_rules_sql_header = ["sub", "rg_name", "srv_name", "name", "start_ip_address", "end_ip_address"]
    sql_db_va_excel_header = ["Subscription", "Resource group", "SQL Server", "Database Name", "Assessment Name", "Assessment Status"]
    sql_db_va_sql_header = ["sub", "rg_name", "srv_name", "db_name", "assessment_name", "assessment_status"]
    sql_db_va_scan_excel_header = ["Subscription", "Resource group", "SQL Server", "Database Name", "Assessment Name", "Assessment Status", "Scan Name", "Scan ID", "Status", "Trigger Type", "High Severity Failed Rules", "Medium Severity Failed Rules", "Low Severity Failed Rules", "Passed Rules", "Failed Rules", "Total Rules", "Baseline Applied"]
    sql_db_va_scan_sql_header = ["sub", "rg_name", "srv_name", "db_name", "assessment_name", "assessment_status", "scan_name", "scan_id", "status", "trigger_type", "hs_failed_rules", "ms_failed_rules", "ls_failed_rules", "passed_rules", "failed_rules", "total_rules", "baseline_applied"]
    sql_db_vasr_excel_header = ["Subscription", "Resource group", "SQL Server", "Database Name", "Assessment Name", "Assessment Status", "Scan Name", "Scan ID", "Rule Name", "Rule ID", "Rule Status", "Rule Severity", "Rule Category", "Rule Type", "Rule Title", "Rule Description", "Rule Remediation", "Rule Error Message"]
    sql_db_vasr_sql_header = ["sub", "rg_name", "srv_name", "db_name", "assessment_name", "assessment_status", "scan_name", "scan_id", "rule_name", "rule_id", "rule_status", "rule_severity", "rule_category", "rule_type", "rule_title", "rule_description", "rule_remediation", "rule_error_message"]
    with open('SQL Servers.csv', mode='w', newline='') as sql_srv_excel_file_header:
        csvwriter = csv.writer(sql_srv_excel_file_header, delimiter=',')
        csvwriter.writerow(sql_server_excel_header)
    with open('sql_sql_srv.csv', mode='w', newline='') as sql_srv_sql_file_header:
        csvwriter = csv.writer(sql_srv_sql_file_header, delimiter=',')
        csvwriter.writerow(sql_server_sql_header)
    with open('SQL Databases.csv', mode='w', newline='') as sql_dbs_excel_file_header:
        csvwriter = csv.writer(sql_dbs_excel_file_header, delimiter=',')
        csvwriter.writerow(sql_database_excel_header)
    with open('sql_sql_dbs.csv', mode='w', newline='') as sql_dbs_sql_file_header:
        csvwriter = csv.writer(sql_dbs_sql_file_header, delimiter=',')
        csvwriter.writerow(sql_database_sql_header)
    with open('SQL Firewall Rules.csv', mode='w', newline='') as sql_fwr_excel_file_header:
        csvwriter = csv.writer(sql_fwr_excel_file_header, delimiter=',')
        csvwriter.writerow(sql_server_firewall_rules_excel_header)
    with open('sql_sql_fwr.csv', mode='w', newline='') as sql_fwr_sql_file_header:
        csvwriter = csv.writer(sql_fwr_sql_file_header, delimiter=',')
        csvwriter.writerow(sql_server_firewall_rules_sql_header)
    with open('SQL Vulnerability Assessments.csv', mode='w', newline='') as sql_va_excel_file_header:
        csvwriter = csv.writer(sql_va_excel_file_header, delimiter=',')
        csvwriter.writerow(sql_db_va_excel_header)
    with open('sql_sql_va.csv', mode='w', newline='') as sql_va_sql_file_header:
        csvwriter = csv.writer(sql_va_sql_file_header, delimiter=',')
        csvwriter.writerow(sql_db_va_sql_header)
    with open('SQL Vulnerability Assessments Scan.csv', mode='w', newline='') as sql_vas_excel_file_header:
        csvwriter = csv.writer(sql_vas_excel_file_header, delimiter=',')
        csvwriter.writerow(sql_db_va_scan_excel_header)
    with open('sql_sql_vas.csv', mode='w', newline='') as sql_vas_sql_file_header:
        csvwriter = csv.writer(sql_vas_sql_file_header, delimiter=',')
        csvwriter.writerow(sql_db_va_scan_sql_header)
    with open('SQL Vulnerability Assessments Scan Results.csv', mode='w', newline='') as sql_vasr_excel_file_header:
        csvwriter = csv.writer(sql_vasr_excel_file_header, delimiter=',')
        csvwriter.writerow(sql_db_vasr_excel_header)
    with open('sql_sql_vasr.csv', mode='w', newline='') as sql_vasr_sql_file_header:
        csvwriter = csv.writer(sql_vasr_sql_file_header, delimiter=',')
        csvwriter.writerow(sql_db_vasr_sql_header)
    # Query API
    get_sql_server = requests.get(url = "https://management.azure.com/subscriptions/"+subscription_id+"/providers/Microsoft.Sql/servers?api-version=2022-05-01-preview", headers = header)
    get_sql_server_to_json = get_sql_server.json()
    # with open("sql_srv.json", "w", encoding="utf-8") as sql_srv_json:
    #     json.dump(get_sql_server_to_json, sql_srv_json, ensure_ascii=False, indent=4)
    if get_sql_server.status_code == 200 or get_sql_server.status_code == 204:
        if "value" in get_sql_server_to_json:
            # Go for SQL Servers
            for server in get_sql_server_to_json["value"]:
                sql_srv_rg_name_split = server["id"].split('/')
                sql_srv_rg_name = sql_srv_rg_name_split[4]
                sql_srv_name = server["name"]
                sql_srv_location = server["location"]
                if "kind" in server:
                    sql_srv_kind = server["kind"]
                else:
                    sql_srv_kind = None
                if "properties" in server:
                    if "version" in server["properties"]:
                        sql_srv_version = server["properties"]["version"]
                    else:
                        sql_srv_version = None
                    if "state" in server["properties"]:
                        sql_srv_status = server["properties"]["state"]
                    else:
                        sql_srv_status = None
                    if "fullyQualifiedDomainName" in server["properties"]:
                        sql_srv_fqdn = server["properties"]["fullyQualifiedDomainName"]
                    else:
                        sql_srv_fqdn = None
                    if "publicNetworkAccess" in server["properties"]:
                        sql_srv_pna = server["properties"]["publicNetworkAccess"]
                    else:
                        sql_srv_pna = None
                # Write Data to CSV
                print("Writing CSV Data for ", sql_srv_name)
                sql_server_excel_data = [subscription_name, sql_srv_rg_name, sql_srv_name, sql_srv_location, sql_srv_kind, sql_srv_version, sql_srv_status, sql_srv_fqdn, sql_srv_pna]
                sql_server_sql_data = [subscription_name, sql_srv_rg_name, sql_srv_name, sql_srv_location, sql_srv_kind, sql_srv_version, sql_srv_status, sql_srv_fqdn, sql_srv_pna]
                with open('SQL Servers.csv', mode='a', newline='') as sql_srv_excel_file_data:
                    csvwriter = csv.writer(sql_srv_excel_file_data, delimiter=',')
                    csvwriter.writerow(sql_server_excel_data)
                with open('sql_sql_srv.csv', mode='a', newline='') as sql_srv_sql_file_data:
                    csvwriter = csv.writer(sql_srv_sql_file_data, delimiter=',')
                    csvwriter.writerow(sql_server_sql_data)
                # Go for SQL Databases
                print("Getting Database Details for ", sql_srv_name)
                get_sql_databases = requests.get(url = "https://management.azure.com"+server["id"]+"/databases?api-version=2022-05-01-preview", headers = header)
                get_sql_databases_to_json = get_sql_databases.json()
                if get_sql_databases.status_code == 200 or get_sql_databases.status_code == 204:
                    if "value" in get_sql_databases_to_json:
                        for database in get_sql_databases_to_json["value"]:
                            sql_db_rg_name_split = database["id"].split('/')
                            sql_db_rg_name = sql_db_rg_name_split[4]
                            sql_db_name = database["name"]
                            sql_db_location = database["location"]
                            if "properties" in database:
                                if "status" in database["properties"]:
                                    sql_db_status = database["properties"]["status"]
                                else:
                                    sql_db_status = None
                                if "maxSizeBytes" in database["properties"]:
                                    sql_db_max_size = database["properties"]["maxSizeBytes"] / 1024 / 1024 / 1024
                                else:
                                    sql_db_max_size = float(0)
                                if "collation" in database["properties"]:
                                    sql_db_collation = database["properties"]["collation"]
                                else:
                                    sql_db_collation = None
                                if "zoneRedundant" in database["properties"]:
                                    sql_db_zone = database["properties"]["zoneRedundant"]
                                else:
                                    sql_db_zone = None
                                if "creationDate" in database["properties"]:
                                    sql_db_creation_date = database["properties"]["creationDate"]
                                else:
                                    sql_db_creation_date = None
                                if "readScale" in database["properties"]:
                                    sql_db_read_scale = database["properties"]["readScale"]
                                else:
                                    sql_db_read_scale = None
                                if "currentBackupStorageRedundancy" in database["properties"]:
                                    sql_db_backup_storage_redundancy = database["properties"]["currentBackupStorageRedundancy"]
                                else:
                                    sql_db_backup_storage_redundancy = None
                            else:
                                sql_db_status = None
                                sql_db_max_size = None
                                sql_db_collation = None
                                sql_db_zone = None
                                sql_db_creation_date = None
                                sql_db_read_scale = None
                                sql_db_backup_storage_redundancy = None
                            if "sku" in database:
                                sql_db_sku_name = database["sku"]["name"]
                                sql_db_sku_tier = database["sku"]["tier"]
                                sql_db_sku_capacity = database["sku"]["capacity"]
                            else:
                                sql_db_sku_name = None
                                sql_db_sku_tier = None
                                sql_db_sku_capacity = None
                            # Write Data to CSV
                            print("Writing Database Details for ", sql_srv_name)
                            sql_database_excel_data = [subscription_name, sql_db_rg_name, sql_srv_name, sql_db_name, sql_db_location, sql_db_status, sql_db_max_size, sql_db_collation, sql_db_zone, sql_db_creation_date, sql_db_sku_name, sql_db_sku_tier, sql_db_sku_capacity, sql_db_read_scale, sql_db_backup_storage_redundancy]
                            sql_database_sql_data = [subscription_name, sql_db_rg_name, sql_srv_name, sql_db_name, sql_db_location, sql_db_status, sql_db_max_size, sql_db_collation, sql_db_zone, sql_db_creation_date, sql_db_sku_name, sql_db_sku_tier, sql_db_sku_capacity, sql_db_read_scale, sql_db_backup_storage_redundancy]
                            with open('SQL Databases.csv', mode='a', newline='') as sql_dbs_excel_file_data:
                                csvwriter = csv.writer(sql_dbs_excel_file_data, delimiter=',')
                                csvwriter.writerow(sql_database_excel_data)
                            with open('sql_sql_dbs.csv', mode='a', newline='') as sql_dbs_sql_file_data:
                                csvwriter = csv.writer(sql_dbs_sql_file_data, delimiter=',')
                                csvwriter.writerow(sql_database_sql_data)
                            # Get Vulnerability Assessment Summary and Results
                            print("Getting Vulnerability Assessment Summary for ", sql_db_name)
                            get_vas_details = requests.get(url = "https://management.azure.com"+database["id"]+"/sqlVulnerabilityAssessments?api-version=2022-05-01-preview", headers = header)
                            get_vas_details_to_json = get_vas_details.json()
                            if get_vas_details.status_code == 200 or get_vas_details.status_code == 204:
                                if "value" in get_vas_details_to_json:
                                    for va in get_vas_details_to_json["value"]:
                                        va_name = va["name"]
                                        va_id = va["id"]
                                        if "properties" in va:
                                            if "state" in va["properties"]:
                                                va_status = va["properties"]["state"]
                                                if va_status == "Enabled":
                                                    get_va_scan_details = requests.get(url = "https://management.azure.com"+database["id"]+"/sqlVulnerabilityAssessments/default/scans?api-version=2022-05-01-preview", headers = header)
                                                    get_va_scan_details_to_json = get_va_scan_details.json()
                                                    if get_va_scan_details.status_code == 200 or get_va_scan_details.status_code == 204:
                                                        if "value" in get_va_scan_details_to_json:
                                                            for vas in get_va_scan_details_to_json["value"]:
                                                                vas_scan_name = vas["name"]
                                                                if "properties" in vas:
                                                                    if "scanId" in vas["properties"]:
                                                                        vas_scan_id = vas["properties"]["scanId"]
                                                                        # Get Vulnerability Assessment Scan Result
                                                                        print("Getting Vulnerability Assessment Scan results for ", sql_db_name)
                                                                        get_vasr_details = requests.get(url = "https://management.azure.com"+database["id"]+"/sqlVulnerabilityAssessments/default/scans/"+vas_scan_id+"/scanResults?api-version=2022-05-01-preview", headers = header)
                                                                        get_vasr_details_to_json = get_vasr_details.json()
                                                                        if get_vasr_details.status_code == 200 or get_vasr_details.status_code == 204:
                                                                            if "value" in get_vasr_details_to_json:
                                                                                for vasr in get_vasr_details_to_json["value"]:
                                                                                    vasr_name = vasr["name"]
                                                                                    if "properties" in vasr:
                                                                                        if "ruleId" in vasr["properties"]:
                                                                                            vasr_rule_id = vasr["properties"]["ruleId"]
                                                                                        else:
                                                                                            vasr_rule_id = None
                                                                                        if "status" in vasr["properties"]:
                                                                                            vasr_rule_status = vasr["properties"]["status"]
                                                                                        else:
                                                                                            vasr_rule_status = None
                                                                                        if "errorMessage" in vasr["properties"]:
                                                                                            vasr_rule_error_message = vasr["properties"]["errorMessage"]
                                                                                        else:
                                                                                            vasr_rule_error_message = None
                                                                                        if "remediation" in vasr["properties"]:
                                                                                            if "description" in vasr["properties"]["remediation"]:
                                                                                                vasr_rule_remediation = vasr["properties"]["remediation"]["description"]
                                                                                            else:
                                                                                                vasr_rule_remediation = None
                                                                                        else:
                                                                                            vasr_rule_remediation = None
                                                                                        if "ruleMetadata" in vasr["properties"]:
                                                                                            if "severity" in vasr["properties"]["ruleMetadata"]:
                                                                                                vasr_rule_severity = vasr["properties"]["ruleMetadata"]["severity"]
                                                                                            else:
                                                                                                vasr_rule_severity = None
                                                                                            if "category" in vasr["properties"]["ruleMetadata"]:
                                                                                                vasr_rule_category = vasr["properties"]["ruleMetadata"]["category"]
                                                                                            else:
                                                                                                vasr_rule_category = None
                                                                                            if "ruleType" in vasr["properties"]["ruleMetadata"]:
                                                                                                vasr_rule_type = vasr["properties"]["ruleMetadata"]["ruleType"]
                                                                                            else:
                                                                                                vasr_rule_type = None
                                                                                            if "title" in vasr["properties"]["ruleMetadata"]:
                                                                                                vasr_rule_title = vasr["properties"]["ruleMetadata"]["title"]
                                                                                            else:
                                                                                                vasr_rule_title = None
                                                                                            if "description" in vasr["properties"]["ruleMetadata"]:
                                                                                                vasr_rule_description = vasr["properties"]["ruleMetadata"]["description"]
                                                                                            else:
                                                                                                vasr_rule_description = None
                                                                                        else:
                                                                                            vasr_rule_severity = None
                                                                                            vasr_rule_category = None
                                                                                            vasr_rule_type = None
                                                                                            vasr_rule_title = None
                                                                                            vasr_rule_description = None
                                                                                        # Write Data to CSV
                                                                                        print("Writing Vulnerability Assessment Scan Results for ", sql_db_name)
                                                                                        sql_db_vasr_excel_data = [subscription_name, sql_srv_rg_name, sql_srv_name, sql_db_name, va_name, va_status, vas_scan_name, vas_scan_id, vasr_name, vasr_rule_id, vasr_rule_status, vasr_rule_severity, vasr_rule_category, vasr_rule_type, vasr_rule_title, vasr_rule_description, vasr_rule_remediation, vasr_rule_error_message]
                                                                                        sql_db_vasr_sql_data = [subscription_name, sql_srv_rg_name, sql_srv_name, sql_db_name, va_name, va_status, vas_scan_name, vas_scan_id, vasr_name, vasr_rule_id, vasr_rule_status, vasr_rule_severity, vasr_rule_category, vasr_rule_type, vasr_rule_title, vasr_rule_description, vasr_rule_remediation, vasr_rule_error_message]
                                                                                        with open('SQL Vulnerability Assessments Scan Results.csv', mode='a', newline='') as sql_vasr_excel_file_data:
                                                                                            csvwriter = csv.writer(sql_vasr_excel_file_data, delimiter=',')
                                                                                            csvwriter.writerow(sql_db_vasr_excel_data)
                                                                                        with open('sql_sql_vasr.csv', mode='a', newline='') as sql_vasr_sql_file_data:
                                                                                            csvwriter = csv.writer(sql_vasr_sql_file_data, delimiter=',')
                                                                                            csvwriter.writerow(sql_db_vasr_sql_data)
                                                                                    else:
                                                                                        print("Vulnerability Assessment Scan Result Property not found for ", sql_db_name)
                                                                            else:
                                                                                print("No Vulnerability Scan Results are found for ", sql_db_name)
                                                                                pass
                                                                        else:
                                                                            print("Error Getting Vulnerability Assessment Scan Results for ", sql_db_name)
                                                                            pass
                                                                    else:
                                                                        vas_scan_id = None
                                                                        print("Vulnerability Assessment scan ID not found for ", sql_db_name)
                                                                        pass
                                                                    if "state" in vas["properties"]:
                                                                        vas_status = vas["properties"]["state"]
                                                                    else:
                                                                        vas_status = None
                                                                    if "triggerType" in vas["properties"]:
                                                                        vas_trigger_type = vas["properties"]["triggerType"]
                                                                    else:
                                                                        vas_trigger_type = None
                                                                    if "highSeverityFailedRulesCount" in vas["properties"]:
                                                                        vas_hs_rules = vas["properties"]["highSeverityFailedRulesCount"]
                                                                    else:
                                                                        vas_hs_rules = None
                                                                    if "mediumSeverityFailedRulesCount" in vas["properties"]:
                                                                        vas_ms_rules = vas["properties"]["mediumSeverityFailedRulesCount"]
                                                                    else:
                                                                        vas_ms_rules = None
                                                                    if "lowSeverityFailedRulesCount" in vas["properties"]:
                                                                        vas_ls_rules = vas["properties"]["lowSeverityFailedRulesCount"]
                                                                    else:
                                                                        vas_ls_rules = None
                                                                    if "totalPassedRulesCount" in vas["properties"]:
                                                                        vas_tp_rules = vas["properties"]["totalPassedRulesCount"]
                                                                    else:
                                                                        vas_tp_rules = None
                                                                    if "totalFailedRulesCount" in vas["properties"]:
                                                                        vas_fs_rules = vas["properties"]["totalFailedRulesCount"]
                                                                    else:
                                                                        vas_fs_rules = None
                                                                    if "totalRulesCount" in vas["properties"]:
                                                                        vas_tr_rules = vas["properties"]["totalRulesCount"]
                                                                    else:
                                                                        vas_tr_rules = None
                                                                    if "isBaselineApplied" in vas["properties"]:
                                                                        vas_ba = vas["properties"]["isBaselineApplied"]
                                                                    else:
                                                                        vas_ba = None
                                                                    # Write Data to CSV
                                                                    print("Writing Vulnerability Assessment Scan Details for ", sql_db_name)
                                                                    sql_db_va_scan_excel_data = [subscription_name, sql_srv_rg_name, sql_srv_name, sql_db_name, va_name, va_status, vas_scan_name, vas_scan_id, vas_status, vas_trigger_type, vas_hs_rules, vas_ms_rules, vas_ls_rules, vas_tp_rules, vas_fs_rules, vas_tr_rules, vas_ba]
                                                                    sql_db_va_scan_sql_data = [subscription_name, sql_srv_rg_name, sql_srv_name, sql_db_name, va_name, va_status, vas_scan_name, vas_scan_id, vas_status, vas_trigger_type, vas_hs_rules, vas_ms_rules, vas_ls_rules, vas_tp_rules, vas_fs_rules, vas_tr_rules, vas_ba]
                                                                    with open('SQL Vulnerability Assessments Scan.csv', mode='a', newline='') as sql_vas_excel_file_data:
                                                                        csvwriter = csv.writer(sql_vas_excel_file_data, delimiter=',')
                                                                        csvwriter.writerow(sql_db_va_scan_excel_data)
                                                                    with open('sql_sql_vas.csv', mode='a', newline='') as sql_vas_sql_file_data:
                                                                        csvwriter = csv.writer(sql_vas_sql_file_data, delimiter=',')
                                                                        csvwriter.writerow(sql_db_va_scan_sql_data)
                                                                else:
                                                                    print("Vulnerability Assessment Scan Properties not found for ", sql_db_name)
                                                                    pass
                                                        else:
                                                            print("Vulnerability Assessment Scan Data not found for ", sql_db_name)
                                                            pass
                                                    else:
                                                        print("Erorr getting Vulneraility Scan API response for ", sql_db_name)
                                                        pass
                                                else:
                                                    print("Vulnerability Status is Disabled for ", sql_db_name)
                                                    pass
                                            else:
                                                va_status = None
                                                print("Vulnerability Assessment Status not found for ", sql_db_name)
                                                pass
                                            # Write Data to Excel
                                            print("Writing Vulnerability Assessment Details for ", sql_db_name)
                                            sql_db_va_excel_data = [subscription_name, sql_srv_rg_name, sql_srv_name, sql_db_name, va_name, va_status]
                                            sql_db_va_sql_data = [subscription_name, sql_srv_rg_name, sql_srv_name, sql_db_name, va_name, va_status]
                                            with open('SQL Vulnerability Assessments.csv', mode='a', newline='') as sql_va_excel_file_data:
                                                csvwriter = csv.writer(sql_va_excel_file_data, delimiter=',')
                                                csvwriter.writerow(sql_db_va_excel_data)
                                            with open('sql_sql_va.csv', mode='a', newline='') as sql_va_sql_file_data:
                                                csvwriter = csv.writer(sql_va_sql_file_data, delimiter=',')
                                                csvwriter.writerow(sql_db_va_sql_data)
                                        else:
                                            print("Vulnerability Assessment Properties not found for ", sql_db_name)
                                            pass
                                else:
                                    print("No Vulnerability Assessment Found for ", sql_db_name)
                                    pass
                            else:
                                print("Error getting Vulnerability Assessment API response for ", sql_db_name)
                                pass
                    else:
                        print("No Database Found for ", sql_srv_name)
                        pass
                else:
                    print("Error getting SQL Database Details for ", sql_srv_name)
                    pass
                # Go for Firewall Rules
                print("Getting Firewall Rules for ", sql_srv_name)
                get_sql_fwr_details = requests.get(url = "https://management.azure.com"+server["id"]+"/firewallRules?api-version=2022-05-01-preview", headers = header)
                get_sql_fwr_details_to_json = get_sql_fwr_details.json()
                if get_sql_fwr_details.status_code == 200 or get_sql_fwr_details.status_code == 204:
                    if "value" in get_sql_fwr_details_to_json:
                        for fwr in get_sql_fwr_details_to_json["value"]:
                            if "name" in fwr:
                                fwr_name = fwr["name"]
                            else:
                                fwr_name = None
                            if "properties" in fwr:
                                if "startIpAddress" in fwr["properties"]:
                                    fwr_start_ip = fwr["properties"]["startIpAddress"]
                                else:
                                    fwr_start_ip = None
                                if "endIpAddress" in fwr["properties"]:
                                    fwr_end_ip = fwr["properties"]["endIpAddress"]
                                else:
                                    fwr_end_ip = None
                            else:
                                fwr_start_ip = None
                                fwr_end_ip = None
                            # Write Data to CSV
                            print("Writing Firewall Rules for ", sql_srv_name)
                            sql_server_firewall_rules_excel_data = [subscription_name, sql_srv_rg_name, sql_srv_name, fwr_name, fwr_start_ip, fwr_end_ip]
                            sql_server_firewall_rules_sql_data = [subscription_name, sql_srv_rg_name, sql_srv_name, fwr_name, fwr_start_ip, fwr_end_ip]
                            with open('SQL Firewall Rules.csv', mode='a', newline='') as sql_fwr_excel_file_data:
                                csvwriter = csv.writer(sql_fwr_excel_file_data, delimiter=',')
                                csvwriter.writerow(sql_server_firewall_rules_excel_data)
                            with open('sql_sql_fwr.csv', mode='a', newline='') as sql_fwr_sql_file_data:
                                csvwriter = csv.writer(sql_fwr_sql_file_data, delimiter=',')
                                csvwriter.writerow(sql_server_firewall_rules_sql_data)
                    else:
                        print("No Firewall Rules found for ", sql_srv_name)
                        pass
                else:
                    print("Error getting SQL Firewall Rules for ", sql_srv_name)
                    pass
        else:
            print("No Value found in API Response for ", subscription_name)
            pass
    else:
        print("Error getting SQL Server Details for ", subscription_name)
        pass