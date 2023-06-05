import time
import matplotlib.pyplot as plt
import requests
import sys
import json

backend_url = 'http://127.0.0.1:5000'
# start the session first
response = requests.get(
    url=f"{backend_url}/configuration/start_session")
session = response.cookies.values()[0]
print(session)
headers = {'Cookie': f'session={session}'}

# upload a local file which does NOT include event log import
file_path = sys.path[0]+"/../data/BPI2016_Complaints.csv"
response = requests.post(headers=headers, url=f"{backend_url}/import/upload_local_file",
                         files={"file": open(file_path, "rb")}, data={'separator': ';', "file_type": "csv"})
print(json.loads(response.text))

# you can ask for all the columns in the uploaded file to let the user select the case/time/activity
response = requests.get(
    headers=headers, url=f"{backend_url}/import/get_column_names")
print(json.loads(response.text))


# after setting the columns for case/time/activity you can actually load the event log into the session
response = requests.post(headers=headers, url=f"{backend_url}/import/import_local_file",
                         json={"case": "CustomerID", "time": "ContactDate", "activity": "ComplaintTopic_EN"})
print(json.loads(response.text))


# upload a local file which does NOT include event log import
file_path = sys.path[0]+"/../data/log_vacc.xes"
response = requests.post(headers=headers, url=f"{backend_url}/import/upload_local_file",
                         files={"file": open(file_path, "rb")}, data={'separator': ";", "file_type": "xes"})
print(json.loads(response.text))

# you can ask for all the columns in the uploaded file to let the user select the case/time/activity
response = requests.get(
    headers=headers, url=f"{backend_url}/import/get_column_names")
print(json.loads(response.text))

# after setting the columns for case/time/activity you can actually load the event log into the session
response = requests.post(headers=headers, url=f"{backend_url}/import/import_local_file",
                         json={"case": "Patient", "time": "time:timestamp", "activity": "concept:name"})
print(json.loads(response.text))


response = requests.get(
    headers=headers, url=f"{backend_url}/import/get_imported_data_sets")
print(json.loads(response.text))

response = requests.post(
    headers=headers, url=f"{backend_url}/import/delete_data", json={"name": "BPI2016_Complaints.csv"})
print(json.loads(response.text))


response = requests.get(
    headers=headers, url=f"{backend_url}/import/get_imported_data_sets")
print(json.loads(response.text))


response = requests.post(
    headers=headers, url=f"{backend_url}/import/select_data", json={"name": "log_vacc.xes"})
print(json.loads(response.text))


# if needed, you can reset to all event filters allowed
# response = requests.post(
#    headers=headers, url=f"{backend_url}/event/reset")
# print(json.loads(response.text))

# get parameter for all event filter
response = requests.get(
    headers=headers, url=f"{backend_url}/event/get_parameter")
print(json.loads(response.text))

# set parameter for all event filters (in this demo we are just using the same values again)
response = requests.post(headers=headers, url=f"{backend_url}/event/set_parameter",
                         json=json.loads(json.loads(response.text)["result"]))
print(json.loads(response.text))


# if needed, you can reset to all trace filters allowed
# response = requests.post(
#     headers=headers, url=f"{backend_url}/trace/reset")
# print(json.loads(response.text))

# get parameter for all trace filter
response = requests.get(
    headers=headers, url=f"{backend_url}/trace/get_parameter")
print(json.loads(response.text))

# set parameter for all trace filters (in this demo we are just using the same values again)
response = requests.post(headers=headers, url=f"{backend_url}/trace/set_parameter",
                         json=json.loads(json.loads(response.text)["result"]))
print(json.loads(response.text))


# if needed, you can reset to all algorithms allowed
# response = requests.post(
#     headers=headers, url=f"{backend_url}/algorithm/reset")
# print(json.loads(response.text))

# get parameter for all algorithms
response = requests.get(
    headers=headers, url=f"{backend_url}/algorithm/get_parameter")
print(json.loads(response.text))

# set parameter for all algorithms (in this demo we are just using the same values again)
response = requests.post(headers=headers, url=f"{backend_url}/algorithm/set_parameter",
                         json=json.loads(json.loads(response.text)["result"]))
print(json.loads(response.text))


# if needed, you can reset to all qualities allowed
# response = requests.post(
#     headers=headers, url=f"{backend_url}/quality/reset")
# print(json.loads(response.text))

# get parameter for all qualities
response = requests.get(
    headers=headers, url=f"{backend_url}/quality/get_parameter")
print(json.loads(response.text))

# set parameter for all qualities (in this demo we are just using the same values again)
response = requests.post(headers=headers, url=f"{backend_url}/quality/set_parameter",
                         json=json.loads(json.loads(response.text)["result"]))
print(json.loads(response.text))

response = requests.post(
    headers=headers, url=f"{backend_url}/optimizer/set_timeout", json={"seconds": 600})
print(json.loads(response.text))

response = requests.get(
    headers=headers, url=f"{backend_url}/optimizer/get_all_optimizer")
print(json.loads(response.text))

response = requests.post(
    headers=headers, url=f"{backend_url}/optimizer/set_optimizer", json={"kernel": "NelderMead"})
print(json.loads(response.text))

response = requests.get(
    headers=headers, url=f"{backend_url}/optimizer/run_optimizer")
print(json.loads(response.text))

for _ in range(0,3):
    response = requests.get(
        headers=headers, url=f"{backend_url}/optimizer/get_result")
    print(json.loads(response.text)["result"])
    time.sleep(10)

response = requests.get(
    headers=headers, url=f"{backend_url}/optimizer/stop_optimizer")
print(json.loads(response.text)["result"])