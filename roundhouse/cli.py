# -*- coding: utf-8 -*-

import click

from roundhouse import __version__
from roundhouse.serializer import discover_serializers
from roundhouse.utils import get_file_extension


serializers = discover_serializers()
serializer_formats = list(serializers.keys())
extension_to_format_map = {}

for serializer in serializers.values():
    for ext in serializer.extensions:
        extension_to_format_map[ext] = serializer.format


class ShortChoice(click.Choice):
    """Truncate choices if many options"""

    truncate_after = 3

    def get_metavar(self, param):
        choices = self.choices

        if len(choices) > self.truncate_after:
            choices = choices[:self.truncate_after] + ['...']

        return '[%s]' % '|'.join(choices)


@click.command(context_settings=dict(
    help_option_names=['-h', '--help']
))
@click.version_option(version=__version__)
@click.option(
    '-i',
    '--input-format',
    type=ShortChoice(serializer_formats),
    help='Input format. Inferred from infile extension if not provided'
)
@click.option(
    '-o',
    '--output-format',
    type=ShortChoice(serializer_formats),
    help='Output format. Inferred from outfile extension if not provided'
)
@click.option(
    '-I',
    '--infile',
    type=click.File('r', lazy=True),
    default='-',
    help='Read from file. Defaults to stdin'
)
@click.option(
    '-O',
    '--outfile',
    type=click.File('w', lazy=True),
    default='-',
    help='Write to file. Defaults to stdout'
)
def main(input_format, output_format, infile, outfile):
    """Roundhouse

    Convert many formats to many formats
    """

    if input_format is None:
        if infile.name == '-':
            raise click.BadParameter('Must provide input-format when reading from stdin')

        ext = get_file_extension(infile.name)
        input_format = extension_to_format_map.get(ext)
        if input_format is None:
            raise click.BadParameter((
                'Unable to guess serializer format from extension "{}", '
                'check filename or explicitly provide input-format'
            ).format(ext))

    if output_format is None:
        if outfile.name == '-':
            raise click.BadParameter('Must provide output-format when writing to stdout')

        ext = get_file_extension(outfile.name)
        output_format = extension_to_format_map.get(ext)
        if output_format is None:
            raise click.BadParameter((
                'Unable to guess serializer format from extension "{}", '
                'check filename or explicitly provide output-format'
             ).format(ext))

    input_serializer = serializers[input_format]()
    output_serializer = serializers[output_format]()

    data = input_serializer.deserialize(infile)
    output_serializer.serialize(data, outfile)
