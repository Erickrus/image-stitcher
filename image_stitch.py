# -*- coding: utf-8 -*-

import os
import glob
import math
import numpy as np

from PIL import Image, ImageDraw

class ImageStitcher:
    def __init__(self):
        pass

    def get_stitch_position(self, im1, im2):
        # px1, px2 = np.array(im1.convert("L")), np.array(im2.convert("L"))
        px1, px2 = np.array(im1.convert("RGB")), np.array(im2.convert("RGB"))
        px1Line = px1[:,-1]
        # print(px1Line.shape)

        minDiff, minPos = 999999, 10000
        for i in range(px2.shape[1]):
            px2Line = px2[:,i]
            # MSE as difference
            diff = np.sqrt(np.sum((px2Line - px1Line)**2))
            #print(i, diff)
            if diff < minDiff:
                minDiff = diff
                minPos = i
        return minPos
    def mkdir(self, baseDir, dirName):
        try:
            os.mkdir(os.path.join(baseDir, dirName))
        except:
            pass

    def stitch(self, baseDir):

        self.mkdir(baseDir, "output")

        filenames = []
        for filename in glob.glob(os.path.join(baseDir,"*.PNG")):
            filenames.append(filename)
        sorted(filenames)

        batchSize = 30

        for i in range(math.ceil(len(filenames)/batchSize)):
            im = Image.open(filenames[i * batchSize])
            for j in range(1,batchSize):
                idx = i * batchSize + j
                if idx > len(filenames)-1:
                    break
                im1 = im
                im2 = Image.open(filenames[idx]).convert("RGB")

                stitchPos = self.get_stitch_position(im1, im2)
                im = Image.new(
                    "RGB",
                    (im1.size[0] + im2.size[0] - stitchPos,  im1.size[1]),
                    0xFFFFFF
                )

                im.paste(im1, (0, 0))
                im.paste(im2, (im1.size[0]-stitchPos, 0))
            im.save(os.path.join(baseDir, "output", "%d.png" %i))
                

