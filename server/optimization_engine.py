

class OptimizationEngine:
    """
    key point is the opportunity to execute the optimization mechanism.
    there are two parts: computation model, image size
        computation model is easy to realize, but the image size should be thought carefully.
        if the net condition becomes worse, server should send small size back to the client. however,
        what about some 500×500 image have already been handled?
    """
    def __init__(self):
        pass
