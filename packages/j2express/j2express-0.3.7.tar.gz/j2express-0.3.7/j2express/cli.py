import click
from jinja2 import Environment
import os
import re


def enviro_value(value, key):
    return os.getenv(key, value)


def find_upper_case_envs(line):
    pattern = r"\{\{ ([A-Z0-9]+) \}\}"
    matches = re.findall(pattern, line)
    return [f"{{{{ {x} }}}}" for x in matches]


def process_file(filename):
    with open(filename, 'r') as f:
        template_lines = f.readlines()
    for i in range(0, len(template_lines)):
        env_vars = find_upper_case_envs(template_lines[i])
        for e_var in env_vars:
            clean_evar = re.sub(r"[{}\s]", "", e_var)
            template_lines[i] = template_lines[i].replace(
                e_var, f"{{{{ \"\" | enviro_value('{clean_evar}') }}}}")
    return template_lines


@click.command()
@click.option('-f', '--filename', help='J2 Template to process')
@click.option('--trim-blocks/--no-trim-blocks', show_default=True,
              default=False,
              help="Set renderer to trim_blocks")
@click.option('--lstrip-blocks/--no-lstrip-blocks', show_default=True,
              default=True,
              help="Set renderer to lstrip_blocks")
def main(filename, lstrip_blocks, trim_blocks):
    env = Environment(lstrip_blocks=lstrip_blocks, trim_blocks=trim_blocks)
    env.filters['enviro_value'] = enviro_value
    template_lines = process_file(filename)
    template = env.from_string("".join(template_lines))
    click.echo(template.render())


if __name__ == '__main__':
    main()
