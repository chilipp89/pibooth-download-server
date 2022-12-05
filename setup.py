#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from io import open
import os.path as osp
from setuptools import setup


HERE = osp.abspath(osp.dirname(__file__))
sys.path.insert(0, HERE)
import pibooth_qr_download as plugin


def main():
    setup(
        name=plugin.__name__,
        version=plugin.__version__,
        description=plugin.__doc__,
        long_description=open(osp.join(HERE, 'README.md'), encoding='utf-8').read(),
        long_description_content_type='text/markdown',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: MIT License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Natural Language :: English',
            'Topic :: Multimedia :: Graphics :: Capture :: Digital Camera',
        ],
        author="P. Junietz",
        url="https://github.com/chilipp89/pibooth-qr-download",
        license='MIT',
        platforms=['unix', 'linux'],
        keywords=[
            'Raspberry Pi',
            'camera',
            'photobooth',
            'qrcode'
        ],
        py_modules=['pibooth_qr_download', 'qr_filetransfer'],
        python_requires=">=3.6",
        install_requires=[
            'pibooth>=2.0.0',
            'netifaces'
        ],
        zip_safe=False,  # Don't install the lib as an .egg zipfile
        entry_points={'pibooth': ["pibooth_qr_download = pibooth_qr_download"]},
    )


if __name__ == '__main__':
    main()