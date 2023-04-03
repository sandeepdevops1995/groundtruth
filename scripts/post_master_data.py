import requests
import json
from master_data import gateway_ports_data,wagon_master_data

IP = "0.0.0.0"
PORT = "8040"
API_KEY = "pbkdf2_sha256$320000$KC5jIA4n1WFBWeGtFSYTSM$tvM5FUFHiwPu5ZTb+nf3n5Ikw7g0wfuvZN9cQ+4lPqc="
CLIENT_ID = "ground_truth"

base_url = "http://"+IP+":"+PORT
gateway_port_path = "/gateway_port"
wagon_master_path = "/wagon"



def post_data_to_ground_truth(url,data):
    try:
        headers = {'content-type': 'application/json','Authorization': API_KEY,'Client-Id' : CLIENT_ID}
        response = requests.post(url,headers=headers,data=json.dumps(data))
        if response.status_code in [200,201]:
            print("data posted to ground truth")
        elif response.status_code == 401:
            print("please change the API_KEY")
        print(response.status_code,response.content)
    except Exception as e:
        print("Unable to post data to ground truth",e)
        
def post_gateway_port():
    url = base_url+gateway_port_path
    print("---------posting gateway port data to ground truth----------")
    post_data_to_ground_truth(url,gateway_ports_data)

def post_wagon_master_data():
    url = base_url+wagon_master_path
    print("---------posting wagons master data to ground truth----------")
    post_data_to_ground_truth(url,wagon_master_data)
    
    
if __name__ == "__main__":
    post_gateway_port()
    post_wagon_master_data()