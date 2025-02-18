from efficientnet_pytorch import EfficientNet
from torchvision import transforms
from numpy.linalg import norm
import numpy as np

get_norm = lambda x1,x2 : round(norm(x1-x2),5)
mae_similarity = lambda x1,x2:  round(np.linalg.norm(x1- x2), 5)/round(np.linalg.norm(x1), 5)
mse_similarity = lambda x1,x2 : np.square(np.subtract(x1, x2)).mean()

''' Embedding section '''
model = EfficientNet.from_pretrained('efficientnet-b0')
model.eval()
def get_image_embedding(img):
    tfms = transforms.Compose([transforms.Resize(224), transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),])
    img = tfms(img).unsqueeze(0)
    return model.extract_features(img).detach().numpy()
