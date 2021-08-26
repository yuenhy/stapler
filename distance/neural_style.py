import torch
from PIL import Image
from torchvision import transforms
import torch.nn.functional as F
import torch
from .vgg import VGG

from tqdm import tqdm

def gram_matrix(input):
    a, b, c, d = input.size()  # batch size, number of feature maps, dimensions of a f. map 

    features = input.view(a * b, c * d)  # resize F_XL into \hat F_XL

    G = torch.mm(features, features.t())  # compute the gram product

    # 'normalize' the values of the gram matrix
    # by dividing by the number of element in each feature maps.
    return G.div(a * b * c * d)

def gram_loss(x, y, N, M):
#   return torch.sum(torch.pow(x - y, 2)).div((np.power(N*M*2, 2, dtype=np.float64)))
  return F.mse_loss(x, y)

def content_loss(x, y):
  return F.mse_loss(x, y)

def image_loader(device, image_name):
    imsize = 512
    loader = transforms.Compose([
        transforms.Resize((imsize, imsize)),  # scale imported image
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
        ])  # transform it into a torch tensor

    image = Image.open(image_name)
    # fake batch dimension required to fit network's input dimensions
    image = loader(image).unsqueeze(0)
    return image.to(device, torch.float)

def score_by_style(original_imgs, generated_imgs):

    assert torch.cuda.is_available(), "cuda required"

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    vgg = VGG().to(device).eval()

    style_layers = ["block1_conv1", "block2_conv1", "block3_conv1", "block4_conv1", "block5_conv1"]

    distances = []

    for i in tqdm(range(len(generated_imgs))):
        generated_img = image_loader(device, generated_imgs[i])
        original_img = image_loader(device, original_imgs[i])    

        # get the style activations of the generated image
        generated_activations = vgg.get_style_activations(generated_img)
        # get the style activations of the real image"
        original_activations = vgg.get_style_activations(original_img)

        generated_gram = [gram_matrix(x.detach()) for x in generated_activations]
        original_gram = [gram_matrix(x.detach()) for x in original_activations]

        distance = 0
        for x, y in zip(generated_gram, original_gram):
            N, M = x.size()
            distance += (gram_loss(x, y, N, M)/ len(style_layers)).item()
        distances.append(distance)
    
    # sorting direction
    # ascending = True
        
    return distances

def score_by_content(original_imgs, generated_imgs):

    assert torch.cuda.is_available(), "cuda required"

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    vgg = VGG().to(device).eval()

    distances = []

    for i in tqdm(range(len(generated_imgs))):
        generated_img = image_loader(device, generated_imgs[i])
        original_img = image_loader(device, original_imgs[i])

        generated_activations = vgg.get_content_activations(generated_img)
        original_activations = vgg.get_content_activations(original_img)

        generated_gram = [x.detach() for x in generated_activations]
        original_gram = [x.detach() for x in original_activations]

        distance = 0
        for x, y in zip(original_gram, generated_gram):
            distance += content_loss(x, y).item()
        distances.append(distance)

    # sorting direction
    # ascending = True

    return distances