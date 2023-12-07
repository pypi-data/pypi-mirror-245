#!/usr/bin/env python

# Copyright (C) Raffaele Salmaso <raffaele@salmaso.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
from os.path import dirname
import sys

from stua.commands import BaseCommand
from stua.os import system


COMMAND = os.environ.get("DJANGO_COMMAND", "manage.py")
PYTHON = os.environ.get("PYTHON", "python3")


class Command(BaseCommand):
    def find_manage_py(self, path=None):
        path = path or os.getcwd()

        while path != "/":
            manage = os.path.join(path, COMMAND)
            if os.path.exists(manage):
                return path
            path = dirname(path)
        return False

    def build_cmd(self, args):
        cmd = []

        try:
            cmd.append(PYTHON)
        except:
            pass
        cmd.append("./{}".format(COMMAND))

        if len(args) > 0:
            if args[0] == "test":
                # test are always verbose if not tell otherwise
                verbosity = [True for arg in args if arg.startswith("--verbosity")]
                if not verbosity:
                    args.append("--verbosity=2")
        cmd.extend(args)

        return cmd

    def handle(self, command, args):
        path = self.find_manage_py()

        status = 0
        if path:
            os.chdir(path)
            cmd = self.build_cmd(args)
            status = system(cmd, env=os.environ).returncode
        return status


def main():
    dj = Command()
    status = dj.run(sys.argv)
    sys.exit(status)
