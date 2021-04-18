import numpy as np
import logging
import pickle


def main(ctx, msg):
    payload = pickle.loads(msg)
    logging.info('mask detection no active, assuming all without mask')
    payload['mask_predictions'] = np.array([[0, 1]])
    ctx.send(pickle.dumps(payload))
    return
