#!/usr/bin/env python

from distutils.core import setup

setup(name='rtsp_to_image',
    version='0.1',
    description='RTSP to ROS Image converter',
    author='Adi Bar Ilan',
    author_email='adi.perfetto@gmail.com',
    scripts=['rtsp_to_image/convert_stream.py']
    )
