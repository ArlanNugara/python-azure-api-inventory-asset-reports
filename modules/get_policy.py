import requests
import json
import sys
import csv
import os

def policy_assignment(subscription_id, subscription_name, header):
    print("Getting Policy Assignment Details for ", subscription_name)
    pa_excel_header = ["Subscription", "Name", "Enforcement Mode", "Location", "Scope"]
    pa_sql_header = ["sub", "name", "enforcement", "location", "scope"]
    with open('Policy Assignments.csv', mode = 'w', newline='') as pa_excel_file_header:
        csvwriter = csv.writer(pa_excel_file_header, delimiter=',')
        csvwriter.writerow(pa_excel_header)
    with open('sql_policy_assignments.csv', mode = 'w', newline='') as pa_sql_file_header:
        csvwriter = csv.writer(pa_sql_file_header, delimiter=',')
        csvwriter.writerow(pa_sql_header)
    get_policy_assignment_list = requests.get(url = "https://management.azure.com/subscriptions/"+subscription_id+"/providers/Microsoft.Authorization/policyAssignments?api-version=2022-06-01", headers = header)
    get_policy_assignment_list_to_json = get_policy_assignment_list.json()
    if get_policy_assignment_list.status_code == 200 or get_policy_assignment_list.status_code == 204:
        if "value" in get_policy_assignment_list_to_json:
            for pa in get_policy_assignment_list_to_json["value"]:
                if "location" in pa:
                    location = pa["location"]
                else:
                    location = None
                pa_excel_data = [subscription_name, pa["properties"]["displayName"], pa["properties"]["enforcementMode"], location, pa["properties"]["scope"]]
                pa_sql_data = [subscription_name, pa["properties"]["displayName"], pa["properties"]["enforcementMode"], location, pa["properties"]["scope"]]
                with open('Policy Assignments.csv', mode = 'a', newline='') as pa_excel_file_data:
                    csvwriter = csv.writer(pa_excel_file_data, delimiter=',')
                    csvwriter.writerow(pa_excel_data)
                with open('sql_policy_assignments.csv', mode = 'a', newline='') as pa_sql_file_data:
                    csvwriter = csv.writer(pa_sql_file_data, delimiter=',')
                    csvwriter.writerow(pa_sql_data)
            print("Writing Policy Assignment Details for ", subscription_name)
        else:
            print("No Policy Assignment Found. Exiting..")
    else:
        print("Error getting Policy Assignments")

def policy_assessment(subscription_id, subscription_name, header):
    print("Getting Policy Assessment for ", subscription_name)
    assessment_excel_header = ["Subscription", "Assessment ID", "Name", "Status", "Source", "Resource ID"]
    assessment_sql_header = ["sub", "assessment_id", "name", "status", "source", "resource_id"]
    with open('Policy Assessments.csv', mode = 'w', newline='') as pa_excel_file_header:
        csvwriter = csv.writer(pa_excel_file_header, delimiter=',')
        csvwriter.writerow(assessment_excel_header)
    with open('sql_policy_assessment.csv', mode = 'w', newline='') as pa_sql_file_header:
        csvwriter = csv.writer(pa_sql_file_header, delimiter=',')
        csvwriter.writerow(assessment_sql_header)
    get_policy_assessment = requests.get(url = "https://management.azure.com/subscriptions/"+subscription_id+"/providers/Microsoft.Security/assessments?api-version=2020-01-01", headers = header)
    get_policy_assessment_to_json = get_policy_assessment.json()
    if get_policy_assessment.status_code == 200 or get_policy_assessment.status_code == 204:
        if "value" in get_policy_assessment_to_json:
            for assessment in get_policy_assessment_to_json["value"]:
                if "Id" in assessment["properties"]["resourceDetails"]:
                    id = assessment["properties"]["resourceDetails"]["Id"]
                else:
                    id = None
                assessment_excel_data = [subscription_name, assessment["name"], assessment["properties"]["displayName"], assessment["properties"]["status"]["code"], assessment["properties"]["resourceDetails"]["Source"], id]
                assessment_sql_data = [subscription_name, assessment["name"], assessment["properties"]["displayName"], assessment["properties"]["status"]["code"], assessment["properties"]["resourceDetails"]["Source"], id]
                with open('Policy Assessments.csv', mode = 'a', newline='') as pa_excel_file_data:
                    csvwriter = csv.writer(pa_excel_file_data, delimiter=',')
                    csvwriter.writerow(assessment_excel_data)
                with open('sql_policy_assessment.csv', mode = 'a', newline='') as pa_sql_file_data:
                    csvwriter = csv.writer(pa_sql_file_data, delimiter=',')
                    csvwriter.writerow(assessment_sql_data)
            while 'nextLink' in get_policy_assessment_to_json:
                print("Next Link Found. Querying API for more data")
                get_policy_assessment = requests.get(url = get_policy_assessment_to_json["nextLink"], headers = header)
                get_policy_assessment_to_json = get_policy_assessment.json()
                if get_policy_assessment.status_code == 200 or get_policy_assessment.status_code == 204:
                    if "value" in get_policy_assessment_to_json:
                        for assessment in get_policy_assessment_to_json["value"]:
                            assessment_excel_data = [subscription_name, assessment["name"], assessment["properties"]["displayName"], assessment["properties"]["status"]["code"], assessment["properties"]["resourceDetails"]["Source"], id]
                            assessment_sql_data = [subscription_name, assessment["name"], assessment["properties"]["displayName"], assessment["properties"]["status"]["code"], assessment["properties"]["resourceDetails"]["Source"], id]
                            with open('Policy Assessments.csv', mode = 'a', newline='') as pa_excel_file_data:
                                csvwriter = csv.writer(pa_excel_file_data, delimiter=',')
                                csvwriter.writerow(assessment_excel_data)
                            with open('sql_policy_assessment.csv', mode = 'a', newline='') as pa_sql_file_data:
                                csvwriter = csv.writer(pa_sql_file_data, delimiter=',')
                                csvwriter.writerow(assessment_sql_data)
                    else:
                        print("No value returned for Next Link. Exiting")
                else:
                    print("No Assessment Found for Next Link. Exiting")
        else:
            print("No Policy Assessment Found. Exiting..")
    else:
        print("Error Getting Policy Assessment.")

def policy_rcs(subscription_id, subscription_name, header):
    print("Getting Regulatory Copliance Standards for ", subscription_name)
    rcs_excel_header = ["Subscription", "Name", "Status", "Passed Controls", "Failed Controls", "Skipped Controls", "Unsupported Controls"]
    rcs_sql_header = ["sub", "name", "status", "passed_controls", "failed_controls", "skipped_controls", "unsupported_controls"]
    rcc_excel_header = ["Subscription", "Compliance Name", "Control Name", "Description", "Status", "Passed Assessment", "Failed Assessment", "Skipped Assessment"]
    rcc_sql_header = ["sub", "compliance_name", "control_name", "description", "status", "passed_assessment", "failed_assessment", "skipped_assessment"]
    with open('Regulatory Compliance Standards.csv', mode = 'w', newline='') as rcs_excel_file_header:
        csvwriter = csv.writer(rcs_excel_file_header, delimiter=',')
        csvwriter.writerow(rcs_excel_header)
    with open('sql_rcs.csv', mode = 'w', newline='') as rcs_sql_file_header:
        csvwriter = csv.writer(rcs_sql_file_header, delimiter=',')
        csvwriter.writerow(rcs_sql_header)
    with open('Regulatory Compliance Controls.csv', mode = 'w', newline='') as rcc_excel_file_header:
        csvwriter = csv.writer(rcc_excel_file_header, delimiter=',')
        csvwriter.writerow(rcc_excel_header)
    with open('sql_rcc.csv', mode = 'w', newline='') as rcc_sql_file_header:
        csvwriter = csv.writer(rcc_sql_file_header, delimiter=',')
        csvwriter.writerow(rcc_sql_header)
    get_rcs = requests.get(url = "https://management.azure.com/subscriptions/"+subscription_id+"/providers/Microsoft.Security/regulatoryComplianceStandards?api-version=2019-01-01-preview", headers = header)
    get_rcs_to_json = get_rcs.json()
    if get_rcs.status_code == 200 or get_rcs.status_code == 204:
        if "value" in get_rcs_to_json:
            print("Writing Data for Regulatory Compliance Standards for ", subscription_name)
            for rcs_details in get_rcs_to_json["value"]:
                rcs_excel_data = [subscription_name, rcs_details["name"], rcs_details["properties"]["state"], rcs_details["properties"]["passedControls"], rcs_details["properties"]["failedControls"], rcs_details["properties"]["skippedControls"], rcs_details["properties"]["unsupportedControls"]]
                rcs_sql_data = [subscription_name, rcs_details["name"], rcs_details["properties"]["state"], rcs_details["properties"]["passedControls"], rcs_details["properties"]["failedControls"], rcs_details["properties"]["skippedControls"], rcs_details["properties"]["unsupportedControls"]]
                with open('Regulatory Compliance Standards.csv', mode = 'a', newline='') as rcs_excel_file_data:
                    csvwriter = csv.writer(rcs_excel_file_data, delimiter=',')
                    csvwriter.writerow(rcs_excel_data)
                with open('sql_rcs.csv', mode = 'a', newline='') as rcs_sql_file_data:
                    csvwriter = csv.writer(rcs_sql_file_data, delimiter=',')
                    csvwriter.writerow(rcs_sql_data)
                # Get Regulatory Compliance Control Details
                print("Getting Control Status for ", rcs_details["name"])
                get_rcc = requests.get(url = "https://management.azure.com/subscriptions/"+subscription_id+"/providers/Microsoft.Security/regulatoryComplianceStandards/"+rcs_details["name"]+"/regulatoryComplianceControls?api-version=2019-01-01-preview", headers = header)
                get_rcc_to_json = get_rcc.json()
                if get_rcc.status_code == 200 or get_rcc.status_code == 204:
                    if "value" in get_rcc_to_json:
                        for rcc_details in get_rcc_to_json["value"]:
                            rcc_excel_data = [subscription_name, rcs_details["name"], rcc_details["name"], rcc_details["properties"]["description"], rcc_details["properties"]["state"], rcc_details["properties"]["passedAssessments"], rcc_details["properties"]["failedAssessments"], rcc_details["properties"]["skippedAssessments"]]
                            rcc_sql_data = [subscription_name, rcs_details["name"], rcc_details["name"], rcc_details["properties"]["description"], rcc_details["properties"]["state"], rcc_details["properties"]["passedAssessments"], rcc_details["properties"]["failedAssessments"], rcc_details["properties"]["skippedAssessments"]]
                            with open('Regulatory Compliance Controls.csv', mode = 'a', newline='') as rcc_excel_file_data:
                                csvwriter = csv.writer(rcc_excel_file_data, delimiter=',')
                                csvwriter.writerow(rcc_excel_data)
                            with open('sql_rcc.csv', mode = 'a', newline='') as rcc_sql_file_data:
                                csvwriter = csv.writer(rcc_sql_file_data, delimiter=',')
                                csvwriter.writerow(rcc_sql_data)
                    else:
                        print("No Data Found for Regulatory Compliance Controls ", rcs_details["name"])
                        pass
                else:
                    print("Error getting response for Regulatory Compliance Controls ", rcs_details["name"])
                    pass
        else:
            print("No Data found for Regulatory Compliance Standard")
    else:
        print("Error getting response for Regulatory Compliance Standard")