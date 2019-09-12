"Main run point for streamlit-reconfigure, using click to create command line options."

import click

from .clickload import load_defaults, configurator_options
from .gears import *


@click.command()
@configurator_options
@click.pass_context
def main(ctx, **kwargs):
    """Loads current streamlit config, applies any new settings given to click, and 
    generates a new config file with the modified settings."""
    rawconfig = gather_rawconfig()

    # create a config for "internal use only" (contains NANSENSE placeholders)
    config = toml.loads(preprocess_rawconfig(rawconfig))

    # iterate over the config, not the CLI input, because the config is full of
    # weird mixed-case thingies that we need to preserve.
    for topkey in config.keys():
        for key in config[topkey].keys():
            if kwargs.get(key.lower(), None):
                config[key] = kwargs[key]

    # dump (TOML) the new config, then reprocess the output to wash away NANSENSE.
    outp = postprocess_toml_dump(toml.dumps(config))
    print(outp)


@click.command()
def defaults():
    "Prints a config file containing all default values."
    print(load_defaults())

