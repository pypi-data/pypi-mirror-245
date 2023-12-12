import os
import cv2
import numpy as np

import argparse
import shutil

from glob import glob
from pathlib import Path
from typing import Any, Union
from joblib import Parallel, delayed
from tqdm import tqdm

_SUPPORT_VIDEO_EXTENSIONS_ = [
    '.mp4', '.avi', '.webm', 'flv', 'mkv', 'mpg',
]

_SUPPORT_IMAGE_EXTENSIONS_ = [
    '.jpg', 'jpeg', 'png', 'bmp', 'tif', 'tiff', 'webp',
]

_VID_FOURCC_ = {
    'mp4': 'h264',  # 'avc1',
    'avi': 'xvid',  # 'xvid', 'i420'是无压缩yuv可能会很大
    'mkv': 'h264',
    'flv': 'h264',
}


def str2bool(v: str) -> bool:
    return v.lower() in ('yes', 'true', 't', 'y', '1')


def argparser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='A converter to convert images to videos.')

    '''Overall parameters'''
    parser.add_argument('--img-dir',
                        type=str,
                        default='',
                        required=True,
                        help='Directory with images to convert.')
    parser.add_argument('--img-ext',
                        type=str,
                        default=None,
                        help='Extension of images to convert. If not provided, will default to mixed extensions.')
    parser.add_argument('--output-dir',
                        type=str,
                        default=None,
                        help='Directory to save converted video. If not provided, will default to the images directory.')
    parser.add_argument('--vid-ext',
                        type=str,
                        default=None,
                        help='Extension of video to convert. If not provided, will default to .mp4.')

    '''Video parameters'''
    parser.add_argument('--fps',
                        type=int,
                        default=30,
                        help='Frames per second for the converted video.')
    parser.add_argument('-H', '--video-height',
                        type=int,
                        default=None,
                        help='Height of the converted video.')
    parser.add_argument('-W', '--video-width',
                        type=int,
                        default=None,
                        help='Width of the converted video.')

    '''Process parameters'''
    parser.add_argument('--parallel',
                        type=str2bool,
                        default=True,
                        help='Whether to initialize CPU-based parallel processing to convert.')

    # TODO
    # parser.add_argument('--sort-img',
    #                     type=str,
    #                     default=None,
    #                     help='Whether to sort images. If input \'ascending\', the images will be sorted in ascending '
    #                          'way; if input \'descending\', the images will be sorted in descending way; if default '
    #                          'to None (not None in string), the images will be arranged by the glob mechanism.')
    # parser.add_argument('--interval',
    #                     type=int,
    #                     default=1,
    #                     help='')

    return parser.parse_args()


class img2vid(object):

    def __init__(self,
                 img_dir: str,
                 img_ext,
                 output_dir,
                 vid_ext,
                 parallel,
                 fps,
                 height,
                 width,
                 sort_img=False,
                 interval=1):
        self.imgDir = img_dir
        self.imgExt = img_ext
        # TODO: Allow None as image extension
        if self.imgExt is None:
            raise ValueError('Doesn\'t support auto image extension. Please specify an image extension for now.')
        self.outputDir = output_dir
        self.vidExt = vid_ext
        # TODO: Allow None as video extension
        if self.vidExt is None:
            raise ValueError('Doesn\'t support auto video extension. Please specify a video extension for now.')
        self.interval = interval  # TODO
        self.fps = fps
        self.height = height
        self.width = width

        self.sortImg = sort_img  # TODO
        self.parallel = parallel
        self.cores = os.cpu_count()

    def __call__(self):
        self._img2vid()

    def _read_imgs(self):

        # TODO:
        #  1. Get all images of supported formats.
        #  2. Verify height and width of all images.
        #  3. Define new video regardless of the video extension.
        #  4. Sort images according to filenames.

        self.imgPaths = sorted(list(Path(self.imgDir).glob(f'*.{self.imgExt}')))
        self.h, self.w, _ = cv2.imdecode(np.fromfile(self.imgPaths[0], dtype=np.uint8), cv2.IMREAD_COLOR).shape
        self.vw = cv2.VideoWriter(os.path.join(self.outputDir, f'{Path(self.imgDir).stem}_Video.{self.vidExt}'),
                                  cv2.VideoWriter_fourcc(*_VID_FOURCC_[self.vidExt].upper()),
                                  self.fps, (self.width, self.height))

    def _img2vid(self):
        for path in tqdm(self.imgPaths, desc='Converting images to one video'):
            img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
            self.vw.write(img)
        self.vw.release()


if __name__ == '__main__':
    args = argparser()

    img2vid(
        img_dir=args.img_dir,
        img_ext=args.img_ext,
        output_dir=args.output_dir,
        vid_ext=args.vid_ext,
        parallel=args.parallel,
        fps=args.fps,
        height=args.height,
        width=args.width,
    )()
