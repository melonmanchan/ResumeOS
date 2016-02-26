#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Matti Jokitulppo"

from distutils.dir_util import copy_tree
from jinja2 import Template
from pyfiglet import Figlet

import click
import os

def get_real_path(filename):
    return os.path.dirname(os.path.realpath(__file__)) + filename

def render_template_file(file_name, context):
    """ Renders and overrides Jinja2 template files """
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
@click.option('--font',
            default='slant',
            help='The font used in the kickass README.md ASCII banner (used with pyfiglet)')
def main(name, output, font):
    """ Easily bootstrap an OS project to fool HR departments and pad your resume. """

    directory_name = os.getcwd() + os.sep + name.lower().replace(' ', '-') +  os.sep

    copy_tree(get_real_path(os.sep + 'my-cool-os-template'), directory_name)

    start_byte = int('0xb8000', 16)
    instructions_list = []

    # Create the necessary assembly mov instructions for printing out the output on boot
    for c in output:
        char_as_hex = '0x02'+ c.encode('hex')
        instructions_list.append('\tmov word [{0}], {1} ; {2}'.format(hex(start_byte), char_as_hex, c))
        start_byte += 2

    banner = Figlet(font=font).renderText(name)

    render_template_file(directory_name  + 'README.md', {'name' : name, 'banner' : banner})
    render_template_file(directory_name  + 'grub.cfg' , {'name' : name})
    render_template_file(directory_name  + 'boot.asm' , {'instructions_list' : instructions_list})

    print('finished bootstrapping OS project into directory ' + directory_name)

if __name__ == '__main__':
    main()

