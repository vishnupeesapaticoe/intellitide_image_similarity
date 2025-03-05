import torch
from torchvision import transforms
from torchvision.models import vit_b_16,ViT_B_16_Weights
from numpy.linalg import norm
import numpy as np


EFFIENCIENTNET_FLAG = False
get_norm = lambda x1,x2 : round(norm(x1-x2),5)
get_cosine_similarity = lambda x1, x2: max(0, np.dot(x1, x2) / (norm(x1) * norm(x2)))
mae_similarity = lambda x1,x2:  round(np.linalg.norm(x1- x2), 5)/round(np.linalg.norm(x1), 5)
mse_similarity = lambda x1,x2 : np.square(np.subtract(x1, x2)).mean()

''' Embedding section but with the latest VIt model '''
model = vit_b_16(weights = ViT_B_16_Weights.DEFAULT)
model.eval()

def get_image_embedding(img):
    tfms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    img = tfms(img).unsqueeze(0)
    with torch.no_grad():
        embedding = model(img).squeeze().cpu().numpy()
    return embedding
