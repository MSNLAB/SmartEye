import os
import pickle
import numpy as np
from mean_average_precision import MetricBuilder
from sklearn.preprocessing import normalize


def gt_data(gt_file):
    with open(gt_file, 'rb') as handle:
        boxes = pickle.load(handle)["boxes"]
                        
    for i in range(len(boxes)):
                                        
        boxes[i] = list(boxes[i][0] + boxes[i][1])
    boxes = np.array(boxes)
    add = np.zeros((boxes.shape[0], 3))
    gt = np.hstack((boxes, add))
    gt = normalize(gt,axis=0,norm='max')
    
    return gt

def pred_data(pred_file):

    with open(pred_file, 'rb') as handle:
        info = pickle.load(handle)
    boxes = info["boxes"]
    score = info["score"]

    for i in range(len(boxes)):
        boxes[i] = list(boxes[i][0] + boxes[i][1]) 
    boxes = np.array(boxes)
                
    score = np.array(score)
    
    score = score.reshape(score.shape[0], 1)
    
    add = np.zeros((boxes.shape[0], 1))
    boxes_add = np.hstack((boxes, add))
    pred = np.hstack((boxes_add, score))                                                                                    
    pred=normalize(pred, axis=0, norm='max')                                                                                
    return pred

def get_map(gt, pred):
                                                                                                                            
    metric_fn = MetricBuilder.build_evaluation_metric("map_2d", async_mode=True, num_classes=1)
                                                                                                                            
    for i in range(10):
        metric_fn.add(pred, gt)

    print(f"COCO mAP: {metric_fn.value(iou_thresholds=np.arange(0.5, 1.0, 0.05), recall_thresholds=np.arange(0., 1.01, 0.01), mpolicy='soft')['mAP']}")
    return {metric_fn.value(iou_thresholds=np.arange(0.5, 1.0, 0.05), recall_thresholds=np.arange(0., 1.01, 0.01), mpolicy='soft')['mAP']}


gt_folder = "1080p"

pred_folder = "240p"
maps = []
for gt_file in os.listdir(gt_folder):
    #print(os.path.join(gt_folder, gt_file))
    gt = gt_data(os.path.join(gt_folder, gt_file))
    #print(os.path.join(pred_folder, gt_file))
    pred = pred_data(os.path.join(pred_folder, gt_file))
    
    mapp =  list(get_map(gt, pred)) 
    maps.append(mapp[0])


print("average COCO mAP:" + str(sum(maps)/ len(maps)))



