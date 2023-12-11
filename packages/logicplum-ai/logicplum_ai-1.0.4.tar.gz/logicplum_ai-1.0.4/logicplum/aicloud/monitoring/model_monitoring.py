import requests

base_url = "https://dev-aicloud-gateway.logicplum.com/api/v2"

def read_file(file_path):
    with open(file_path, "rb") as file:
        uploaded_filename = file_path.split('\\')[-1]
        content = file.read()
        return uploaded_filename, content
    
def aipilot_model_monitoring(client_token,data,file_path):
    url = f"{base_url}/aipilot_model_monitoring"
    # Get The Monitor Graph Of The Deployed Model
    headers = {"Authorization":client_token}
    uploaded_filename, content = read_file(file_path)
    files = {'file': (uploaded_filename, content)}
    # Send the POST request
    response = requests.post(url, data=data, headers=headers,files=files)
    return response.json()


def comprehensive_model_monitoring(client_token,data,file_path):
    url = f"{base_url}/comprehensive_model_monitoring"
    # Get The Monitor Graph Of The Deployed Model
    headers = {"Authorization":client_token}
    uploaded_filename, content = read_file(file_path)
    files = {'file': (uploaded_filename, content)}
    # Send the POST request
    response = requests.post(url, data=data, headers=headers,files=files)
    return response.json()