"Supplies the machinery that makes it possible to invent all options at runtime."

import click

OPTION_TMPL = '--{}-{}'

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

    Values are assumed to be defaults and loaded into the Options as such.

    :param config: (dict)
    :returns: list of click.Option instances
    :rtype: list 
    """
    opts = []

    for topkey in config.keys():
        for key, val in config[topkey].items():
            # generate an Option based on the type of the existing value.
            # (janky, perhaps? we'll see)
            opts.append(click.Option([OPTION_TMPL.format(topkey, key)], type=type(val), default=val))
    return opts

