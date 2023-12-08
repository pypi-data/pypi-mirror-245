import requests
import base64

base_url = "https://dev-aicloud-gateway.logicplum.com/api/v2"

def roc_plot(data,client_token):
    url = f"{base_url}/plot/roc"
    headers = {"Authorization":client_token}
    response = requests.post(url, data=data,headers=headers)
    return response.json()


def advanced_lift_chart(data,client_token):
    url = f"{base_url}/plot/advanced-lift-chart"
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data,headers=headers)
    return response.json()


def advanced_feature_impact(data,client_token):
    url = f"{base_url}/plot/advanced-feature-impact"
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data,headers=headers)
    return response.json()



def partial_dependency(data,client_token):
    url = f"{base_url}/plot/partial-dependency"
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data,headers=headers)
    return response.json()




def residual(data,client_token):
    url = f"{base_url}/plot/residual"
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data,headers=headers)
    return response.json()



def predict_vs_actual(data,client_token):
    url = f"{base_url}/plot/predict-vs-actual"
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data,headers=headers)
    return response.json()


def word_cloud(data,client_token):
    url = f"{base_url}/plot/wordcloud"
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data,headers=headers)
    return response.json()




def confusion_matrix(data,client_token):
    url = f"{base_url}/plot/confusion-matrix"
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data,headers=headers)
    return response.json()