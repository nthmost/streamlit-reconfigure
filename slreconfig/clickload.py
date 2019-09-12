"Supplies the machinery that makes it possible to invent all options at runtime."

import os

import click
import toml

# the shape option names will take when constructed from the config.
OPTION_TMPL = '--{}-{}'   #e.g. --horse-race, --rubber-soul...


def load_defaults():
    "load defaults (dict) from package's included default.toml file in /cfg/."
    config_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cfg')
    return toml.load(os.path.join(config_dir, 'defaults.toml'))


def generate_options(config):
    """Given a config file (dictionary) that is 2 levels deep, generate
    a list of click.Option objects that would allow command-line entry of the 
    items in that dictionary.

    Dictionary values will be used to generate a type for the option, 
    defaulting to TEXT type.

    For example:

        {'tron':  {'legacy': 'soundtrack'},
         'marvel': {'Thor': 2, 'captainA': False, 'IronMan': 'Pepper Potts'},
        }

    Should result in options like this:

        --tron-legacy  TEXT
        --marvel-Thor  INTEGER
        --marvel-captainA   TEXT
        --marvel-IronMan    TEXT
    
    No default values are set for the options.

    :param config: (dict)
    :returns: list of click.Option instances
    :rtype: list 
    """
    opts = []

    for topkey in config.keys():
        for key, val in config[topkey].items():
            # generate an Option based on the type of the existing value.
            opts.append(click.option(OPTION_TMPL.format(topkey, key), type=type(val)))   #, default=val))
    return opts


def configurator_options(func):
    defaults = load_defaults()
    for option in reversed(generate_options(defaults)):
        func = option(func)
    return func



