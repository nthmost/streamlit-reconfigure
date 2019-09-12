"Main run point for streamlit-reconfigure, using click to create command line options."

import subprocess
import click

from .clickload import load_defaults, configurator_options
from .gears import *

def gather_rawconfig():
    """Runs `streamlit config show` in shell and returns its output as string.

    :rtype: str
    """
    cmd = 'streamlit config show'
    process = subprocess.run(cmd.split(), check=True, stdout=subprocess.PIPE, universal_newlines=True)
    rawconfig = process.stdout
    return str(rawconfig)


@click.command()
@configurator_options
@click.pass_context
def main(ctx, **kwargs):
    #print('Loading current streamlit config...')
    rawconfig = gather_rawconfig()

    #print('...got it.')

    # create a config for "internal use only" (contains NANSENSE placeholders)
    config = toml.loads(preprocess_rawconfig(rawconfig))

    # rewrite the config using any received user input
    # TODO
    from IPython import embed; embed()

    # dump (TOML) the new config, then reprocess the output to wash away NANSENSE.
    outp = postprocess_toml_dump(toml.dumps(config))
    print(outp)


@click.command()
def defaults():
    "Prints a config file containing all default values."
    print(load_defaults())

