import json
import logging

import click
import CloudFlare

log = logging.getLogger('Compliance check')


@click.command('list', help='List Cloudflare Zones')
@click.option(
    '-t',
    '--token',
    type=str,
    # The lib automaticly consider this option
    # envvar="CLOUDFLARE_API_TOKEN",
    help='Cloudflare API token',
)
@click.option(
    '-j',
    '--json',
    'json_format',
    type=str,
    is_flag=True,
    default=False,
    help='Cloudflare API token',
)
def list_zones(token, json_format):
    cf_config = {}
    if token:
        cf_config['token'] = token
    cf = CloudFlare.CloudFlare(**cf_config)
    zones = cf.zones.get()
    if json_format:
        print(json.dumps(zones, indent=4))
    else:
        for z in zones:
            print('{name} (ID: {id})'.format(**z))
