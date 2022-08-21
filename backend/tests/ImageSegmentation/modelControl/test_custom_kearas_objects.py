#imports from other directory
import sys, os 
sys.path.append(os.path.abspath(os.path.join('..', 'backend')))
from ImageSegmentation.modelControl import customKearasObjects

def test_get_custom_objects_returns_dict():
    obj = customKearasObjects.getCustomObjects()
    assert type(obj) == dict

def test_calculate_max_dice_loss_correct():
    y = [[[[1],[1]],[[1],[1]]]]
    loss = customKearasObjects.diceLoss(y,y)
    assert loss == 0

def test_calculate_max_mean_IoU_correct():
    y = [[[[1],[1]],[[1],[1]]]]
    iou = customKearasObjects.meanIoU(y,y)
    assert iou == 1

def test_calculate_min_mean_IoU_correct():
    y = [[[[1],[1]],[[1],[1]]]]
    yT = [[[[0],[0]],[[0],[0]]]]
    iou = customKearasObjects.meanIoU(y,yT)
    assert iou == 0