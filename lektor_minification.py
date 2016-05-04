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
__version__ = "1.0"
__maintainer__ = "Pierre-Julien Grizel"
__email__ = "pjgrizel@numericube.com"
__status__ = "Production"

import shutil
import imghdr
import subprocess
import os.path

# PIL stuff
# from PIL import Image

# Lektor stuff
from lektor.pluginsystem import Plugin
from lektor.sourceobj import VirtualSourceObject
from lektor.build_programs import FileAssetBuildProgram
# from lektor.utils import build_url
from lektor.assets import File, Directory

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
        # Check image file type
        # Default/fallback behaviour is to copy file to the dest directory 'as is'.
        img_type = imghdr.what(self.source.source_filename)
        if img_type == 'png':
            parameters = {
                "destination":      artifact.dst_filename,
                "source":           self.source.source_filename,
                "command":          "optipng",
                "optimization":     "",
            }
            artifact.ensure_dir()
            subprocess.check_call("""%(command)s %(optimization)s -out "%(destination)s" -- "%(source)s" """ % parameters, shell=True)

        elif img_type == 'jpeg':
            parameters = {
                "destination":      os.path.dirname(artifact.dst_filename),
                "source":           self.source.source_filename,
                "command":          "jpegoptim",
                "optimization":     "",
            }
            artifact.ensure_dir()
            subprocess.check_call("""%(command)s %(optimization)s -d "%(destination)s" -- "%(source)s" """ % parameters, shell=True)

        else:
            super(ImageBuildProgram, self).build_artifact(artifact)



