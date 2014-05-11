# coding: utf-8 -*-

import sys
import os

import ebi.parsers
import ebi.cli.caller

class EbiCLI(ebi.parsers.EbiCLIOptionParser):
    def run(self):
        self.parse_args()
        
        fun = self.config['fun']
        arg = self.config['arg']
        
        caller = ebi.cli.caller.EbiCaller(self.options.root, fun, arg)
        
        if self.options.doc:
            caller.print_docs()
            self.exit(os.EX_OK)
        
        if self.options.list:
            caller.print_tasks()
            self.exit(os.EX_OK)
        
        if self.options.grains:
            caller.print_grains()
            self.exit(os.EX_OK)
        
        if self.options.pillar:
            pass
        
        caller.run()