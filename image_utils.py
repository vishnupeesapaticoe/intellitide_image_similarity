import os, uuid, sys
import sys
import shutil
from azure.storage.blob import ContainerClient

sas_url="https://qaadieu2usmediastorage.blob.core.windows.net/pimdigitalassets?sv=2021-10-04&spr=https%2Chttp&st=2023-09-26T09%3A46%3A29Z&se=2023-10-31T09%3A46%3A00Z&sr=c&sp=rlf&sig=3Cr5h7AS1nvJmWzjiJSAD5ySkPKnqvIcELIBLeJguuw%3D"


def list_files(dir_name='Data'):
    container_client = ContainerClient.from_container_url(sas_url)
    container_gen = container_client.list_blob_names()
    print(container_gen.next())


print(list_files())
'''
def download_file(dir_name='Data',sub_dir_name='data'):
    container_client = ContainerClient.from_container_url(sas_url)
    files_list= [i.name for i in container_client.list_blobs() if ('.pdf' in i.name) or ('.txt' in i.name) or ('.docx' in i.name)]
    print(f'Detected files in blob storage : {files_list}')
    try:
        shutil.rmtree(f'{dir_name}/{sub_dir_name}')
    except Exception as e:
        print(e)
    os.makedirs(f'{dir_name}/{sub_dir_name}')
    for filename in files_list:
        with open(f'{dir_name}/{filename}', "wb") as my_file:
            if 'data/' in filename:
                download = container_client.download_blob(filename)
                download.readinto(my_file)
                print(f'Downloaded {filename}')
'''