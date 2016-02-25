#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Matti Jokitulppo"

import click
from distutils.dir_util import copy_tree
import os
from jinja2 import Template

def get_real_path(filename):
    return os.path.dirname(os.path.realpath(__file__)) + filename

def render_template_file(file_name, context):
    """ Renders Jinja2 template files """
    with open(file_name, 'r+') as f:
        template = Template(f.read())
        output = template.render(context)
        f.seek(0)
        f.write(output)
        f.truncate()


@click.command()
@click.option('--name',
            default='my-own-cool-os',
            help='The name of your OS',
            prompt='What is the name of your OS? ')
@click.option('--output',
            default='Hello, world!',
            help='The string output by your OS on boot',
            prompt='What do you want to print on boot? ')
def main(name, output):
    """ Easily bootstrap an OS project to fool HR departments and pad your resume. """
    directory_name = os.getcwd() + '/' + name.lower().replace(' ', '-') + '/'
    print(directory_name)

    copy_tree(get_real_path('/my-cool-os'), directory_name)

    render_template_file(directory_name  + 'README.md', {'name': name})
    render_template_file(directory_name  + 'grub.cfg', {'name': name})

if __name__ == '__main__':
    main()


