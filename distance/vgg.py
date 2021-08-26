import torch.nn as nn
import torch.nn as nn
import torchvision.models as models


class VGG(nn.Module):
    def __init__(self):
        super(VGG, self).__init__()
        
        self.vgg = models.vgg19(pretrained=True).features
    
    def get_style_activations(self, x):
        # block1_conv1, block2_conv1, block3_conv1, block4_conv1, block5_conv1

        features = [self.vgg[:4](x)] + [self.vgg[:7](x)] + [self.vgg[:12](x)] + [self.vgg[:21](x)] + [self.vgg[:30](x)] 
        return features

    def get_content_activations(self, x):
      # block4_conv2
      features = self.vgg[:23](x)
      return features

    
    def forward(self, x):
        return self.vgg(x)
