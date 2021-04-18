import cv2
import numpy as np
import logging
import pickle
from datetime import datetime
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import msgpack

prototext_file = '/models/face_detector.prototxt'
weights_file = '/models/face_detector.caffemodel'
mask_model = '/models/mask_detector.model'
facenet = cv2.dnn.readNet(prototext_file, weights_file)
masknet = load_model(mask_model)
confidence = 0.5


def main(ctx, msg):

    #load image from kps datasource
    unpacked_dict = msgpack.unpackb(msg, raw=False, max_bin_len=3145728)
    raw_image = np.fromstring(unpacked_dict["Data"], dtype=unpacked_dict["DataType"])
    raw_image = raw_image.reshape((unpacked_dict["Height"], unpacked_dict["Width"], unpacked_dict["Channels"]))
    image = cv2.cvtColor(raw_image, cv2.COLOR_RGB2BGR)
    logging.info('Received image, starting model detection')

    # prepare image for detection
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))
    facenet.setInput(blob)
    detections = facenet.forward()

    faces = []
    face_locations = []
    faces_without_mask = 0
    faces_with_mask = 0

    for i in range(0, detections.shape[2]):
        image_confidence = detections[0, 0, i, 2]

        if image_confidence > confidence:
            # compute the (x, y)-coordinates of the bounding box for the object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype('int')

            # ensure the bounding boxes fall within the dimensions of the frame
            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

            # extract the face ROI, convert it from BGR to RGB channel ordering, resize it to 224x224, and preprocess it
            face = image[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)

            # add the face and bounding boxes to their respective to result lists
            faces.append(face)
            face_locations.append((startX, startY, endX, endY))


    logging.info(f'Found [{len(faces)} faces in the image')
    # only make a predictions if at least one face was detected
    if len(faces) > 0:
        # for faster inference we'll make batch predictions on *all*
        # faces at the same time rather than one-by-one predictions
        # in the above `for` loop
        faces = np.array(faces, dtype="float32")
        mask_predictions = masknet.predict(faces, batch_size=32)

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

        cv2.putText(image, label, (startX, startY - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
        cv2.rectangle(image, (startX, startY), (endX, endY), color, 4)
    logging.info(f'detected ({faces_with_mask}) faces with mask and ({faces_without_mask}) without mask ')
    _, img_encoded = cv2.imencode('.jpg', image)
    payload = {
        'values': [
            {'id': 'image_timestamp', 'name': 'Timestamp', 'value': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'icon': 'fa-hourglass-half'},
            {'id': 'mask_count', 'name': 'Masks', 'value': faces_with_mask, 'icon': 'fa-check-circle'},
            {'id': 'nomask_count', 'name': 'No masks', 'value': faces_without_mask, 'icon': 'fa-times-circle'}],
        'image': img_encoded.tobytes()
    }

    ctx.send(pickle.dumps(payload))
    return

