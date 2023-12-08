import requests
import base64
import json 

base_url = "https://dev-aicloud-gateway.logicplum.com/api/v2"
api_token = "i6DmueJGRHw1UYVcyKXmjSprOEWDRtCC7oqxJKuKzz7wXcAHHO9UPUQLlWt23AHx"

def reports(data,client_token):
    url = f'{base_url}/plot/report'
    headers = {"Authorization":client_token}
    response = requests.post(url, data=data,headers=headers)
    pdf_data = response.content
    pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
    data = {
        'result': pdf_base64
    }
    json_string = json.dumps(data)
    return json_string