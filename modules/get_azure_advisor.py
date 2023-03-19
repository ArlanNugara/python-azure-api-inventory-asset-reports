import requests
import json
import sys
import csv
import os

def get_advised(subscription_id, subscription_name, header):
    print("Getting Azure Advisor for ", subscription_name)
    aar_excel_header = ["Subscription", "Impacted Resource", "Resource Type", "Category", "Impact", "Problem", "Solution", "Resource ID"]
    aar_sql_header = ["sub", "impacted_resource", "resource_type", "category", "impact", "problem", "solution", "resource_id"]
    with open('Azure Advisor Recommendation.csv', mode='w', newline='') as aar_excel_file_header:
        csvwriter = csv.writer(aar_excel_file_header, delimiter=',')
        csvwriter.writerow(aar_excel_header)
    with open('sql_aar.csv', mode='w', newline='') as aar_sql_file_header:
        csvwriter = csv.writer(aar_sql_file_header, delimiter=',')
        csvwriter.writerow(aar_sql_header)
    get_recommendation = requests.get(url = "https://management.azure.com/subscriptions/"+subscription_id+"/providers/Microsoft.Advisor/recommendations?api-version=2020-01-01", headers = header)
    get_recommendation_to_json = get_recommendation.json()
    if get_recommendation.status_code == 200 or get_recommendation.status_code == 204:
        if "value" in get_recommendation_to_json:
            for recommendation in get_recommendation_to_json["value"]:
                if "impactedValue" in recommendation["properties"]:
                    impacted_value = recommendation["properties"]["impactedValue"]
                else:
                    impacted_value = None
                if "impactedField" in recommendation["properties"]:
                    impacted_field = recommendation["properties"]["impactedField"]
                else:
                    impacted_field = None
                if "category" in recommendation["properties"]:
                    category = recommendation["properties"]["category"]
                else:
                    category = None
                if "impact" in recommendation["properties"]:
                    impact = recommendation["properties"]["impact"]
                else:
                    impact = None
                aar_excel_data = [subscription_name, impacted_value, impacted_field, category, impact, recommendation["properties"]["shortDescription"]["problem"], recommendation["properties"]["shortDescription"]["solution"], recommendation["properties"]["resourceMetadata"]["resourceId"]]
                aar_sql_data = [subscription_name, impacted_value, impacted_field, category, impact, recommendation["properties"]["shortDescription"]["problem"], recommendation["properties"]["shortDescription"]["solution"], recommendation["properties"]["resourceMetadata"]["resourceId"]]
                with open('Azure Advisor Recommendation.csv', mode='a', newline='') as aar_excel_file_data:
                    csvwriter = csv.writer(aar_excel_file_data, delimiter=',')
                    csvwriter.writerow(aar_excel_data)
                with open('sql_aar.csv', mode='a', newline='') as aar_sql_file_data:
                    csvwriter = csv.writer(aar_sql_file_data, delimiter=',')
                    csvwriter.writerow(aar_sql_data)
            while 'nextLink' in get_recommendation_to_json:
                print("Next Link Found. Querying API for more data")
                get_recommendation = requests.get(url = get_recommendation_to_json["nextLink"], headers = header)
                get_recommendation_to_json = get_recommendation.json()
                if get_recommendation.status_code == 200 or get_recommendation.status_code == 204:
                    if "value" in get_recommendation_to_json:
                        for recommendation in get_recommendation_to_json["value"]:
                            if "impactedValue" in recommendation["properties"]:
                                impacted_value = recommendation["properties"]["impactedValue"]
                            else:
                                impacted_value = None
                            if "impactedField" in recommendation["properties"]:
                                impacted_field = recommendation["properties"]["impactedField"]
                            else:
                                impacted_field = None
                            if "category" in recommendation["properties"]:
                                category = recommendation["properties"]["category"]
                            else:
                                category = None
                            if "impact" in recommendation["properties"]:
                                impact = recommendation["properties"]["impact"]
                            else:
                                impact = None
                            aar_excel_data = [subscription_name, impacted_value, impacted_field, category, impact, recommendation["properties"]["shortDescription"]["problem"], recommendation["properties"]["shortDescription"]["solution"], recommendation["properties"]["resourceMetadata"]["resourceId"]]
                            aar_sql_data = [subscription_name, impacted_value, impacted_field, category, impact, recommendation["properties"]["shortDescription"]["problem"], recommendation["properties"]["shortDescription"]["solution"], recommendation["properties"]["resourceMetadata"]["resourceId"]]
                            with open('Azure Advisor Recommendation.csv', mode='a', newline='') as aar_excel_file_data:
                                csvwriter = csv.writer(aar_excel_file_data, delimiter=',')
                                csvwriter.writerow(aar_excel_data)
                            with open('sql_aar.csv', mode='a', newline='') as aar_sql_file_data:
                                csvwriter = csv.writer(aar_sql_file_data, delimiter=',')
                                csvwriter.writerow(aar_sql_data)
                    else:
                        print("No value returned for Next Link. Exiting")
                else:
                    print("No Recommendation Found for Next Link. Exiting")
        else:
            print("No Recommendation Found for ", subscription_name)
            pass
    else:
        print("No Recommendation Found for ", subscription_name)