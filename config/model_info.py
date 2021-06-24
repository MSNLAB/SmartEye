model_lib = {
    'fasterrcnn_mobilenet_v3_large_320_fpn': {
        'model_path': 'fasterrcnn_mobilenet_v3_large_320_fpn-907ea3f9.pth',
        'tx2_delay':   0.18,
        'cloud_delay': 0.024,
        'precision':   None,
        'service_type': 'object_detection'},
    'fasterrcnn_mobilenet_v3_large_fpn': {
        'model_path': 'fasterrcnn_mobilenet_v3_large_fpn-fb6a3cc7.pth',
        'tx2_delay':  0.39,
        'cloud_delay': 0.026,
        'precision':  None,
        'service_type': 'object_detection'},
    'fasterrcnn_resnet50_fpn': {
        'model_path': 'fasterrcnn_resnet50_fpn_coco-258fb6c6.pth',
        'tx2_delay':  1.57,
        'cloud_delay': 0.058,
        'precision':  None,
        'service_type': 'object_detection'},
    'maskrcnn_resnet50_fpn': {
        'model_path': 'maskrcnn_resnet50_fpn_coco-bf2d0c1e.pth',
        'tx2_delay':   1.65,
        'cloud_delay': 0.064,
        'precision':   None,
        'service_type': 'object_detection'},
    'retinanet_resnet50_fpn': {
        'model_path': 'retinanet_resnet50_fpn_coco-eeacb38b.pth',
        'tx2_delay':  1.77,
        'cloud_delay':  0.063,
        'precision':  None,
        'service_type': 'object_detection'},
}

edge_object_detection_model = ('fasterrcnn_mobilenet_v3_large_320_fpn',
                               'fasterrcnn_mobilenet_v3_large_fpn',
                               'fasterrcnn_resnet50_fpn')

cloud_object_detection_model = ('fasterrcnn_mobilenet_v3_large_320_fpn',
                                'fasterrcnn_mobilenet_v3_large_fpn',
                                'fasterrcnn_resnet50_fpn',
                                'maskrcnn_resnet50_fpn',
                                'retinanet_resnet50_fpn',
                                #'ssd300_vgg16',
                                #'ssdlite320_mobilenet_v3_large'
                               )


