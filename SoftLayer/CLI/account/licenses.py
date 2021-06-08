"""Show the all account licenses."""
# :license: MIT, see LICENSE for more details.
import click
from SoftLayer import utils

from SoftLayer.CLI import environment
from SoftLayer.CLI import formatting
from SoftLayer.managers.account import AccountManager


@click.command()
@environment.pass_env
def cli(env):
    """return the control panel and VMWare licenses"""

    manager = AccountManager(env.client)

    panel_control = manager.get_active_virtual_licenses()
    vmwares = manager.get_active_account_licenses()

    table_panel = formatting.KeyValueTable(['id', 'ip_address', 'manufacturer', 'software',
                                            'key', 'subnet', 'subnet notes'])

    table_vmware = formatting.KeyValueTable(['name', 'license_key', 'cpus', 'description',
                                             'manufacturer', 'requiredUser'])
    for panel in panel_control:
        table_panel.add_row([panel.get('id'), panel.get('ipAddress'),
                             utils.lookup(panel, 'softwareDescription', 'manufacturer'),
                             utils.trim_to(utils.lookup(panel, 'softwareDescription', 'longDescription'), 40),
                             panel.get('key'), utils.lookup(panel, 'subnet', 'broadcastAddress'),
                             utils.lookup(panel, 'subnet', 'note')])

    env.fout(table_panel)
    for vmware in vmwares:
        table_vmware.add_row([utils.lookup(vmware, 'softwareDescription', 'name'),
                              vmware.get('key'), vmware.get('capacity'),
                              utils.lookup(vmware, 'billingItem', 'description'),
                              utils.lookup(vmware, 'softwareDescription', 'manufacturer'),
                              utils.lookup(vmware, 'softwareDescription', 'requiredUser')])

    env.fout(table_vmware)
