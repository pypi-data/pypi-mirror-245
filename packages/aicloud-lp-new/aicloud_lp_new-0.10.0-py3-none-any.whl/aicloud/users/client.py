import requests

base_url = "https://dev-aicloud-gateway.logicplum.com/api/v2"
api_token = "i6DmueJGRHw1UYVcyKXmjSprOEWDRtCC7oqxJKuKzz7wXcAHHO9UPUQLlWt23AHx"

def create_account(data):
    url = f"{base_url}/client/"
    data = {
    "name": "aaa",           #Client Name
    "email": "aaa@yopmail.com", #Client Email
    }
    headers = {"Authorization":api_token}
    response = requests.post(url,json=data,headers=headers)
    return response.text


def create_app(data):
    url = f"{base_url}/app/"
    headers = {"Authorization":api_token}
    response = requests.post(url,json=data,headers=headers)
    return response.json()



   
   