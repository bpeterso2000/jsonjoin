"""Command-Line Interface."""
import sys

import click
from click import argument, option, version_option
from jsoncut.cli import load_json, output

from . import core

JOIN_TYPES = list(core.JOIN_FUNCTS.keys())


def join_(d1, d2, key, **kwds):
    """Join JSON documents."""
    kwds_copy = kwds.copy()
    for drop_key in ('indent', 'nocolor'):
        del kwds_copy[drop_key]
    # try:
    return core.join_(d1, d2, key, **kwds_copy)
    # except exc.JsonJoinError as e:
    #     click.echo(e.format_error(), err=True)
    #    sys.exit(1)


@click.command()
@argument('json_left', type=click.Path(readable=True), required=False)
@argument('json_right', type=click.Path(readable=True), required=False)
@option('-k', '--key', required=True,
        help='Select the primary key for the left document (JSON Key)')
@option('-K', '--rgtkey',
        help='Select the primary key for the right document (JSON Key)')
@option('-r', '--root', help='Set the root of the left document (JSON Key')
@option('-R', '--rgtroot', help='Set the root of the right document (JSON Key')
@option('-j', '--join', 'jointype', type=click.Choice(JOIN_TYPES),
        default='inner', help='Set the join type')
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
    d1 = load_json(ctx, kwds.pop('json_left'))
    d2 = load_json(ctx, kwds.pop('json_right'))
    key = kwds.pop('key')
    results = join_(d1, d2, key, **kwds)
    output(ctx, results, kwds['indent'], False)

if __name__ == '__main__':
    main()
