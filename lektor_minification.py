#!/usr/bin/env python
# encoding: utf-8
"""
minification.py

A simple plugin to handle image minification

Created by Pierre-Julien Grizel et al.
Copyright (c) 2016 NumeriCube. All rights reserved.


"""
from __future__ import unicode_literals

__author__ = ""
__copyright__ = "Copyright 2016, NumeriCube"
__credits__ = ["Pierre-Julien Grizel", ]
__license__ = "GNU GPLv3"
__version__ = "1.1.5"
__maintainer__ = "Pierre-Julien Grizel"
__email__ = "pjgrizel@numericube.com"
__status__ = "Production"

import shutil
import imghdr
from os.path import abspath, dirname, join, isfile

import pyimagediet

# Lektor stuff
from lektor.pluginsystem import Plugin
from lektor.build_programs import FileAssetBuildProgram, AttachmentBuildProgram, BuildProgram
from lektor.assets import File
from lektor.sourceobj import VirtualSourceObject
from lektor.project import Project
from lektor.db import Image
from werkzeug._internal import _log

# Load and parse the pyimagediet configuration
config_filename = abspath(join(Project.discover().project_path, '..', 'configs', 'minification.yml'))

if not isfile(config_filename):
    from pyimagediet.process import DEFAULT_CONFIG as DIET_CONFIG
else:
    DIET_CONFIG = pyimagediet.read_yaml_configuration(config_filename)

try:
    DIET_CONFIG = pyimagediet.parse_configuration(DIET_CONFIG)
except pyimagediet.ConfigurationErrorDietException, e:
    raise Exception(e.msg)


def copy_and_optimize(src, dst):
    """Make sure it's an image, and then optimize on place"""
    img_type = imghdr.what(src)
    if img_type in ('png', 'jpeg', 'gif'):

        # Copy the artifact file to its destination
        shutil.copyfile(src, dst)

        # Perform the optimization
        try:
            result=pyimagediet.diet(dst, DIET_CONFIG)
            if result:
                _log('info', "(optimized)")
        except pyimagediet.CompressFileDietException, e:
            raise Exception(e.msg)


class MinificationPlugin(Plugin):
    """The main plugin class"""
    name = 'Minification'
    description = 'A plugin that compresses images on-the-fly when building site.'

    def on_setup_env(self, **extra):
        """Register our build program for File objects.
        NOTA: We'll need to find a way to 'propagate' those build to other builder
        if the one we're supplying is not satisfying"""
        # Our gory way of overriding build_programs to handle compression on-the-fly
        self.env.add_build_program(File, ImageAssetBuildProgram)
        self.env.add_build_program(Image, ImageAttachmentBuildProgram)
        # self.env.add_build_program(VirtualSourceObject, ThumbnailBuildProgram)


class ImageAssetBuildProgram(FileAssetBuildProgram):
    """The image program builder"""

    def build_artifact(self, artifact):
        """This method is invoked for previously declared artifacts and is supposed to write out the artifact. It's only invoked if the builder decided that the artifact is outdated based on the information at hand.
        """

        # Let Lektor try to copy the file, which is necessary if the file isn't an image
        super(ImageAssetBuildProgram, self).build_artifact(artifact)
        copy_and_optimize(self.source.source_filename, artifact.dst_filename)



class ImageAttachmentBuildProgram(AttachmentBuildProgram):

    def build_artifact(self, artifact):
        # Let Lektor try to copy the file, which is necessary if the file isn't an image
        super(ImageAttachmentBuildProgram, self).build_artifact(artifact)
        copy_and_optimize(self.source.attachment_filename, artifact.dst_filename)


# Monkey patching make_thumbnails to add support for image optimization

import lektor
import wrapt

@wrapt.decorator
def optimize_after(wrapped, instance, args, kwargs):
    # we are overriding :
    # def process_image(ctx, source_image, dst_filename, width, height=None, crop=False):
    # so args[2] is dst_filename
    dst = args[2]
    final=wrapped(*args, **kwargs)
    try:
        result=pyimagediet.diet(dst, DIET_CONFIG)
        if result:
            _log('info', "(optimized)")
    except pyimagediet.CompressFileDietException, e:
        raise Exception(e.msg)
    return final

lektor.imagetools.process_image = optimize_after(lektor.imagetools.process_image)
