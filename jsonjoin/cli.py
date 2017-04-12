"""Command-Line Interface."""

import sys

import click
from click import argument, option, version_option

from jsoncut.cli import load_json, output


from . import core
from . import exceptions as exc


def join_(d1, d2, kwds):
    """Join JSON documents."""
    kwds_copy = kwds.copy()
    for key in ('indent', 'jsonfile', 'nocolor'):
        del kwds_copy[key]
    try:
        return core.join_(d1, d2, **kwds_copy)
    except exc.JsonJoinError as e:
        click.echo(e.format_error(), err=True)
        sys.exit(1)


@click.command()
@argument('jsonfile1', type=click.Path(readable=True), required=False)
@argument('jsonfile2', type=click.Path(readable=True), required=False)
@option('-r', '--root', 'rootkey', help='Set the root of the JSON document')
@option('-k', '--keys', type=(str, str),
        help='replace key in 1st document with key in 2nd document')
@option('-v', '--values', type=(str, str),
        help='replace value in 1st document with value in 2nd document')
@option('-K', '--keyval', type=(str, str),
        help='replace key in 1st document with value in 2nd document')
@option('-V', '--valkey', type=(str, str),
        help='replace value in 1st document with key in 2nd document')
@option('-l', '--list', 'listkeys', is_flag=True,
        help='numbered JSON keys list')
@option('-i', '--inspect', is_flag=True,
        help='inspect JSON document; all keys, indexes & types')
@option('-f', '--fullscan', is_flag=True, help='deep inpections')
@option('-q', '--quotechar', default='"', help='set quoting char for keys')
@option('-I', '--indent', type=int, help='indent JSON when redirecting')
@option('-c', '--nocolor', is_flag=True, help='disable syntax highlighting')
@version_option(version='0.1.0', prog_name='JSON Cut')
@click.pass_context
def main(ctx, **kwds):
    """Quickly select or filter out properties in a JSON document."""
    if kwds['nocolor']:
        ctx.color = False
    d1 = load_json(ctx, kwds['jsonfile1'])
    d2 = load_json(ctx, kwds['jsonfile2'])
    results = join_(d1, d2, kwds)
    is_json = not (kwds['listkeys'] or kwds['inspect'])
    output(ctx, results, kwds['indent'], is_json)


if __name__ == '__main__':
    main()
