from locust import HttpUser, task,between
import json
import random
from rich.console import Console
console = Console()
images_list = open('images_list.txt','r').read().split('\n')
def get_api_payload():
    return {'source_url':random.choice(images_list),'target_url':random.sample(images_list,1)}
class QuickstartUser(HttpUser):
    wait_time = between(1, 2)
    def on_start(self):
        print('started')

    @task
    def predict_test(self):
        try:
            global count
            json_data = get_api_payload()
            result = self.client.post("/predict", json=json_data)
            console.log(f"request : {json_data} | result: {result.text}",style='green')
            console.log('#'*10,style='red')
        except Exception as e:
            print(e)

