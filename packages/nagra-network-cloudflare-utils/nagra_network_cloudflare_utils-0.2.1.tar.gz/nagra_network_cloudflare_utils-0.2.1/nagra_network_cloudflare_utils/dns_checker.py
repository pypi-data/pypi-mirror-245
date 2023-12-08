import csv
import logging
from pathlib import Path

import click

from .schema import check_records, sort_records

log = logging.getLogger('Record checker')


@click.command(
    'check',
    help='Check that the CSV file is compliant with Terraform module',
)
@click.option(
    '-f',
    '--file',
    type=Path,
    help='Name of the file to check',
    default='dns_records.csv',
)
def check_csvfile(file: Path):
    if not file.is_file():
        log.warn('File does not exist. Ignoring validation')
        return
    if file.suffix != '.csv':
        log.warn('File must be a .csv file')
        return
    with open(file) as f:
        check_records(csv.DictReader(f))
    log.info('File {} is valid'.format(file))


@click.command(
    'sort',
    help='Sort the CSV file',
)
@click.option(
    '-f',
    '--file',
    type=Path,
    help='Name of the file to check',
    default='dns_records.csv',
)
def sort_csvfile(file: Path):
    header = ('name', 'type', 'content', 'ttl', 'proxied')
    with open(file) as f:
        records = list(csv.DictReader(f, fieldnames=header))
    records = records[1:]  # Remove header
    records = sort_records(records)
    with open(file, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(records)
