import cv2
import numpy as np
import scipy
import _pickle as pickle
import random
import os
import matplotlib.pyplot as plt

# Program Face-Recognition
def features_extract(img_path, vectorsize=32):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    try:
        kaze = cv2.KAZE_create()
        kp = kaze.detect(img,None)
        kp = sorted(kp, key=lambda x: -x.response)[:vectorsize]
        kp, des = kaze.compute(img,kp)
        des = des.flatten()
        if (des.size < vectorsize*64):
            des = np.concatenate([des, np.zeros((vectorsize*64) - des.size)])
    except cv2.error as e:
        print('Error: ', e)
        return None
    return des

def extract_batch(img_path, pickled_path="features.pck"):
    files = [os.path.join(root, file) for root, dirs, files in os.walk(img_path) for file in files if file.endswith(".jpg")]
    result = {}
    for f in files:
        print('Extracting features from image %s' % f)
        result[f] = features_extract(f)
    fp = open("../bin/"+pickled_path,'wb')
    pickle.dump(result,fp)
    return result

class Matcher(object):
    
    def __init__(self, pickled_path="features.pck"):
        fp = open(pickled_path,'rb')
        self.data = pickle.load(fp)
        self.names = []
        self.features = []
        for k, v in self.data.items():
            self.names.append(k)
            self.features.append(v)
        self.features = np.array(self.features)
        self.names = np.array(self.names)

    def euclid_dist(self, vector):
        # Metode euclidian distance
        v = vector.reshape(1,-1)
        dist = np.array([])
        for i in range(len(self.features)):
            temp = 0
            for j in range(len(self.features[i])):
                temp += (self.features[i][j] - v[0][j])**2
            dist = np.append(dist,temp**0.5)
        return dist.reshape(-1)

    def cos_sim(self,vector):
        # Metode cosine similarity
        v = vector.reshape(1,-1)
        sim = np.array([])
        magv = 0
        for i in range(len(v[0])):
            magv += v[0][i]**2
        magv = magv**0.5
        for i in range(len(self.features)):
            dot = 0
            magu = 0
            for j in range(len(self.features[i])):
                dot += self.features[i][j] * v[0][j]
                magu += self.features[i][j]**2
            magu = magu**0.5
            sim = np.append(sim,1-(dot/(magu*magv)))
        return sim.reshape(-1)

    def cos_euc_sim(self, vector):
        # Metode gabungan cosine dan euclidian
        cos = self.cos_sim(vector).reshape(-1)
        euc = self.euclid_dist(vector).reshape(-1)
        sim = np.array([])
        for i in range(len(cos)):
            sim = np.append(sim,cos[i]+euc[i])
        return sim.reshape(-1)

    def match(self, image_path, method=2, topn=5):
        features = features_extract(image_path)
        if (method == 0):
            img_distances = self.euclid_dist(features)
        elif (method == 1):
            img_distances = self.cos_sim(features)
        else:
            img_distances = self.cos_euc_sim(features)
        nearest_ids = np.argsort(img_distances)[:topn].tolist()
        nearest_img_paths = self.names[nearest_ids].tolist()
        perc = img_distances[nearest_ids].tolist()
        for i in range(len(perc)):
            if (method == 0):
                perc[i] = (20-perc[i])*5
            elif (method == 1):
                perc[i] = (1-perc[i])*100
            else:
                perc[i] = (20-perc[i])*5
        return nearest_img_paths, perc
    
def run():
    images_path_db = str(input("Images database folder path: "))
    random_bool = str(input("Random sample? (y/n): "))
    images_path_sm = str(input("Images sample(s) folder path: "))
    T = int(input("How many match result shown: "))
    sm = [os.path.join(root, file) for root, dirs, files in os.walk(images_path_sm) for file in files if file.endswith(".jpg")]
    db = [os.path.join(root, file) for root, dirs, files in os.walk(images_path_db) for file in files if file.endswith(".jpg")]
    if (images_path_db!='database/'):
        namepck = images_path_db.split('/')[-1].lower()
    else:
        namepck = 'default'
    if not(os.path.exists("../bin/"+namepck+".pck")):
        extract_batch(images_path_db,pickled_path=namepck+".pck")
    ma = Matcher(pickled_path="../bin/"+namepck+".pck")
    
    if (random_bool.lower() == 'y'):
        N = int(input("How many sample to match: "))
        sample = random.sample(sm, N)
    else:
        sample = [images_path_sm]


    for s in sample:
        names, match = ma.match(s,topn=T)
        fig=plt.figure(num='Matches',figsize=(10, 10))
        columns = 3
        rows = 1 + (len(match)//3)
        print('Query image ==========================================')
        img = cv2.imread(s)
        fig.add_subplot(rows, columns, 2)
        kaze = cv2.KAZE_create()
        kp = kaze.detect(img,None)
        img2 = cv2.drawKeypoints(img,kp,outImage=None,color=(0,255,0),flags=0)
        plt.imshow(img2[...,::-1])
        print('Result images ========================================')
        i = 0
        ax = [0]*(columns*rows +1)
        for j in range(4, columns*rows +1):
            img = cv2.imread(names[i])
            print('Match %f' % (1-match[i]))
            ax[i] = fig.add_subplot(rows, columns, j)
            ax[i].title.set_text('Match %.2f' % (match[i]) + '%')
            plt.imshow(img[...,::-1])
            i+=1
            if (i == len(match)):
                break
        plt.show()

#delete '# to run with console
#run()
