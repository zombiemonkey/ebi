# coding: utf-8 -*-

import os
import tempfile
import shutil
import yaml
import os
import types
import sys
import fnmatch

import salt.cli.caller
from salt.exceptions import (
    SaltClientError,
    CommandNotFoundError,
    CommandExecutionError,
    SaltInvocationError,
)

import ebi.config

class EbiCaller(salt.cli.caller.Caller):
    def __init__(self, root, fun=None, arg=[]):
        self.env = tempfile.mkdtemp()
        self.root = root
        
        minion_opts = ebi.config.ebi_minion_config()
        minion_opts.update({
            'id': 'local',
            'conf_file': os.path.abspath('{0}/minion'.format(self.env)),
            'file_client': 'local',
            'fileserver_backend': ['roots'],
            'log_level': 'warning',
            'log_level_logfile': 'warning',
            'log_file': os.path.abspath('{0}/log'.format(self.env)),
            'cachedir': os.path.abspath('{0}/cache'.format(self.env)),
            'returner_dirs': [
                os.path.abspath('{0}/ebi/returners'.format(self.root))
            ],
            'module_dirs': [
                os.path.abspath('{0}/ebi/modules'.format(self.root))
            ],
            'states_dir': [
                os.path.abspath('{0}/ebi/states'.format(self.root))
            ],
            'grains_dir': [
                os.path.abspath('{0}/ebi/grains'.format(self.root))
            ],
            'file_roots': {
                'base': [
                    os.path.abspath('{0}/state'.format(self.env)),
                    os.path.abspath('{0}/tasks'.format(self.root))
                ]
            },
            'pillar_roots': {
                'base': [
                    os.path.abspath('{0}/pillar'.format(self.env)),
                    os.path.abspath('{0}/config_pillar'.format(self.root))
                ]
            },
            'extension_modules': '',
            'retcode_passthrough': True
        })
        
        if os.path.isdir('{0}/config_grains'.format(self.root)):
            minion_opts['grains'] = self._load_static_data(
                '{0}/config_grains'.format(self.root))
        
        if os.path.isdir('{0}/config_pillar'.format(self.root)):
            if not os.path.exists('{0}/pillar'.format(self.env)):
                os.mkdir('{0}/pillar'.format(self.env))
            pillar_top = {
                'base': {
                    '*': self._sls_library(
                            '{0}/config_pillar'.format(self.root),
                            self._sls_walk(
                                '{0}/config_pillar'.format(self.root)))
                }
            }
            yaml.safe_dump(
                pillar_top,
                open('{0}/pillar/top.sls'.format(self.env), 'w'))
                
        yaml.safe_dump(minion_opts,
                       open('{0}/minion'.format(self.env), 'w'))
                
        minion_opts['fun'] = fun
        minion_opts['arg'] = arg
        
        super(EbiCaller, self).__init__(minion_opts)

    def _sls_walk(self, path):
        sls_list = []
        
        for root, dirname, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, '*.sls'):
                sls_list.append(os.path.join(root, filename))
                
        return sls_list

    def _load_static_data(self, path):
        data = {}
        
        for sls_file in self._sls_walk(path):
            data.update(yaml.load(open(sls_file, 'r')))
                
        return data

    def _sls_library(self, root, sls_list):
        library = []
        for sls in sls_list:
            if sls.startswith(root):
                sls = sls[len(root):]
            if sls.startswith('/'):
                sls = sls[1:]
            if sls.endswith('/init.sls'):
                sls = os.path.dirname(sls)
            if sls.endswith('.sls'):
                sls = sls[:-4]
            if sls.endswith('/'):
                sls = sls[:-1]
            library.append(sls.replace('/', '.'))
            
        return library
        
    def print_docs(self):
        if self.opts['fun']:
            super(EbiCaller, self).print_docs()
        else:
            sys.stderr.write('You must specify a function or task in the form: '
                             'ebi -d <module.function>\n')
            sys.exit(os.EX_UNAVAILABLE)
    
    def print_tasks(self):
        tasks = self._sls_library(
            '{0}/tasks'.format(self.root),
            self._sls_walk('{0}/tasks'.format(self.root)))
                
        if len(tasks) == 0:
            sys.stdout.write(
                '\nNo tasks found for task root {0}\n\n'.format(self.root))
            sys.exit(os.EX_UNAVAILABLE)
            
        sys.stdout.write('\nTasks [{0}]:\n\n'.format(self.root))
        for task in tasks:
            sys.stdout.write('    {0}\n'.format(task))
        sys.stdout.write('\n')
        
    def __del__(self):
        if os.path.exists(self.env):
            shutil.rmtree(self.env)

    def run(self):
        try:
            ret = self.call()
            salt.output.display_output(
                    {'local': ret.get('return', {})},
                    ret.get('out', 'nested'),
                    self.opts)
            for k, v in ret['return'].iteritems():
                if not v.get('result', True):
                    sys.exit(1)
            if self.opts.get('retcode_passthrough', False):
                sys.exit(ret['retcode'])
        except SaltInvocationError as err:
            raise SystemExit(err)