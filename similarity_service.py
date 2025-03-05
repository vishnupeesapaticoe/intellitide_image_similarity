import io
import validators
import requests
from PIL import Image
from functools import lru_cache
import tempfile
import traceback
from rich.console import Console
import time
import pandas as pd
from concurrent.futures.thread import ThreadPoolExecutor
from embedding_utils import get_image_embedding , get_norm , get_cosine_similarity
import base64
console = Console()
start  = time.time()
#image_urls = open('images_list.txt','r').read().split('\n')


def split_list_into_n_lists(list1, n):
  ''' WIll split a list into n lists'''
  chunks = []
  chunk_size = len(list1) // n
  start_index = 0
  for i in range(n):
    end_index = min(start_index + chunk_size, len(list1))
    chunk = list1[start_index:end_index]
    chunks.append(chunk)
    start_index = end_index
  return chunks

generate_img_payload = lambda embedding,url,status :  {'embedding':embedding,'url':url,'status':status}

@lru_cache
def download_image(image_url):
    ''' Function for single download of image'''
    if not validators.url(image_url):return
    buffer = tempfile.SpooledTemporaryFile(max_size=1e9)
    r = requests.get(image_url, stream=True)
    if r.status_code != 200:
        console.log(f'Download failed for {image_url}',style='red')
        return generate_img_payload(None,image_url,-1)
    if int(r.headers['Content-length'])==0:
        console.log(f'File size is 0 for {image_url}',style='red')
        return generate_img_payload(None,image_url,-2)
    if 'image' not in r.headers['Content-Type']:
        console.log(f'File is not an image {image_url}',style='red')
        return generate_img_payload(None,image_url,-3)
  
    filesize = int(r.headers['content-length'])
    for chunk in r.iter_content(chunk_size=1024*3):
        buffer.write(chunk)
    #console.log(f'Downloaded {image_url} {filesize/1024} KB')
    ''' Setting the buffer to start of the file in memory'''
    buffer.seek(0)
    ''' Converting from 4 channels to 3 and adding to img payload , embedding image here since we dont need the orginal image for the api response '''
    payload = generate_img_payload(get_image_embedding(Image.open(io.BytesIO(buffer.read())).convert("RGB")),image_url,1)
    console.log(f'Downloaded {image_url} {filesize/1024} KB')
    return payload


def compute_cosine_manager(image_url,source_image_embedding):
    ''' This method will download the image and also check the similarity since its fast to do it while multithreading'''
    comp_image = download_image(image_url)
    norm = -1 # for status less than -2
    if comp_image['status']==1:norm = get_cosine_similarity(source_image_embedding,comp_image['embedding'])
    comp_image['norm']=norm
    return comp_image


thread_download_scheduler = lambda image_urls,source_image_embedding : [compute_cosine_manager(i,source_image_embedding)  for i in image_urls]
def thread_manager(source_image,image_urls,nb_workers=4):
   
    results = []
    ''' if arguments are less than number of threads then we need to ensure only one thread is used and also split function has to give the right output'''
    if len(image_urls)<nb_workers:
        nb_workers=1 
    split_image_urls = split_list_into_n_lists(image_urls,nb_workers)
    nb_workers=len(split_image_urls) #if len is less than 4 , we need this count for number of thread
    with ThreadPoolExecutor(max_workers=nb_workers) as executor:
        ''' Passing embedding here since if we calculate cosine in thread ,its much faster'''
        futures = [executor.submit(thread_download_scheduler,i,source_image['embedding']) for i in split_image_urls]
        for i in futures:
            results = results + i.result()
    
    return results


def get_image_report(source_image_url,image_urls):
    ''' first image needs to be only downloaded only once'''
    start = time.time()
    source_image = download_image(source_image_url)
    console.log('Downloaded source image:',source_image_url)
    if source_image['status']<0:
        del source_image['embedding']
        return source_image
    df = pd.DataFrame(thread_manager(source_image,image_urls))
    incorrect_df = df[df['status']<0]
    df = df[df['status']>0]
    ''' Usually norm is 0 when image is duplicate or the same '''
    if sum(df['norm'])==0:df['score']=100
    else:
        #df['score'] = [ (1 - i/sum(df['norm']))*100 for i in df['norm'] ]
        #df['score'] = df['score'].round(2)
        df['score'] = df['norm']
        df = df.sort_values(by="score",ascending=False,kind="mergesort")
        df.reset_index(inplace=True)
        
    df = pd.concat([df, incorrect_df], ignore_index=True, sort=False)
    df = df.fillna(0)
    console.log(time.time()- start)
    console.log(df)
    return df[['url','score','status']].to_dict(orient='records')

# Base 64 image similarity service



def get_embedding_from_base64(base64_string):
    """Convert base64 string to image and get its embedding."""
    # Decode the base64 string into bytes
    image_data = base64.b64decode(base64_string)
    
    # Convert bytes to an image
    image = Image.open(io.BytesIO(image_data)).convert("RGB")
    
    # Get the embedding
    embedding = get_image_embedding(image)
    
    return embedding


def get_image_report_base64(source_image : str,target_images : list):
    """Generate image similarity report for base64 strings"""
    console.log('Base64 image report started')
    source_image_embedding = get_embedding_from_base64(source_image)
    target_image_embeddings = [get_embedding_from_base64(i) for i in target_images]
    total_images = len(target_images)
    url = [i for i in range(1,total_images+1)]
    score = [ get_cosine_similarity(source_image_embedding,i) for i in target_image_embeddings]
    status = [1] * total_images
    df = pd.DataFrame()
    df['url'],df['score'],df['status'] = url,score,status
    console.log(df)
    return df[['url','score','status']].to_dict(orient='records')

