import requests

base_url = "https://dev-aicloud-gateway.logicplum.com/api/v2"

def read_file(file_path):
    with open(file_path, "rb") as file:
        uploaded_filename = file_path.split('\\')[-1]
        content = file.read()
        return uploaded_filename, content
import base64
def aipilot_model_monitoring(client_token,data,file_path):
    url = f"{base_url}/training/aipilot/monitor-model"
    # Get The Monitor Graph Of The Deployed Model
    headers = {"Authorization":client_token}
    uploaded_filename, content = read_file(file_path)
    files = {'file': (uploaded_filename, content)}
    # Send the POST request
    response = requests.post(url, data=data, headers=headers,files=files)
    if data.get('res_type') == 'image':
        return response.content
    return response.json()


def comprehensive_model_monitoring(client_token,data,file_path):
    url = f"{base_url}/training/comprehensive/monitor-model"
    # Get The Monitor Graph Of The Deployed Model
    headers = {"Authorization":client_token}
    uploaded_filename, content = read_file(file_path)
    files = {'file': (uploaded_filename, content)}
    # Send the POST request
    response = requests.post(url, data=data, headers=headers,files=files)
    if data.get('res_type') == 'image':
        return response.content
    return response.json()

client_token="eyJuYW1lIjoiYWFhMiIsImVtYWlsIjoiYTJhYUB5b3BtYWlsLmNvbSJ9:1rBDLh:Nbt5XzVcLQFgHu4uzqBPPp5da1RYJQTtLWsTnNRtB4E"
deployment_id = "37621e2b-2b3f-424e-815d-e2fbe4672ea4"
file_path = r"C:\WORK\AI CLOUD 4.0\csv\IRIS.csv"
data = {
    'res_type':'image',
    'deployment_id': deployment_id
}
aipilot_model_monitoring(client_token,data,file_path)
# display(Image(data=binary_data))