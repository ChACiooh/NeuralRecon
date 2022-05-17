from concurrent.futures import process
import os
import argparse
from multiprocessing import Pool
import multiprocessing
from SensorData import SensorData
import sys
import numpy as np


datapath_scannet = '/AppData/scannet/'


def run(pair):
    dir, path = pair
    # dir = dir.decode('utf-8')
    # path = path.decode('utf-8')
    if not os.path.exists(os.path.join(path + dir, 'color')):
        filename = path + dir + '/' + dir + '.sens'
        output_path = path + dir
        sys.stdout.write('loading %s...' % filename)
        sd = SensorData(filename)
        sys.stdout.write('loaded!\n')
        sd.export_depth_images(os.path.join(output_path, 'depth'))
        sd.export_color_images(os.path.join(output_path, 'color'))
        sd.export_poses(os.path.join(output_path, 'pose'))
        sd.export_intrinsics(os.path.join(output_path, 'intrinsic'))
    return 0

if __name__ == '__main__':
    paths = [datapath_scannet + 'scans/', datapath_scannet + 'scans_test/']

    num_select = 16

    for path in paths:
        #dirs = [dir.encode(encoding='utf-8') for dir in os.listdir(path)]
        dirs = os.listdir(path)
        for index in np.arange(0, len(dirs), num_select):
            with Pool(processes=num_select) as p:
                results = p.map(run, zip(dirs[index: index + num_select], [path] * num_select))