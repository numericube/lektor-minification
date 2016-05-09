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
__version__ = "1.1"
__maintainer__ = "Pierre-Julien Grizel"
__email__ = "pjgrizel@numericube.com"
__status__ = "Production"

import shutil
import imghdr
from os.path import abspath, dirname, join

import pyimagediet

# Lektor stuff
from lektor.pluginsystem import Plugin
from lektor.build_programs import FileAssetBuildProgram
from lektor.assets import File

# Load and parse the pyimagediet configuration
THIS_DIR = abspath(dirname(__file__))
config = pyimagediet.read_yaml_configuration(join(THIS_DIR, 'config.yml'))
try:
    config = pyimagediet.parse_configuration(config)
except pyimagediet.ConfigurationErrorDietException, e:
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
        self.env.add_build_program(File, ImageBuildProgram)

class ImageBuildProgram(FileAssetBuildProgram):
    """The image program builder"""

    def build_artifact(self, artifact):
        """This method is invoked for previously declared artifacts and is supposed to write out the artifact. It's only invoked if the builder decided that the artifact is outdated based on the information at hand.
        """

        # Let Lektor try to copy the file, which is necessary if the file isn't an image
        super(ImageBuildProgram, self).build_artifact(artifact)

        # Optimize the artifact file if we're sure that it's an image
        img_type = imghdr.what(self.source.source_filename)
        if img_type in ('png', 'jpeg', 'gif'):

            # Copy the artifact file to its destination
            shutil.copyfile(self.source.source_filename, artifact.dst_filename)

            # Perform the optimization
            try:
                pyimagediet.diet(artifact.dst_filename, config)
            except pyimagediet.CompressFileDietException, e:
                raise Exception(e.msg)
