# -*- coding: utf-8 -*-
"""
Created on Sat May  2 12:33:53 2020

@author: AMAZING-GRACE
"""

import cv2
import numpy as np
import argparse

ap = argparse.ArgumentParser()

ap.add_argument('-src', '--source', required = True, help = "Path to source image")
ap.add_argument('-tar', '--target', required = True, help = "Path to target image")
args = vars(ap.parse_args())

def image_stats(image):
    l, a, b = cv2.split(image)
    (lMean, lStd) = (l.mean(), l.std())
    (aMean, aStd) = (a.mean(), a.std())
    (bMean, bStd) = (b.mean(), b.std())
    
    return (lMean, lStd, aMean, aStd, bMean, bStd)
    
    
def color_transfer(source, target):
    source = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype('float32')
    target = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype('float32')
    
    lMeanSrc, lStdSrc, aMeanSrc, aStdSrc, bMeanSrc, bStdSrc = image_stats(source)
    lMeanTar, lStdTar, aMeanTar, aStdTar, bMeanTar, bStdTar = image_stats(target)
    
    (l, a, b) = cv2.split(target)
    
    l -= lMeanTar
    a -= aMeanTar
    b -= bMeanTar
    
    l = (lStdTar/lStdSrc) * l
    a = (aStdTar/aStdSrc) * a
    b = (bStdTar/bStdSrc) * b
    
    l += lMeanSrc
    a += aMeanSrc
    b += bMeanSrc
    
    l = np.clip(l, 0, 255)
    a = np.clip(a, 0, 255)
    b = np.clip(b, 0, 255)
    
    target = np.merge([l, a, b])
    target = cv2.cvtColor(target.astype('uint8'), cv2.COLOR_LAB2BGR)
    
    return target

color_transfer(args['source'], args['target'])