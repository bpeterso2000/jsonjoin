import json

import click
# import pytest
from click import argument, option, version_option
from click.testing import CliRunner

from jsonjoin.cli import JOIN_TYPES

"""
    @option('-k', '--key',
            help='Select the primary key for the left document (JSON Key)')
    @option('-K', '--rgtkey',
            help='Select the primary key for the right document (JSON Key)')
    @option('-r', '--root', help='Set the root of the left document (JSON Key')
    @option('-R', '--rgtroot',
            help='Set the root of the right document (JSON Key')
    @option('-j', '--join', 'join_type', type=click.Choice(JOIN_TYPES),
            default='inner', help='Set the join type')
    @option('-f', '--fullscan', is_flag=True, help='deep inpections')
    @option('-q', '--quotechar', default='"', help='set quoting char for keys')
    @option('-I', '--indent', type=int, help='indent JSON when redirecting')
    @option('-c', '--nocolor', is_flag=True,
            help='disable syntax highlighting')
    @version_option(version='0.1.0', prog_name='JSON Cut')
    @click.pass_context
"""


LEFT_JSON = {"side": "left"}
RIGHT_JSON = {"side": "right"}


def test_join():
    @click.command()
    @argument('json_left', type=click.Path(readable=True), required=False)
    @argument('json_right', type=click.Path(readable=True), required=False)
    @option('-k', '--key',
            help='Select the primary key for the left document (JSON Key)')
    @click.pass_context
    def main(ctx, **kwds):

        left = json.load(open(kwds['json_left']))
        if 'side' in left and left.get('side') == 'left':
            click.echo(left)
            return

        right = json.load(open(kwds['json_right']))
        if 'side' in right and right.get('side') == 'right':
            click.echo(right)
            return

        click.echo('Primary Key - Left Side: ' + kwds['key'])

        """
        if rgtkey in 'kwds':
            click.echo('Primary Key - Right Key: ' + kwds['rgtkey'])

        if root in 'kwds':
            click.echo('Root Key - Left Side: ' + kwds['root'])
        click.echo('Root Key - Right Side: ' + kwds['rgtroot'])

        click.echo('Join Type: ' + kwds['join_type'])

        click.echo('Full Scan?: ' + kwds['fullscan'])
        click.echo('JSON Key Quote Character: ' + kwds['quotechar'])
        click.echo('JSON Indentation Size: ' + kwds['indent'])
        click.echo('Use Terminal Colors?: ' + kwds['nocolor'])

        """

    runner = CliRunner()

    with runner.isolated_filesystem():

        left = json.dumps(LEFT_JSON)
        with open('left.json', 'w') as f:
            f.write(left)

        right = json.dumps(RIGHT_JSON)
        with open('right.json', 'w') as f:
            f.write(right)

        empty = json.dumps({})
        with open('empty.json', 'w') as f:
            f.write(empty)

        result = runner.invoke(main, ['left.json', 'empty.json', '--key', '.'])
        assert result.exit_code == 0
        left = result.output.replace("'", '"')
        assert json.loads(left) == {"side": "left"}

        result = runner.invoke(main, ['empty.json', 'right.json',
                               '--key', '.'])
        assert result.exit_code == 0
        right = result.output.replace("'", '"')
        assert json.loads(right) == {"side": "right"}

        result = runner.invoke(main, ['empty.json', 'empty.json',
                               '--key', '.'])
        assert result.exit_code == 0
        assert result.output == 'Primary Key - Left Side: .\n'
