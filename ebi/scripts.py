# coding: utf-8 -*-

import ebi
import ebi.cli

def ebi_cli():
    try:
        _ebi_cli = ebi.cli.EbiCLI()
        _ebi_cli.run()
    except KeyboardInterrupt:
        raise SystemExit('\nExiting gracefully on Ctrl-c')
