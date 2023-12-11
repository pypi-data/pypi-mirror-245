import numpy as np
import torch
import datetime
import torch.nn as nn
from torch.nn import functional as F
from scipy.stats import pearsonr
def Ploss_L2L1_SE_ST(recon_x, x, alpha1, alpha2, beta, alpha_x1, alpha_x2, beta_y):
    tempB, tempN =x.size()
    Ploss = F.poisson_nll_loss(recon_x, x,log_input=False, reduction='sum')
    
    l2temp=0.0
    for temp in alpha_x1:
        l2temp = l2temp+ temp.norm(2)
    
    l2temp2=0.0
    for temp in alpha_x2:
        l2temp2 = l2temp2+ temp.weight.norm(2)
    
    L2loss=alpha1*l2temp+alpha2*l2temp2
    
    
    l1temp=0.0
    for temp in beta_y:
        l1temp = l1temp+ temp.weight.norm(1)
    L1loss=beta*l1temp
    
    return Ploss+L2loss+L1loss

def Ploss_L2L1_SE_regularizaion_2conv(recon_x, x, alpha1, alpha2, beta, alpha_x1, alpha_x2, beta_y):
    tempB, tempN = x.size()
    Ploss = F.poisson_nll_loss(recon_x, x, log_input=False, reduction="sum")
    l2temp1 = 0.0
    l2temp2 = 0.0
    
    for temp in alpha_x1:
        l2temp1 = l2temp1 + temp.weight.norm(2)
    for temp in alpha_x2:
        l2temp2 = l2temp2 + temp.weight.norm(2)
    L2loss = alpha1 * l2temp1 + alpha2 * l2temp2
    l1temp = 0.0
    for temp in beta_y:
        l1temp = l1temp + temp.weight.norm(1)
    L1loss = beta * l1temp
    return Ploss + L2loss + L1loss

def model_train(model,
                data,
                optimizer,
                device,
                EPOCH,
                loss_func,
                valdata,
                alpha1=None,
                beta=None,
                alpha2=None,
                earlystop=False,
                valdevice=None,
                verbose=True):
    print(datetime.datetime.now())
    loss=0.0
    trainlosses=np.zeros((EPOCH))
    vallosses  =np.zeros((EPOCH)) # save validation losses of all epochs until early stopping
    for epoch in range(EPOCH):
        model=model.to(device)
        model=model.train()
        for step, (x,y) in enumerate(data):
            x=torch.from_numpy(x).float()
            y=torch.from_numpy(y).float()
            b_x = x.to(device) 
            b_y = y.to(device)

            encoded = model(b_x)
            if hasattr(model, "conv1_st"):
                ## for spatial_temporal_model (PLOS based)
                loss=loss_func(encoded, b_y,alpha1,alpha2,beta,[model.conv1_ss],[model.conv1_st],[model.fc1])
            elif hasattr(model,"conv2"):
                ## for two_layers_CNN_model
                loss = loss_func(encoded, b_y, alpha1, alpha2, beta, [model.conv1], [model.conv2], [model.fc1])
            else:
                print('sth is wrong, DEBUG')
                break
            
            # last epoch to get the training loss, keep the same sample size as validation
            trainlosses[epoch]=trainlosses[epoch]+loss.detach().clone().cpu().data.numpy()
            #
            optimizer.zero_grad()               # clear gradients for this training step
            loss.backward()                     # backpropagation, compute gradients
            optimizer.step()                    # apply gradients
            #
            if step % 100 == 0 and verbose==True:
                print('Model: ',model.__class__.__name__,'|Epoch: ', epoch,\
                      '| train loss: %.4f' % loss.cpu().data.numpy())
        # validation
        if hasattr(model,"conv1_st"):
            vallosses[epoch]=np.mean(model_val(model,valdata,valdevice))
        elif hasattr(model,"conv2"):
            vallosses[epoch]=np.mean(model_val_v1(model,valdata,valdevice))
        else:
            print('sth is wrong DEBUG model_utils.py')
        trainlosses[epoch] =trainlosses[epoch]/len(data)
        
        if epoch>10 and earlystop==True: # epoch>20, early stopping check after each epoch, use CC as a metric
            if epoch-np.argmax(vallosses)>4: # >4
                break
    print ('Epoch: {:} val loss: {:.4f}, finish training!'.format(epoch,vallosses[epoch]))
    print(datetime.datetime.now())
    return trainlosses,vallosses

# def model_val(model,data,device):

#     model=model.to(device)
#     model=model.eval()
    
#     if hasattr(model, "ones"):
#         model.ones = model.ones.to(device)
#     if hasattr(model,'gaussian_kernel_2d'):
#         model.gaussian_kernel_2d = model.gaussian_kernel_2d.to(device)
        
#     (x,y)=data
#     x=torch.from_numpy(x).float()
#     b_x = x.to(device) 
#     with torch.no_grad():
#         encoded = model(b_x)
#     # CC as metric
#     encoded_np=encoded.cpu().data.numpy()

#     numCell = y.shape[-1]
#     valccs,valps = np.zeros(numCell),np.zeros(numCell)
#     # print(encoded_np.shape,y.shape,x.shape[2]-1)
#     for cell in range(numCell):
#         valccs[cell],valps[cell] = pearsonr(encoded_np[x.shape[2]-1:,cell],y[x.shape[2]-1:,cell])
#     return valccs


# def model_test(model,data,device):
#     model=model.eval()
#     model=model.to(device)
#     if hasattr(model, "ones"):
#         model.ones = model.ones.to(device)
#     if hasattr(model,'gaussian_kernel_2d'):
#         model.gaussian_kernel_2d = model.gaussian_kernel_2d.to(device)
#     (x,y)=data
#     x=torch.from_numpy(x).float()
#     b_x = x.to(device) 
#     encoded = model(b_x)
#     encoded_np=encoded.cpu().data.numpy()
#     ##TODO 
#     # use len(encoded_np) con
#     numCell = len(encoded_np) # y.shape[-1]
#     testccs,testps = np.zeros(numCell),np.zeros(numCell)
#     for cell in range(numCell):
#         testccs[cell],testps[cell] = pearsonr(encoded_np[x.shape[2]-1:,cell],y[x.shape[2]-1:,cell])
#     return testccs,testps

def model_val_v1(model,data,device):

    model=model.to(device)
    model=model.eval()
    
    if hasattr(model, "ones"):
        model.ones = model.ones.to(device)
    if hasattr(model,'gaussian_kernel_2d'):
        model.gaussian_kernel_2d = model.gaussian_kernel_2d.to(device)
        
    (x,y)=data
    x=torch.from_numpy(x).float()
    b_x = x.to(device) 
    with torch.no_grad():
        encoded = model(b_x)
    # CC as metric
    encoded_np=encoded.cpu().data.numpy()

    numInput = len(encoded_np)
    numCell = encoded_np.shape[-1]
    
    print('#val input: {}, #cell: {}'.format(numInput,numCell))
    valccs,valps = np.zeros(numCell),np.zeros(numCell)
    for cell in range(numCell):
        # print(encoded_np[:,cell],y[:,cell])
        # print(pearsonr(encoded_np[:,cell],y[:,cell]))
        valccs[cell],valps[cell] = pearsonr(encoded_np[:,cell],y[:,cell])
    return valccs

def model_test_v1(model,data,device):
    model=model.eval()
    model=model.to(device)
    if hasattr(model, "ones"):
        model.ones = model.ones.to(device)
    if hasattr(model,'gaussian_kernel_2d'):
        model.gaussian_kernel_2d = model.gaussian_kernel_2d.to(device)
    (x,y)=data
    x=torch.from_numpy(x).float()
    b_x = x.to(device) 
    encoded = model(b_x)
    encoded_np=encoded.cpu().data.numpy()
    
    numInput = len(encoded_np)
    numCell = encoded_np.shape[-1]
    print('#test input: {}, #cell: {}'.format(numInput,numCell))
    
    testccs,testps = np.zeros(numCell),np.zeros(numCell)
    for cell in range(numCell):
        testccs[cell],testps[cell] = pearsonr(encoded_np[:,cell],y[:,cell])
    return testccs,testps