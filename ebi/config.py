# coding: utf-8 -*-

import os
import copy
import salt.config

DEFAULT_EBI_CONFIG = {
    'root': os.getcwd(),
    'list': False,
    'grains': False,
    'pillar': False
}

def ebi_config():
    return copy.deepcopy(DEFAULT_EBI_CONFIG)

def ebi_minion_config():
    return copy.deepcopy(salt.config.DEFAULT_MINION_OPTS)