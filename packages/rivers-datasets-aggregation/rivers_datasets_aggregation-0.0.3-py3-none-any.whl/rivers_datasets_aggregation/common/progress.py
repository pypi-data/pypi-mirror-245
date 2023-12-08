#!/usr/bin/env python
# coding: utf8
# Copyright 2023 CS GROUP
# Licensed to CS GROUP (CS) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# CS licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Progress bar."""

# pylint: disable=consider-using-f-string
import sys
import time


class ProgressAnimation:
    """ProgressAnimation class."""

    __animation_char__ = ["|", "/", "-", "\\"]

    def __init__(self, prefix, start, end):
        """
        Constructor.
        """

        self._start = start
        self._value = start
        self._end = end
        self._animation_counter = 0
        self._last_update_time = time.time()
        self._rewind_len = 0
        sys.stdout.write(prefix)
        sys.stdout.flush()

    def advance(self, custom_progress_string=None):
        """Advance progress animation."""

        self._value += 1
        current_time = time.time()

        if current_time - self._last_update_time > 0.25:
            self._last_update_time = current_time
            self._animation_counter += 1

            if self._animation_counter > 3:
                self._animation_counter = 0

            if custom_progress_string:
                counter_string = custom_progress_string

            elif self._end is not None:
                counter_string = " (%i/%i)" % (self._value, self._end)

            else:
                counter_string = " (%i)" % (self._value)

            sys.stdout.write("".join(["\b"] * self._rewind_len))
            sys.stdout.write(self.__animation_char__[self._animation_counter] + counter_string)
            sys.stdout.flush()
            self._rewind_len = len(counter_string) + 1

    def restart(self):
        """Restart progress animation."""

        sys.stdout.write("".join(["\b"] * self._rewind_len))
        sys.stdout.flush()
        self._rewind_len = 0

    def finalize(self, custom_progress_string=None):
        """Finalize progress animation"""

        sys.stdout.write("".join(["\b"] * self._rewind_len))

        if custom_progress_string:
            sys.stdout.write(custom_progress_string)

            if len(custom_progress_string) < self._rewind_len:
                sys.stdout.write("".join([" "] * (self._rewind_len - len(custom_progress_string))))

        else:
            sys.stdout.write("".join([" "] * self._rewind_len))
        sys.stdout.write("\n")
        sys.stdout.flush()


class Progress:
    """Progress class."""

    def __init__(self, start, end, steps=20, prefix="Progress"):
        """Constructor."""

        self._start = start
        self._end = end
        self._steps = steps
        self._cur = 0
        sys.stdout.write("%s: 000 %%" % prefix)
        sys.stdout.flush()

    def advance(self):
        """Advance progress."""

        self._cur += 1

        if int(self._cur * self._steps / (self._end - self._start)) > int(
            (self._cur - 1) * self._steps / (self._end - self._start)
        ):
            sys.stdout.write("\b" * 6)
            sys.stdout.write("# %03i %%" % int(self._cur * 100 / (self._end - self._start)))
            sys.stdout.flush()

        elif int(self._cur * 100 / (self._end - self._start)) > int((self._cur - 1) * 100 / (self._end - self._start)):
            sys.stdout.write("\b" * 5)
            sys.stdout.write("%03i %%" % int(self._cur * 100 / (self._end - self._start)))
            sys.stdout.flush()

    def finalize(self):
        """Finalize progress."""

        sys.stdout.write("\b" * 5)
        sys.stdout.write("100 %%")
        sys.stdout.write("\n")
        sys.stdout.flush()
