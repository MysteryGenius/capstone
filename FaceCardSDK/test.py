from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys, hashlib, calendar, base64, os, shutil, io, argparse, time
import math, sys, queue, threading, platform, subprocess, requests
import numpy as np
from cv2 import cv2 as cv
import re, sklearn, configparser
from datetime import datetime
from threading import Timer, Thread, Event
from skimage import io
import tensorflow as tf
import tensorboard as tb
import face_recognition
import json
from utils import face_preprocess
from nets.mtcnn_model import P_Net, R_Net, O_Net
from Detection.MtcnnDetector import MtcnnDetector
from Detection.detector import Detector
from Detection.fcn_detector import FcnDetector

tf.compat.v1.disable_v2_behavior()
tf.gfile = tb.compat.tensorflow_stub.io.gfile

global currentYear, currentMonth
currentYear = datetime.now().year
currentMonth = datetime.now().month
currentDay = datetime.now().day
OperatorOrganization = ""

conf = configparser.ConfigParser()
conf.read("FaceCardSDK/config/main.cfg")
MODEL_PATH = conf.get("MOBILEFACENET", "MODEL_PATH")
VERIFICATION_THRESHOLD = float(conf.get("MOBILEFACENET", "VERIFICATION_THRESHOLD"))

def get_test_image(mtcnn_detector):
    capture = cv.VideoCapture(0)
    print(capture.isOpened())
    width = 480
    height = 480
    capture.set(cv.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, height)
    while capture.isOpened():
        ret, frame = capture.read()
        with tf.compat.v1.Session() as sess:
            sess.run(tf.compat.v1.global_variables_initializer())

            faces, landmarks = mtcnn_detector.detect(frame)
            cv.imshow("frame", frame)
            if faces.shape[0] is not 0:
                input_images = np.zeros((faces.shape[0], 112,112,3))
                for i, face in enumerate(faces):
                    if round(faces[i, 4], 6) > 0:
                        # print("Rounding Faces: ", faces)
                        bbox = faces[i,0:4]
                        points = landmarks[i,:].reshape((5,2))
                        return frame

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        elif not ret:
            print("error")
            break
    capture.release()
    cv.destroyAllWindows()

    return

def load_mtcnn(conf):
    # load mtcnn model
    MODEL_PATH = conf.get("MTCNN", "MODEL_PATH")
    MIN_FACE_SIZE = int(conf.get("MTCNN", "MIN_FACE_SIZE"))
    STEPS_THRESHOLD = [float(i) for i in conf.get("MTCNN", "STEPS_THRESHOLD").split(",")]

    detectors = [None, None, None]
    prefix = [MODEL_PATH + "/PNet_landmark/PNet", MODEL_PATH + "/RNet_landmark/RNet", MODEL_PATH + "/ONet_landmark/ONet"]
    epoch = [18, 14, 16]
    model_path = ['%s-%s' % (x, y) for x, y in zip(prefix, epoch)]
    PNet = FcnDetector(P_Net, model_path[0])
    detectors[0] = PNet
    RNet = Detector(R_Net, 24, 1, model_path[1])
    detectors[1] = RNet
    ONet = Detector(O_Net, 48, 1, model_path[2])
    detectors[2] = ONet
    mtcnn_detector = MtcnnDetector(detectors=detectors, min_face_size=MIN_FACE_SIZE, threshold=STEPS_THRESHOLD)

    return mtcnn_detector

mtcnn_detector = load_mtcnn(conf)

def get_model_filenames(model_dir):
    files = os.listdir(model_dir)
    meta_files = [s for s in files if s.endswith('.meta')]
    if len(meta_files) == 0:
        raise ValueError('No meta file found in the model directory (%s)' % model_dir)
    elif len(meta_files) > 1:
        raise ValueError('There should not be more than one meta file in the model directory (%s)' % model_dir)
    meta_file = meta_files[0]
    ckpt = tf.train.get_checkpoint_state(model_dir)
    if ckpt and ckpt.model_checkpoint_path:
        ckpt_file = os.path.basename(ckpt.model_checkpoint_path)
        return meta_file, ckpt_file

    meta_files = [s for s in files if '.ckpt' in s]
    max_step = -1
    for f in files:
        step_str = re.match(r'(^model-[\w\- ]+.ckpt-(\d+))', f)
        if step_str is not None and len(step_str.groups()) >= 2:
            step = int(step_str.groups()[1])
            if step > max_step:
                max_step = step
                ckpt_file = step_str.groups()[0]
    return meta_file, ckpt_file

def load_facecardmodel(model):
    # Check if the model is a model directory (containing a metagraph and a checkpoint file)
    #  or if it is a protobuf file with a frozen graph
    model_exp = os.path.expanduser(model)
    if (os.path.isfile(model_exp)):
        # print('Model filename: %s' % model_exp)
        with tb.compat.tensorflow_stub.io.gfile.GFile(model_exp, 'rb') as f:
            graph_def = tf.compat.v1.GraphDef()
            graph_def.ParseFromString(f.read())
            tf.import_graph_def(graph_def, name='')
    else:
        # print('Model directory: %s' % model_exp)
        meta_file, ckpt_file = get_model_filenames(model_exp)

        # print('Metagraph file: %s' % meta_file)
        # print('Checkpoint file: %s' % ckpt_file)

        saver = tf.compat.v1.train.import_meta_graph(os.path.join(model_exp, meta_file))
        saver.restore(tf.compat.v1.get_default_session(), os.path.join(model_exp, ckpt_file))

def return_embeddings(image, mtcnn_detector):
    with tf.compat.v1.Graph().as_default():
        with tf.compat.v1.Session() as sess:
            load_facecardmodel("./FaceCardSDK/models/facecardnet_model/facecardmodel.pb")
            inputs_placeholder = tf.compat.v1.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.compat.v1.get_default_graph().get_tensor_by_name("embeddings:0")
            faces = []
            while True:
                if len(faces) == 0:
                    faces, landmarks = mtcnn_detector.detect(image)
                else:
                    # print("Faces: ", faces)
                    # print("Landmarks: ", landmarks)
                    break
            # root = './face_db/'
            # input_image = cv2.imread(root + file)
            # for i in range(faces.shape[0]):
            bbox = faces[0,:4]
            points = landmarks[0, :].reshape((5, 2))
            nimg = face_preprocess.preprocess(image, bbox, points, image_size='112,112')
            encoded_data = base64.b64encode(cv.imencode('.jpg', nimg)[1]).decode()
            nimg = nimg - 127.5
            nimg = nimg * 0.0078125
            # name = image.split(".")[0]

            input_image = np.expand_dims(nimg, axis=0)
            feed_dict = {inputs_placeholder: input_image}
            emb_array = sess.run(embeddings, feed_dict=feed_dict)
            embedding = sklearn.preprocessing.normalize(emb_array).flatten()
            
    return embedding, encoded_data

def obtain_enrol_embedding(image):
    embedding, encoded_data = return_embeddings(image, mtcnn_detector)
    temp_embedding = []
    temp_embedding.append(embedding)

    # Convert to string for saving
    # embed = ""
    # for i in range(128):
    #     embed += ", @F%s = %s" % (i, temp_embedding[0][i])
    
    return embedding

def match_user(image, embed):
    matching_embedding = obtain_enrol_embedding(image)
    np.savetxt('matching_embed.txt', matching_embedding)
    match_embed = np.loadtxt('matching_embed.txt', dtype=float)
    embed = np.loadtxt('embed.txt', dtype=float)
    results = face_recognition.compare_faces(matching_embedding, embed)
    if results[0] == True:
        print("You are Logged In!")
        return True
    else:
        print("Credentials Not Met!")
        return False

def test(mtcnn_detector):
    image = get_test_image(mtcnn_detector)
    embed = obtain_enrol_embedding(image)

    # # Saving Embeddings
    # np.savetxt('embed.txt', embed)
    # print("Embedding Saved, Try Recognition")

    # Matching Results Function
    match_result = match_user(image, embed)


if __name__ == "__main__":
    test(mtcnn_detector)