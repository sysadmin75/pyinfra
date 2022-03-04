import sys
from importlib import import_module

import pkg_resources


if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    # NOTE: this is a stupid workaround
    # See: https://github.com/pyinstaller/pyinstaller/issues/3050
    ALL_CONNECTORS = {
        name: import_module(f'pyinfra.connectors.{name}')
        for name in (
            'ansible',
            'chroot',
            'docker',
            'local',
            'mech',
            'ssh',
            'dockerssh',
            'vagrant',
            'winrm',
        )
    }
else:
    ALL_CONNECTORS = {
        entrypoint.name: entrypoint.load()
        for entrypoint in pkg_resources.iter_entry_points('pyinfra.connectors')
    }


# Connectors that handle execution of pyinfra operations
EXECUTION_CONNECTORS = {
    connector: connector_mod
    for connector, connector_mod in ALL_CONNECTORS.items()
    if getattr(connector_mod, 'EXECUTION_CONNECTOR', False)
}
