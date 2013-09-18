#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:     Zhang Cheng <stephenpcg@gmail.com>
# Maintainer: Zhang Cheng <stephenpcg@gmail.com>

import os
import sys
import mmap
import errno
import struct

class UpdateApp(object):
    def __init__(self, update_app_file):
        self.update_app_file = update_app_file
        self.images = list()

        with open(self.update_app_file, "r+b") as fp:
            self.update_app = mmap.mmap(fp.fileno(), 0)

        start = 0
        while True:
            offset = self.update_app.find('\x55\xaa\x5a\xa5', start)
            if offset < 0: break

            # read head
            ## 4 magic
            ## 4 head size
            ## 4 version
            ## 8 hardware
            ## 4 unknown
            ## 4 body size
            ## 16 date
            ## 16 time
            ## 16 image name
            ## 16 blank
            ## 2 ?
            ## 4
            ## 2 * N
            ## padding to 4 aligned
            hsize = struct.unpack('<I', self.update_app[offset+4:offset+8])[0]
            bsize = struct.unpack('<I', self.update_app[offset+24:offset+28])[0]
            name = self.update_app[offset+60:offset+76].strip("\x00")

            # check if hsize == tsize + 98
            if bsize & 4095 != 0: tsize = (1 + (bsize >> 12)) * 2
            else: tsize = (bsize >> 12) * 2
            if tsize + 98 != hsize: raise Exception("Error: tsize + 98 != bsize")

            self.images.append( (name, offset, hsize, bsize) )
            start = offset + hsize + bsize

    def _human_size(self, size):
        if size < 1024:
            return "%4d B" % size
        elif size < 1024 * 1024:
            return "%3d KB" % (size / 1024.0)
        elif size < 1024 * 1024 * 1024:
            return "%3d MB" % (size / 1024.0 / 1024.0)
        elif size < 1024 * 1024 * 1024 * 1024:
            return "%3d GB" % (size / 1024.0 / 1024.0 / 1024.0)

    def list(self):
        i = 0
        for name, offset, hsize, bsize in self.images:
            print "%02d: offset = %08x, hsize = %08x, bsize = %08x(%s), name = %s" \
                    % (i, offset, hsize, bsize, self._human_size(bsize), name)
            i += 1

    def unpack(self):
        i = 0
        for name, offset, hsize, bsize in self.images:
            print "%02d: offset = %08x, hsize = %08x, bsize = %08x(%s), name = %s" \
                    % (i, offset, hsize, bsize, self._human_size(bsize), name)

            head_filename = "output/%s.head" % name.lower()
            with open(head_filename, "w+b") as fp:
                fp.write(self.update_app[offset:offset+hsize])

            body_filename = "output/%s.img" % name.lower()
            with open(body_filename, "w+b") as fp:
                fp.write(self.update_app[offset+hsize:offset+hsize+bsize])

            i += 1

if __name__ == "__main__":
    operation = "list"
    filename = "UPDATE.APP"

    for arg in sys.argv[1:]:
        if arg == "-l":
            operation = "list"
        elif arg == "-u":
            operation = "unpack"
        elif os.path.isfile(arg):
            filename = arg
        else:
            print "ignore unrecognized option:", arg

    try: os.makedirs("output")
    except OSError as e:
        if e.errno == errno.EEXIST: pass
        else: raise

    updateapp = UpdateApp(filename)
    if operation == "list":
        updateapp.list()
    elif operation == "unpack":
        updateapp.unpack()

# vim:ai:et:sts=4:sw=4:
