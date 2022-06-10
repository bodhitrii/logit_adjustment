## Long-tail learning via logit adjustment

Aditya Krishna Menon, Sadeep Jayasumana, Ankit Singh Rawat, Himanshu Jain, Andreas Veit, Sanjiv Kumar. 

------

This is the unofficial implementation of DAR-BN in the paper [Long-tail learning via logit adjustment](https://arxiv.org/abs/2007.07314)(ICLR 2021) in pytorch.

### Dependency

The code is built with following libraries:

- PyTorch 1.2
- TensorboardX
- scikit-learn


### Dataset

- Imbalanced CIFAR. The original data will be downloaded and converted by imbalancec_cifar.py.


### Training 

We provide several training examples with this repo:
- To train the ERM baseline on long-tailed imbalance with ratio of 100

```javascript
python cifar_train.py --gpu 0 --imb_type exp --imb_factor 0.01 --loss_type CE --train_rule None
```

- To train the ERM Loss along with DAR-BN on long-tailed imbalance with ratio of 100
```javascript
python cifar_train.py --gpu 0 --imb_type exp --imb_factor 0.01 --loss_type CE --train_rule DAR-BN
```

### Results
 | |Baseline (ERM) | Logit adjustment loss |
 | :---:  | :---: |:---: |
 |CIFAR-10 LT | 2 | 80.74 |
 |CIFAR-100 LT| 3 | 44.41 |
