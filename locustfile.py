from locust import HttpUser, task,between
import json
import random
import os
import base64
from rich.console import Console
console = Console()

# Function to convert an image file to a base64 string
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

images_list = open('images_list.txt','r').read().split('\n')
dir = "/home/vishnu/Downloads/USFFileDownload/img/"
images_list_base64 = [f"{dir}{i}" for i in os.listdir(dir)]
def get_api_payload():
    return {'source_url':random.choice(images_list),'target_url':random.sample(images_list,1)}
def get_api_payload_base64():
    source_image_path = random.choice(images_list_base64)
    source_base_64 = encode_image_to_base64(source_image_path)
    target_image_path = random.sample(images_list_base64,3)
    target_base_64 = [encode_image_to_base64(i) for i in target_image_path]
    return {'source_url':source_base_64,'target_url':target_base_64} , source_image_path, target_image_path
class QuickstartUser(HttpUser):
    wait_time = between(1, 2)
    def on_start(self):
        print('started')

    # @task
    # def predict_test_http(self):
    #     try:
    #         global count
    #         json_data = get_api_payload()
    #         result = self.client.post("/predict", json=json_data)
    #         console.log(f"request : {json_data} | result: {result.text}",style='green')
    #         console.log('#'*10,style='red')
    #     except Exception as e:
    #         print(e)
    @task 
    def predict_test_base64(self):
        try:
            json_data,source_image_path,target_image_path = get_api_payload_base64()
            console.log('#'*10,style='red')
            console.log(f"Source image : {source_image_path}")
            console.log(f"target image : {target_image_path}")
            result = self.client.post("/predict_base64", json=json_data)
            console.log(f"result: {result.text}",style='green')
            console.log('#'*10,style='red')
        except Exception as e:
            print(e)   
