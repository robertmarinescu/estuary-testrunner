#!/usr/bin/env python3

import os

from entities.render import Render

if __name__ == '__main__':
    render = Render(os.environ.get('TEMPLATE'), os.environ.get('VARIABLES'))
    render.rend_template()
