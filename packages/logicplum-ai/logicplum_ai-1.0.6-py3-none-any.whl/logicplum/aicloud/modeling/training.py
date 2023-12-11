import requests

base_url = "https://dev-aicloud-gateway.logicplum.com/api/v2"
api_token = "i6DmueJGRHw1UYVcyKXmjSprOEWDRtCC7oqxJKuKzz7wXcAHHO9UPUQLlWt23AHx"

def read_file(file_path):
    with open(file_path, "rb") as file:
        uploaded_filename = file_path.split('\\')[-1]
        content = file.read()
        return uploaded_filename, content

def create_model(file_path, endpoint, client_token, data):
    uploaded_filename, content = read_file(file_path)
    url = f"{base_url}/training/{endpoint}"
    files = {'file': (uploaded_filename, content)}
    headers = {"Authorization": client_token}
    # Send the POST request
    response = requests.post(url, data=data, files=files, headers=headers)
    return response.json()

def aipilot_modeling(file_path, client_token, data):
    return create_model(file_path, "create_model", client_token, data)

def quick_modeling(file_path, client_token, data):
    return create_model(file_path, "quick-create_model", client_token, data)

def manual_modeling(file_path, client_token, data):
    return create_model(file_path, "manual-create_model", client_token, data)

def comprehensive_modeling(file_path, client_token, data):
    return create_model(file_path, "comprehensive-create_model", client_token, data)




def model_deployment(data,client_token):
    try:

        url = f"{base_url}/training/deployment"
        headers = {"Authorization":client_token}
        # Send the POST request
        response = requests.post(url, data=data, headers=headers)
        return response.json()
    except:
        return "manual model has no deployment"
    




def get_training_result(project_id,client_token):
    url = f"{base_url}/training/get-results/{project_id}"
    headers = {"Authorization": client_token}
    response = requests.get(url, headers=headers)
    response_json=response.json()
    return response_json



def get_holdout_result(data,client_token):
    url = f"{base_url}/training/model-results"
    headers = {"Authorization":client_token}
    response = requests.post(url,headers=headers,data=data)
    return response.json()
