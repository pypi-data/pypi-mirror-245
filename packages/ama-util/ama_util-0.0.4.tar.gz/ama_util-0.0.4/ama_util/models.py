import torch.nn as nn
import torch
import numpy as np
from torch.nn import functional as F
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from ama_util.utils import cal_gau
class Baseline(nn.Module):
    def __init__(self,numoffea=48):
        super().__init__()
        self.numoffea=numoffea #number of features
        self.sizeoffea=22*50 #size of feature
        self.numofneuron=test_loader[1].shape[1] #number of neurons
        #
        self.conv1 = nn.Conv2d(2,48,kernel_size=9,stride=1)#24,28*56
        stdv = 1. / np.sqrt(1*9*9)
        self.conv1.weight.data.uniform_(-stdv, stdv)
        self.conv1.bias.data.uniform_(-stdv, stdv)
        #
        self.conv2=nn.Conv2d(48,self.numoffea,kernel_size=7,stride=1)#48,22*50
        stdv = 1. / np.sqrt(48*7*7)
        self.conv2.weight.data.uniform_(-stdv, stdv)
        self.conv2.bias.data.uniform_(-stdv, stdv)
        #
        self.fc1 = nn.Linear(self.numoffea*self.sizeoffea, self.numofneuron)
        stdv = 1. / np.sqrt(self.numoffea*self.sizeoffea)
        self.fc1.weight.data.uniform_(-stdv, stdv)
        self.fc1.bias.data.uniform_(-stdv, stdv)
    def forward(self, x):
        # input x, (400, 2, 36, 64)
        
        encoded = F.relu(self.conv1(x))
        # (400, 48, 28, 56)
       
        encoded = F.relu(self.conv2(encoded))
        # (400, 48, 22, 50)
        
        encoded = encoded.view(-1,self.numoffea*self.sizeoffea)
        # (400, 52800)
        
        encoded = torch.exp(self.fc1(encoded)) # use exp instead of relu
        # (400, 161)
        return encoded
    
class two_DoG_learnZeros(nn.Module):
    def __init__(self,numoffea=48):
        super().__init__()
        self.numoffea=numoffea
        
        # the ones-tensor
        if self.training:
            self.ones = torch.ones(1,1,1,1).to('cuda')
        else:
            self.ones = torch.ones(1,1,1,1)
            
        # the gaussian kernel
        tmp_gau = torch.zeros((1,1,5,5));tmp_gau[0,0] = cal_gau(5,1.0,0)
        if self.training:
            self.gaussian_kernel_2d = tmp_gau.to('cuda')
        else:
            self.gaussian_kernel_2d = tmp_gau
            
        self.inhib_alpha1 = nn.Parameter(torch.zeros((self.numoffea,1)))
        self.inhib_alpha2 = nn.Parameter(torch.zeros((self.numoffea,1)))
        
        self.batchsize=400 # number of training sample per batch
        self.sizeoffea=22*50 # size of feature
        self.numofneuron= 161# test_loader[1].shape[1] # number of neurons
        
        self.conv1 = nn.Conv2d(2,48,kernel_size=9,stride=1)# 24,28*56
        stdv = 1. / np.sqrt(1*9*9)
        self.conv1.weight.data.uniform_(-stdv, stdv)
        self.conv1.bias.data.uniform_(-stdv, stdv)
        
        self.conv2=nn.Conv2d(48,self.numoffea,kernel_size=7,stride=1)# 48,22*50
        stdv = 1. / np.sqrt(48*7*7)
        self.conv2.weight.data.uniform_(-stdv, stdv)
        self.conv2.bias.data.uniform_(-stdv, stdv)
        
        self.fc1 = nn.Linear(self.numoffea*self.sizeoffea, self.numofneuron)
        stdv = 1. / np.sqrt(self.numoffea*self.sizeoffea)
        self.fc1.weight.data.uniform_(-stdv, stdv)
        self.fc1.bias.data.uniform_(-stdv, stdv)
        
    def forward(self, x): # input x, (400, 2, 36, 64)
        encoded = F.relu(self.conv1(x)) # (400, 48, 28, 56)
        
        ## add DOG1
        for f_m in range(self.numoffea): # 400，1，28 56， 1，1，5，5
            feature_channel = encoded[:,f_m,].reshape((x.shape[0],1,28,56))
            center = F.conv2d(feature_channel,self.ones)
            surround = F.conv2d(feature_channel,self.gaussian_kernel_2d,padding=2)
            encoded[:,f_m] = (center-self.inhib_alpha1[f_m]*surround).reshape((x.shape[0],28,56))
       
        encoded = F.relu(self.conv2(encoded)) # (400, 48, 22, 50)
        
        ## add DOG2
        for f_m in range(self.numoffea):
            feature_channel = encoded[:,f_m,].reshape((x.shape[0],1,22,50))
            center = F.conv2d(feature_channel,self.ones)
            surround = F.conv2d(feature_channel,self.gaussian_kernel_2d,padding=2)
            encoded[:,f_m] = (center-self.inhib_alpha2[f_m]*surround).reshape((x.shape[0],22,50))
        
        encoded = encoded.view(-1,self.numoffea*self.sizeoffea) # (400, 52800)
        
        encoded = torch.exp(self.fc1(encoded)) # (400, 161)
        return encoded
    
class one_DoG_fixOnes(nn.Module):
    def __init__(self,numoffea=48):
        super().__init__()
        self.numoffea=numoffea
        # the ones-tensor
        if self.training:
            self.ones = torch.ones(1,1,1,1).to('cuda')
        else:
            self.ones = torch.ones(1,1,1,1)
            
        # the gaussian kernel
        tmp_gau = torch.zeros((1,1,5,5));tmp_gau[0,0] = cal_gau(5,1.0,0)
        if self.training:
            self.gaussian_kernel_2d = tmp_gau.to('cuda')
        else:
            self.gaussian_kernel_2d = tmp_gau
        
        # inhib_alpha section
        self.inhib_alpha1 = nn.Parameter(torch.ones((self.numoffea,1)))
        # fix (or learnable)
        self.inhib_alpha1.requires_grad = False
        
        self.sizeoffea=22*50 # size of feature
        self.numofneuron= 161# test_loader[1].shape[1] # number of neurons
        
        self.conv1 = nn.Conv2d(2,48,kernel_size=9,stride=1)# 24,28*56
        stdv = 1. / np.sqrt(1*9*9)
        self.conv1.weight.data.uniform_(-stdv, stdv)
        self.conv1.bias.data.uniform_(-stdv, stdv)
        
        self.conv2=nn.Conv2d(48,self.numoffea,kernel_size=7,stride=1)# 48,22*50
        stdv = 1. / np.sqrt(48*7*7)
        self.conv2.weight.data.uniform_(-stdv, stdv)
        self.conv2.bias.data.uniform_(-stdv, stdv)
        
        self.fc1 = nn.Linear(self.numoffea*self.sizeoffea, self.numofneuron)
        stdv = 1. / np.sqrt(self.numoffea*self.sizeoffea)
        self.fc1.weight.data.uniform_(-stdv, stdv)
        self.fc1.bias.data.uniform_(-stdv, stdv)
        
    def forward(self, x): # input x, (400, 2, 36, 64)
        encoded = F.relu(self.conv1(x)) # (400, 48, 28, 56)
        
        ## add DOG1
        for f_m in range(self.numoffea): # 400，1，28 56， 1，1，5，5
            feature_channel = encoded[:,f_m,].reshape((x.shape[0],1,28,56))
            center = F.conv2d(feature_channel,self.ones)
            surround = F.conv2d(feature_channel,self.gaussian_kernel_2d,padding=2)
            encoded[:,f_m] = (center-self.inhib_alpha1[f_m]*surround).reshape((x.shape[0],28,56))
       
        encoded = F.relu(self.conv2(encoded)) # (400, 48, 22, 50)
        
        encoded = encoded.view(-1,self.numoffea*self.sizeoffea) # (400, 52800)
        
        encoded = torch.exp(self.fc1(encoded)) # (400, 161)
        return encoded
class one_fixOnes_DN(nn.Module):
    def __init__(self,numoffea=48):
        super().__init__()
        self.numoffea=numoffea
        # the ones-tensor
        if self.training:
            self.ones = torch.ones(1,1,1,1).to('cuda')
        else:
            self.ones = torch.ones(1,1,1,1)
        
        # the gaussian kernel
        tmp_gau = torch.zeros((1,1,5,5));tmp_gau[0,0] = cal_gau(5,1.0,0)
        if self.training:
            self.gaussian_kernel_2d = tmp_gau.to('cuda')
        else:
            self.gaussian_kernel_2d = tmp_gau
        
        self.inhib_alpha1 = nn.Parameter(torch.ones((self.numoffea,1)))
        self.inhib_alpha1.requires_grad = False
        
        self.sizeoffea=22*50 # size of feature
        self.numofneuron= 161# test_loader[1].shape[1] # number of neurons
        
        self.conv1 = nn.Conv2d(2,48,kernel_size=9,stride=1)# 24,28*56
        stdv = 1. / np.sqrt(1*9*9)
        self.conv1.weight.data.uniform_(-stdv, stdv)
        self.conv1.bias.data.uniform_(-stdv, stdv)
        
        self.conv2=nn.Conv2d(48,self.numoffea,kernel_size=7,stride=1)# 48,22*50
        stdv = 1. / np.sqrt(48*7*7)
        self.conv2.weight.data.uniform_(-stdv, stdv)
        self.conv2.bias.data.uniform_(-stdv, stdv)
        
        self.fc1 = nn.Linear(self.numoffea*self.sizeoffea, self.numofneuron)
        stdv = 1. / np.sqrt(self.numoffea*self.sizeoffea)
        self.fc1.weight.data.uniform_(-stdv, stdv)
        self.fc1.bias.data.uniform_(-stdv, stdv)
        
    def forward(self, x): # input x, (400, 2, 36, 64)
        encoded = F.relu(self.conv1(x)) # (400, 48, 28, 56)
        ## add DOG1
        for f_m in range(self.numoffea): # 400，1，28 56， 1，1，5，5
            feature_channel = encoded[:,f_m,].reshape((x.shape[0],1,28,56))
            center = F.conv2d(feature_channel,self.ones) # ;print(center.shape)
            surround = F.conv2d(feature_channel,self.gaussian_kernel_2d,padding=2) # ;print(surround.shape)
            encoded[:,f_m] = (center/self.inhib_alpha1[f_m]*surround).reshape((x.shape[0],28,56))
        encoded = F.relu(self.conv2(encoded)) # (400, 48, 22, 50)
        
        encoded = encoded.view(-1,self.numoffea*self.sizeoffea) # (400, 52800)
        
        encoded = torch.exp(self.fc1(encoded)) # (400, 161)
        return encoded
class ModelSE3d1_Neu150_ST_Exp(nn.Module):
    def __init__(self):
        super(ModelSE3d1_Neu150_ST_Exp,self).__init__()
        self.numoffea=16 #number of features
        self.sizeoffea=28*24 #36*32 # 28*24 #size of feature
        self.numofneuron=86 #number of neurons
        #
        #spatial kernel, self.kernel_size=9 #odd number
        self.conv1_ss=nn.Parameter(torch.zeros(self.numoffea,2,1,9,9))
        std=1. / np.sqrt(2*1*9*9)
        #self.conv1_ss.data.uniform_(-1e-4, 1e-4)
        self.conv1_ss.data.uniform_(-std*0.1, std*0.1) #(-std*0.001, std*0.001)
        self.conv1_ss_bias=nn.Parameter(torch.zeros(self.numoffea))
        self.conv1_ss_bias.data.uniform_(-std, std)
        #temporal kernel
        self.conv1_st=nn.Conv3d(self.numoffea,self.numoffea,kernel_size=(50,1,1),stride=1)
        #
        self.fc1=nn.Linear(self.numoffea*self.sizeoffea,self.numofneuron)
    #
    def forward(self, x):
        encoded = F.conv3d(x, self.conv1_ss, bias=self.conv1_ss_bias,stride=1,padding=(0,0,0))
        encoded = self.conv1_st(encoded)
        encoded = encoded.view(-1,self.numoffea*self.sizeoffea)
        encoded = torch.exp(self.fc1(encoded))
        return encoded
    
class one_fixHalf_DN(nn.Module):
    def __init__(self,numoffea=48):
        super().__init__()
        self.numoffea=numoffea
        # the ones-tensor
        if self.training:
            self.ones = torch.ones(1,1,1,1).to('cuda')
        else:
            self.ones = torch.ones(1,1,1,1)
        
        # the gaussian kernel
        tmp_gau = torch.zeros((1,1,5,5));tmp_gau[0,0] = cal_gau(5,1.0,0)
        if self.training:
            self.gaussian_kernel_2d = tmp_gau.to('cuda')
        else:
            self.gaussian_kernel_2d = tmp_gau
            
        # the 1e-6 till one fix alphas
        tmp = np.array([1.0 for i in range(48)])
        tmp[:24]=1e-6
        tmp = tmp.reshape(48,1)
        self.inhib_alpha1 = nn.Parameter(torch.Tensor(tmp));self.inhib_alpha1.requires_grad=False
        
        self.sizeoffea=22*50 # size of feature
        self.numofneuron= 161# test_loader[1].shape[1] # number of neurons
        
        self.conv1 = nn.Conv2d(2,48,kernel_size=9,stride=1)# 24,28*56
        stdv = 1. / np.sqrt(1*9*9)
        self.conv1.weight.data.uniform_(-stdv, stdv)
        self.conv1.bias.data.uniform_(-stdv, stdv)
        
        self.conv2=nn.Conv2d(48,self.numoffea,kernel_size=7,stride=1)# 48,22*50
        stdv = 1. / np.sqrt(48*7*7)
        self.conv2.weight.data.uniform_(-stdv, stdv)
        self.conv2.bias.data.uniform_(-stdv, stdv)
        
        self.fc1 = nn.Linear(self.numoffea*self.sizeoffea, self.numofneuron)
        stdv = 1. / np.sqrt(self.numoffea*self.sizeoffea)
        self.fc1.weight.data.uniform_(-stdv, stdv)
        self.fc1.bias.data.uniform_(-stdv, stdv)
        
    def forward(self, x): # input x, (400, 2, 36, 64)
        encoded = F.relu(self.conv1(x)) # (400, 48, 28, 56)
        ## add DOG1
        for f_m in range(self.numoffea): # 400，1，28 56， 1，1，5，5
            feature_channel = encoded[:,f_m,].reshape((x.shape[0],1,28,56))
            center = F.conv2d(feature_channel,self.ones) # ;print(center.shape)
            surround = F.conv2d(feature_channel,self.gaussian_kernel_2d,padding=2) # ;print(surround.shape)
            encoded[:,f_m] = (center/self.inhib_alpha1[f_m]*surround).reshape((x.shape[0],28,56))
        encoded = F.relu(self.conv2(encoded)) # (400, 48, 22, 50)
        
        encoded = encoded.view(-1,self.numoffea*self.sizeoffea) # (400, 52800)
        
        encoded = torch.exp(self.fc1(encoded)) # (400, 161)
        return encoded
class AC_1(nn.Module):
    def __init__(self):
        super(AC_1,self).__init__()
        self.numoffea=16 # number of feature_channels
        self.sizeoffea=28*24 # (36-9+1)*(32-9+1) ->28*24 #size of feature
        self.numofneuron=86 # number of neurons
        self.ones = torch.ones(1,1,1,1).to('cuda')
        self.conv1_ss=nn.Parameter(torch.zeros(self.numoffea,2,1,9,9))
        std=1. / np.sqrt(2*1*9*9)
        self.conv1_ss.data.uniform_(-std*0.1, std*0.1) #(-std*0.001, std*0.001)
        self.conv1_ss_bias=nn.Parameter(torch.zeros(self.numoffea))
        self.conv1_ss_bias.data.uniform_(-std, std)
        
        # represent the strength of lateral inhibition
        self.inhib_alpha = nn.Parameter(torch.zeros((16,1)))
        
        # the gaussian kernel
        tmp_gau = torch.zeros((1,1,5,5));tmp_gau[0,0] = cal_gau(5,1.0,0)
        self.gaussian_kernel_2d = tmp_gau.to('cuda')
        
        self.conv1_st=nn.Conv3d(self.numoffea,self.numoffea,kernel_size=(50,1,1),stride=1)
        self.fc1=nn.Linear(self.numoffea*self.sizeoffea,self.numofneuron)
        
    def forward(self, x):
        # input: 200, 16, 50, 28, 24
        encoded = F.conv3d(x, self.conv1_ss, bias=self.conv1_ss_bias,stride=1,padding=(0,0,0))
        encoded = self.conv1_st(encoded)
        for f_m in range(self.numoffea):
            feature_channel = encoded[:, f_m, :, :, :]
            
            center = F.conv2d(feature_channel,self.ones)
            surround = F.conv2d(feature_channel,self.gaussian_kernel_2d,padding=2)
            
            encoded[:,f_m] = center-self.inhib_alpha[f_m]*surround 
        encoded = encoded.view(-1,self.numoffea*self.sizeoffea)
        encoded = torch.exp(self.fc1(encoded))
        return encoded