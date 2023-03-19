import requests
import json
import sys
import csv
import os
from datetime import date, timedelta

def get_df(subscription_id,subscription_name,header):
    # Create Headers
    df_excel_header = ["Subscription", "Resource Group", "Name", "Location", "Provisioning State", "Public Network Access", "Tags"]
    df_sql_header = ["sub", "rg_name", "name", "location", "provisioning_state", "public_network_access", "tags"]
    dfds_excel_header = ["Subscription", "Resource Group", "Data Factory", "Name", "Type"]
    dfds_sql_header = ["sub", "rg_name", "df_name", "name", "type"]
    dfp_excel_header = ["Subscription", "Resource Group", "Data Factory", "Name", "Description"]
    dfp_sql_header = ["sub", "rg_name", "df_name", "name", "description"]
    dfpr_excel_header = ["Subscription", "Resource Group", "Data Factory", "Pipeline Name", "Pipeline Run ID", "Pipeline Start Time", "Pipeline End Time", "Pipeline Duration", "Pipeline Status", "Message"]
    dfpr_sql_header = ["sub", "rg_name", "df_name", "pipeline_name", "run_id", "run_start", "run_end", "run_duration", "run_status", "message"]
    with open('Data Factory.csv', mode='w', newline='') as df_excel_file_header:
        csvwriter = csv.writer(df_excel_file_header, delimiter=',')
        csvwriter.writerow(df_excel_header)
    with open('sql_df.csv', mode='w', newline='') as df_sql_file_header:
        csvwriter = csv.writer(df_sql_file_header, delimiter=',')
        csvwriter.writerow(df_sql_header)
    with open('Data Factory Dataset.csv', mode='w', newline='') as dfds_excel_file_header:
        csvwriter = csv.writer(dfds_excel_file_header, delimiter=',')
        csvwriter.writerow(dfds_excel_header)
    with open('sql_dfds.csv', mode='w', newline='') as dfds_sql_file_header:
        csvwriter = csv.writer(dfds_sql_file_header, delimiter=',')
        csvwriter.writerow(dfds_sql_header)
    with open('Data Factory Pipeline.csv', mode='w', newline='') as dfp_excel_file_header:
        csvwriter = csv.writer(dfp_excel_file_header, delimiter=',')
        csvwriter.writerow(dfp_excel_header)
    with open('sql_dfp.csv', mode='w', newline='') as dfp_sql_file_header:
        csvwriter = csv.writer(dfp_sql_file_header, delimiter=',')
        csvwriter.writerow(dfp_sql_header)
    with open('Data Factory Pipeline Runs.csv', mode='w', newline='') as dfpr_excel_file_header:
        csvwriter = csv.writer(dfpr_excel_file_header, delimiter=',')
        csvwriter.writerow(dfpr_excel_header)
    with open('sql_dfpr.csv', mode='w', newline='') as dfpr_sql_file_header:
        csvwriter = csv.writer(dfpr_sql_file_header, delimiter=',')
        csvwriter.writerow(dfpr_sql_header)
    # Get Started
    print("Getting Data Factories for ", subscription_name)
    get_df_details = requests.get(url = "https://management.azure.com/subscriptions/"+subscription_id+"/providers/Microsoft.DataFactory/factories?api-version=2018-06-01", headers = header)
    get_df_details_to_json = get_df_details.json()
    if get_df_details.status_code == 200 or get_df_details.status_code == 204:
        if "value" in get_df_details_to_json:
            for df in get_df_details_to_json["value"]:
                df_rg_name_split = df["id"].split('/')
                df_rg_name = df_rg_name_split[4]
                df_name = df["name"]
                df_location = df["location"]
                if "tags" in df:
                    all_tags = []
                    for key,value in df["tags"].items():
                        tag_value = ""+key+"="+value+""
                        all_tags.append(tag_value)
                    tag_csv_value = '\n'.join(all_tags)
                    tag_sql_value = ','.join(all_tags)
                else:
                    tag_csv_value = str()
                    tag_sql_value = "No Tags"
                if "properties" in df:
                    if "provisioningState" in df["properties"]:
                        df_provisioning_status = df["properties"]["provisioningState"]
                    else:
                        df_provisioning_status = None
                    if "publicNetworkAccess" in df["properties"]:
                        df_public_network_access = df["properties"]["publicNetworkAccess"]
                    else:
                        df_public_network_access = None
                else:
                    df_provisioning_status = None
                    df_public_network_access = None
                # Write Data to CSV
                print("Writing Data Factory Details for ", df_name)
                df_excel_data = [subscription_name, df_rg_name, df_name, df_location, df_provisioning_status, df_public_network_access, tag_csv_value]
                df_sql_data = [subscription_name, df_rg_name, df_name, df_location, df_provisioning_status, df_public_network_access, tag_sql_value]
                with open('Data Factory.csv', mode='a', newline='') as df_excel_file_data:
                    csvwriter = csv.writer(df_excel_file_data, delimiter=',')
                    csvwriter.writerow(df_excel_data)
                with open('sql_df.csv', mode='a', newline='') as df_sql_file_data:
                    csvwriter = csv.writer(df_sql_file_data, delimiter=',')
                    csvwriter.writerow(df_sql_data)
                
                # Get Datasets
                print("Getting Dataset Details for ", df_name)
                get_df_dataset = requests.get(url = "https://management.azure.com"+df["id"]+"/datasets?api-version=2018-06-01", headers = header)
                get_df_dataset_to_json = get_df_dataset.json()
                if get_df_dataset.status_code == 200 or get_df_dataset.status_code == 204:
                    if "value" in get_df_dataset_to_json:
                        for dfds in get_df_dataset_to_json["value"]:
                            dfds_name = dfds["name"]
                            if "properties" in dfds:
                                if "type" in dfds["properties"]:
                                    dfds_type = dfds["properties"]["type"]
                                else:
                                    dfds_type = None
                            else:
                                dfds_type = None
                            # Write Data Factory Dataset to CSV
                            print("Writing Data Factory Dataset Details for ", df_name)
                            dfds_excel_data = [subscription_name, df_rg_name, df_name, dfds_name, dfds_type]
                            dfds_sql_data = [subscription_name, df_rg_name, df_name, dfds_name, dfds_type]
                            with open('Data Factory Dataset.csv', mode='a', newline='') as dfds_excel_file_data:
                                csvwriter = csv.writer(dfds_excel_file_data, delimiter=',')
                                csvwriter.writerow(dfds_excel_data)
                            with open('sql_dfds.csv', mode='a', newline='') as dfds_sql_file_data:
                                csvwriter = csv.writer(dfds_sql_file_data, delimiter=',')
                                csvwriter.writerow(dfds_sql_data)
                        while 'nextLink' in get_df_dataset_to_json:
                            print("Next Link Found. Querying API for more data")
                            get_df_dataset = requests.get(url = get_df_dataset_to_json["nextLink"], headers = header)
                            get_df_dataset_to_json = get_df_dataset.json()
                            if get_df_dataset.status_code == 200 or get_df_dataset.status_code == 204:
                                if "value" in get_df_dataset_to_json:
                                    for dfds in get_df_dataset_to_json["value"]:
                                        dfds_name = dfds["name"]
                                        if "properties" in dfds:
                                            if "type" in dfds["properties"]:
                                                dfds_type = dfds["properties"]["type"]
                                            else:
                                                dfds_type = None
                                        else:
                                            dfds_type = None
                                        # Write Data Factory Dataset to CSV
                                        print("Writing Data Factory Dataset Details for ", df_name)
                                        dfds_excel_data = [subscription_name, df_rg_name, df_name, dfds_name, dfds_type]
                                        dfds_sql_data = [subscription_name, df_rg_name, df_name, dfds_name, dfds_type]
                                        with open('Data Factory Dataset.csv', mode='a', newline='') as dfds_excel_file_data:
                                            csvwriter = csv.writer(dfds_excel_file_data, delimiter=',')
                                            csvwriter.writerow(dfds_excel_data)
                                        with open('sql_dfds.csv', mode='a', newline='') as dfds_sql_file_data:
                                            csvwriter = csv.writer(dfds_sql_file_data, delimiter=',')
                                            csvwriter.writerow(dfds_sql_data)
                                else:
                                    print("No Data Factory Dataset found for ", df_name)
                                    pass
                            else:
                                print("Error getting response for Data Factory Dataset for ", df_name)
                                pass
                    else:
                        print("No Data Factory Dataset found for ", df_name)
                        pass
                else:
                    print("Error getting response for Data Factory Dataset for ", df_name)
                    pass
                
                # Get Pipeline Details
                print("Getting Data Factory Pipeline Details for ", df_name)
                get_df_pipeline = requests.get(url = "https://management.azure.com"+df["id"]+"/pipelines?api-version=2018-06-01", headers = header)
                get_df_pipeline_to_json = get_df_pipeline.json()
                if get_df_pipeline.status_code == 200 or get_df_pipeline.status_code == 204:
                    if "value" in get_df_pipeline_to_json:
                        for dfp in get_df_pipeline_to_json["value"]:
                            dfp_name = dfp["name"]
                            if "properties" in dfp:
                                if "description" in dfp["properties"]:
                                    dfp_description = dfp["properties"]["description"]
                                else:
                                    dfp_description = None
                            else:
                                dfp_description = None
                            # Write Data Factory Pipeline Details to CSV
                            print("Writing Data Factory Pipeline Details for ", df_name)
                            dfp_excel_data = [subscription_name, df_rg_name, df_name, dfp_name, dfp_description]
                            dfp_sql_data = [subscription_name, df_rg_name, df_name, dfp_name, dfp_description]
                            with open('Data Factory Pipeline.csv', mode='a', newline='') as dfp_excel_file_data:
                                csvwriter = csv.writer(dfp_excel_file_data, delimiter=',')
                                csvwriter.writerow(dfp_excel_data)
                            with open('sql_dfp.csv', mode='a', newline='') as dfp_sql_file_data:
                                csvwriter = csv.writer(dfp_sql_file_data, delimiter=',')
                                csvwriter.writerow(dfp_sql_data)
                        while 'nextLink' in get_df_pipeline_to_json:
                            print("Next Link Found. Querying API for more data")
                            get_df_pipeline = requests.get(url = get_df_pipeline_to_json["nextLink"], headers = header)
                            get_df_pipeline_to_json = get_df_pipeline.json()
                            if get_df_pipeline.status_code == 200 or get_df_pipeline.status_code == 204:
                                if "value" in get_df_pipeline_to_json:
                                    for dfp in get_df_pipeline_to_json["value"]:
                                        dfp_name = dfp["name"]
                                        if "properties" in dfp:
                                            if "description" in dfp["properties"]:
                                                dfp_description = dfp["properties"]["description"]
                                            else:
                                                dfp_description = None
                                        else:
                                            dfp_description = None
                                        # Write Data Factory Pipeline Details to CSV
                                        print("Writing Data Factory Pipeline Details for ", df_name)
                                        dfp_excel_data = [subscription_name, df_rg_name, df_name, dfp_name, dfp_description]
                                        dfp_sql_data = [subscription_name, df_rg_name, df_name, dfp_name, dfp_description]
                                        with open('Data Factory Pipeline.csv', mode='a', newline='') as dfp_excel_file_data:
                                            csvwriter = csv.writer(dfp_excel_file_data, delimiter=',')
                                            csvwriter.writerow(dfp_excel_data)
                                        with open('sql_dfp.csv', mode='a', newline='') as dfp_sql_file_data:
                                            csvwriter = csv.writer(dfp_sql_file_data, delimiter=',')
                                            csvwriter.writerow(dfp_sql_data)
                                else:
                                    print("No Data Factory Pipeline Found for ", df_name)
                                    pass
                            else:
                                print("Error Getting API response for Data Factory Pipelines for ", df_name)
                                pass
                    else:
                        print("No Data Factory Pipeline Found for ", df_name)
                        pass
                else:
                    print("Error Getting API response for Data Factory Pipelines for ", df_name)
                    pass

                # Get Pipeline Runs Details
                print("Getting Pipeline Run Details for ", df_name)
                date_today = date.today()
                date_yesterday = date_today - timedelta(days = 1)
                payload = {"lastUpdatedAfter": ""+str(date_yesterday)+"T00:00:00Z", "lastUpdatedBefore": ""+str(date_today)+"T00:00:00Z"}
                get_df_pipeline_runs = requests.post(url = "https://management.azure.com"+df["id"]+"/queryPipelineRuns?api-version=2018-06-01", headers = header, json = payload)
                get_df_pipeline_runs_to_json = get_df_pipeline_runs.json()
                if get_df_pipeline_runs.status_code == 200 or get_df_pipeline_runs.status_code == 204:
                    if "value" in get_df_pipeline_runs_to_json:
                        for dfpr in get_df_pipeline_runs_to_json["value"]:
                            dfp_name = dfpr["pipelineName"]
                            dfpr_run_id = dfpr["runId"]
                            dfpr_run_start = dfpr["runStart"]
                            if "runEnd" in dfpr:
                                dfpr_run_end = dfpr["runEnd"]
                            else:
                                dfpr_run_end = None
                            if "durationInMs" in dfpr:
                                dfpr_duration = dfpr["durationInMs"]
                            else:
                                dfpr_duration = None
                            if "status" in dfpr:
                                dfpr_status = dfpr["status"]
                            else:
                                dfpr_status = None
                            if "message" in dfpr:
                                dfpr_message = dfpr["message"]
                            else:
                                dfpr_message = None
                            # Write Data Factory Pipeline Runs to CSV
                            print("Writing Data Factory Pipeline Runs Details for ", df_name)
                            dfpr_excel_data = [subscription_name, df_rg_name, df_name, dfp_name, dfpr_run_id, dfpr_run_start, dfpr_run_end, dfpr_duration, dfpr_status, dfpr_message]
                            dfpr_sql_data = [subscription_name, df_rg_name, df_name, dfp_name, dfpr_run_id, dfpr_run_start, dfpr_run_end, dfpr_duration, dfpr_status, dfpr_message]
                            with open('Data Factory Pipeline Runs.csv', mode='a', newline='') as dfpr_excel_file_data:
                                csvwriter = csv.writer(dfpr_excel_file_data, delimiter=',')
                                csvwriter.writerow(dfpr_excel_data)
                            with open('sql_dfpr.csv', mode='a', newline='') as dfpr_sql_file_data:
                                csvwriter = csv.writer(dfpr_sql_file_data, delimiter=',')
                                csvwriter.writerow(dfpr_sql_data)
                    else:
                        print("No Data Factory Pipeline Runs found for ", df_name)
                        pass
                else:
                    print("Error Getting Data Factory Pipeline Run Details for ", df_name)
                    pass
        else:
            print("No Data Factory found for ", subscription_name)
            pass
    else:
        print("Erorr getting response from Data Factory API for ", subscription_name)
        pass