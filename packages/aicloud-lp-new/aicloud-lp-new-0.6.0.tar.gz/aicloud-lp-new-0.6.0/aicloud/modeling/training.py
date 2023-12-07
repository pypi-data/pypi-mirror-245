import requests


base_url = "https://dev-aicloud-gateway.logicplum.com/api/v2" 
api_token = "i6DmueJGRHw1UYVcyKXmjSprOEWDRtCC7oqxJKuKzz7wXcAHHO9UPUQLlWt23AHx"


def read_csv(file_path):
    with open(file_path, "rb") as file:
        uploaded_filename = file_path.split('\\')[-1]
        content = file.read()
        return uploaded_filename,content
    

def aipilot_modeling(file_path,client_token,data):
    uploaded_filename,content = read_csv(file_path)
    #model creation
    url = f"{base_url}/training/create_model"
    files = {'file': (uploaded_filename, content)}
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data, files=files,headers=headers)
    return response.json()
  


def quick_modeling(file_path,client_token,data):
    uploaded_filename,content = read_csv(file_path)
    url = f"{base_url}/training/quick-create_model"
    files = {'file': (uploaded_filename, content)}
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data, files=files,headers=headers)
    return response.json()



def manual_modeling(file_path,client_token,data):
    uploaded_filename,content = read_csv(file_path)
    url = f"{base_url}/training/manual-create_model"
    files = {'file': (uploaded_filename, content)}
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data, files=files,headers=headers)
    return response.json()


def comprehensive_modeling(file_path,client_token,data):
    uploaded_filename,content = read_csv(file_path)
    #model creation
    url = f"{base_url}/training/comprehensive-create_model"
    files = {'file': (uploaded_filename, content)}
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data, files=files,headers=headers)
    return response.json()








data= {
"app_id": '4e56d192-23e2-4b28-a179-13868504d133',
"target": "charges",
"max_iterations": 10,
"blended_models": False,
"max_time":180,
"new_feature_extract": False,
"number_features":20,
    
# "advancedOptions":advancedOptions
}

client_token = "eyJuYW1lIjoicHJvZHRlc3R1c2VyMDAyIiwiZW1haWwiOiJwcm9kdGVzdHVzZXIwMDJAeW9wbWFpbC5jb20ifQ:1r6TnQ:AGjWzxYwlpXzgHzoo4VF_c-qdRV45s9iZYCGjX1-g9o"
file_path = r"C:\Users\Aswin\Downloads\insurance.csv"
print(aipilot_modeling(file_path,client_token,data))