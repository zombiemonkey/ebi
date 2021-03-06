# coding: utf-8 -*-

import optparse

import ebi.config
import ebi.version

class EbiCLIOptionParser(optparse.OptionParser):
    VERSION = ebi.version.__version__
    usage = "%prog [options] (-t task pillar='JSON'|module.fun args)"

    def __init__(self, *args, **kwargs):
        self.config = ebi.config.ebi_config()
        kwargs.setdefault('version', '%prog {0}'.format(self.VERSION))
        kwargs.setdefault('usage', self.usage)

        optparse.OptionParser.__init__(self, *args, **kwargs)
        
        self.add_option(
            '-r',
            '--root',
            default=self.config['root'],
            action='store',
            dest='root',
            type='string',
            metavar='ROOT',
            help='Specify a different root directory'
        )

        self.add_option(
            '-t',
            '--task',
            default=None,
            action='store',
            dest='task',
            type='string',
            metavar='TASK',
            help='Specify a task to execute'
        )

        self.add_option(
            '-d',
            '--doc',
            default=False,
            action='store_true',
            dest='doc',
            help=('Return the documentation for the specified module or '
                'for all modules if none are specified.')
        )

        self.add_option(
            '-l',
            '--list',
            default=False,
            action='store_true',
            dest='list',
            help='List available tasks'
        )
        
        self.add_option(
            '-g',
            '--grains',
            default=False,
            action='store_true',
            dest='grains',
            help='Return the information generated by the salt grains'
        )
        
        self.add_option(
            '-p',
            '--pillar',
            default=False,
            action='store_true',
            dest='pillar',
            help='Return the information within the computed pillar output'
        )

    def parse_args(self, args=None, values=None):
        options, args = optparse.OptionParser.parse_args(self, args, values)
        self.options, self.args = options, args
        
        if self.options.task:
            self.config['fun'] = 'state.sls'
            self.config['arg'] = self.options.task.split(',')
            self.config['arg'] += args if len(args) > 0 else []
        elif self.options.pillar:
            self.config['fun'] = 'pillar.items'
            self.config['arg'] = []
        else:
            self.config['fun'] = args[0] if len(args) > 0 else None
            self.config['arg'] = args[1:] if len(args) > 1 else []            
