# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import os
from os.path import abspath, dirname

from restclients_core.dao import DAO


class SPACE_DAO(DAO):
    def __init__(self):
        super().__init__()

    def service_name(self):
        return "space"

    def service_mock_paths(self):
        return [abspath(os.path.join(dirname(__file__), "resources"))]
