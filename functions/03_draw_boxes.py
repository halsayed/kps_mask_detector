import cv2
import json
import logging
import pickle
from datetime import datetime


def main(ctx, msg):
    payload = pickle.loads(msg)
    faces = payload['faces']
    face_locations = payload['face_locations']
    mask_predictions = payload['mask_predictions']
    image = payload['image']
    faces_without_mask = 0
    faces_with_mask = 0

    if len(faces):
        logging.info('drawing boxes on the image')
    else:
        logging.info('no faces on the image')

    # draw boxes around the faces
    for (box, pred) in zip(face_locations, mask_predictions):
        (startX, startY, endX, endY) = box
        (mask, withoutMask) = pred

        # determine the class label and color we'll use to draw
        # the bounding box and text
        if mask > withoutMask:
            label = f'Mask: {mask:.2f}'
            faces_with_mask += 1
            color = (0, 255, 0)
        else:
            label = f'No Mask: {withoutMask:.2f}'
            faces_without_mask += 1
            color = (0, 0, 255)

        cv2.putText(image, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
        cv2.rectangle(image, (startX, startY), (endX, endY), color, 4)

    _, img_encoded = cv2.imencode('.jpg', image)

    data = [
        {'id': 'image_timestamp', 'name': 'Timestamp', 'value': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
         'icon': 'fa-hourglass-half'},
        {'id': 'mask_count', 'name': 'Masks', 'value': faces_with_mask, 'icon': 'fa-check-circle'},
        {'id': 'nomask_count', 'name': 'No masks', 'value': faces_without_mask, 'icon': 'fa-times-circle'},
    ]
    display_payload = {
        'values': json.dumps(data),
        'image': img_encoded.tobytes()
    }
    ctx.send(pickle.dumps(display_payload))
    return
