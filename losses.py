import math
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import sys


def focal_loss(input_values, gamma):
    """Computes the focal loss"""
    p = torch.exp(-input_values)
    loss = (1 - p) ** gamma * input_values
    return loss.mean()

class FocalLoss(nn.Module):
    def __init__(self, weight=None, gamma=0.):
        super(FocalLoss, self).__init__()
        assert gamma >= 0
        self.gamma = gamma
        self.weight = weight

    def forward(self, input, target):
        return focal_loss(F.cross_entropy(input, target, reduction='none', weight=self.weight), self.gamma)

class LDAMLoss(nn.Module):
    
    def __init__(self, cls_num_list, max_m=0.5, weight=None, s=30):
        super(LDAMLoss, self).__init__()
        m_list = 1.0 / np.sqrt(np.sqrt(cls_num_list))
        m_list = m_list * (max_m / np.max(m_list))
        m_list = torch.cuda.FloatTensor(m_list)
        self.m_list = m_list
        assert s > 0
        self.s = s
        self.weight = weight

    def forward(self, x, target):
        index = torch.zeros_like(x, dtype=torch.uint8)
        index.scatter_(1, target.data.view(-1, 1), 1)
        
        index_float = index.type(torch.cuda.FloatTensor)
        batch_m = torch.matmul(self.m_list[None, :], index_float.transpose(0,1))
        batch_m = batch_m.view((-1, 1))
        x_m = x - batch_m
    
        output = torch.where(index, x_m, x)
        return F.cross_entropy(self.s*output, target, weight=self.weight)

class LALoss(nn.Module):
    
    def __init__(self, cls_num_list, tau = 1.0):
        super(LALoss, self).__init__()
        base_probs = cls_num_list/cls_num_list.sum()
        scaled_class_weights = tau * torch.log(base_probs + 1e-12)
        scaled_class_weights = scaled_class_weights.reshape(1,-1) #[1,classnum]
        self.tau = tau
        self.scaled_class_weights = scaled_class_weights.float().cuda()
        self.prob = base_probs

        
    def forward(self, x, target):
        x += self.scaled_class_weights

        return F.cross_entropy(x, target)

    
    
    
