# encoding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import os.path as osp
import sys
import time
import math
import numpy as np
from easydict import EasyDict as edict
import argparse

C = edict()
config = C
cfg = C

C.seed = 12345

remoteip = os.popen('pwd').read()
if os.getenv('volna') is not None:
    C.volna = os.environ['volna']
else:
    C.volna = '/home/cxk/msra_container/' # the path to the data dir.

"""please config ROOT_dir and user when u first using"""
C.repo_name = 'TorchSemiSeg'
C.abs_dir = osp.realpath(".")
C.this_dir = C.abs_dir.split(osp.sep)[-1]

C.root_dir = C.abs_dir[:C.abs_dir.index(C.repo_name) + len(C.repo_name)]
C.log_dir = osp.abspath('log')
C.tb_dir = osp.abspath(osp.join(C.log_dir, "tb"))

C.log_dir_link = osp.join(C.abs_dir, 'log')

# snapshot dir that stores checkpoints
if os.getenv('snapshot_dir'):
    C.snapshot_dir = osp.join(os.environ['snapshot_dir'], "snapshot")
else:
    C.snapshot_dir = osp.abspath(osp.join(C.log_dir, "snapshot"))

exp_time = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime())
C.log_file = C.log_dir + '/log_' + exp_time + '.log'
C.link_log_file = C.log_file + '/log_last.log'
C.val_log_file = C.log_dir + '/val_' + exp_time + '.log'
C.link_val_log_file = C.log_dir + '/val_last.log'

""" Data Dir and Weight Dir """
C.dataset_path = osp.join(C.volna, 'data/final_data/train')
C.img_root_folder = osp.join(C.dataset_path,'labeled_images')
C.gt_root_folder = osp.join(C.dataset_path,'labels')
C.pretrained_model = C.volna + 'pytorch-weight/resnet50_v1c.pth'

""" Path Config """
def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)
add_path(osp.join(C.root_dir, 'furnace'))

''' Experiments Setting '''
C.labeled_ratio = 8     # ratio of labeled set
C.train_source = osp.join(C.dataset_path, "labeled_images.txt")
C.unsup_source = osp.join(C.dataset_path, "unlabeled_images.txt")
C.eval_source = osp.join(C.dataset_path, "vallabeled_images.txt")
C.is_test = False
C.fix_bias = True
C.bn_eps = 1e-5
C.bn_momentum = 0.1

C.unsup_weight = 0
C.cps_weight = 1.5

''' Image Config '''
C.num_classes = 21
C.background = 0
C.image_mean = np.array([0.485, 0.456, 0.406])  # 0.485, 0.456, 0.406
C.image_std = np.array([0.229, 0.224, 0.225])
C.image_height = 512
C.image_width = 512
C.num_train_imgs = 108
C.num_eval_imgs = 27
C.num_unsup_imgs = 1565    # unsupervised samples

"""Train Config"""
if os.getenv('learning_rate'):
    C.lr = float(os.environ['learning_rate'])
else:
    C.lr = 0.005

if os.getenv('batch_size'):
    C.batch_size = int(os.environ['batch_size'])
else:
    C.batch_size = 16

C.lr_power = 0.9
C.momentum = 0.9
C.weight_decay = 1e-4

C.nepochs = 34
C.max_samples = max(C.num_train_imgs, C.num_unsup_imgs)     # Define the iterations in an epoch
C.cold_start = 0
C.niters_per_epoch = int(math.ceil(C.max_samples * 1.0 // C.batch_size))
C.num_workers = 8
C.train_scale_array = [0.5, 0.75, 1, 1.5, 1.75, 2.0]
C.warm_up_epoch = 0

''' Eval Config '''
C.eval_iter = 30
C.eval_stride_rate = 2 / 3
C.eval_scale_array = [1] #[1, 0.75, 1.25]
C.eval_flip = False
C.eval_base_size = 512
C.eval_crop_size = 512

"""Display Config"""
if os.getenv('snapshot_iter'):
    C.snapshot_iter = int(os.environ['snapshot_iter'])
else:
    C.snapshot_iter = 2

C.record_info_iter = 20
C.display_iter = 50