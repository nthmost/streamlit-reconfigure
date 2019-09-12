import os
import re

import streamlit
import toml

# TOML background
#       https://github.com/uiri/toml/issues/77
# 

DATADIR = './data'

# A portmanteau of "NAN" meaning Not A Number and "Nonsense".
NANSENSE = '!NA!'

buf = open(os.path.join(DATADIR, 'sample_output.raw')).read()
rawconfig = buf[buf.find('[global]'):]


re_commented_out_key = re.compile('^\s?#+\s?(?P<comment>.*?)$')
def comment_to_key(line):
    """ If line looks like a commented-out variable like this:

        #region = 

    ... convert to something like this:

       { "#region": NANSENSE }

    :param line: (str) text
    :return: dictionary with one item if variable found. Empty dictionary if not.
    :rtype: (dict) 
    """
    

def preprocess_raw_config(raw):
    # Convert commented-out options to being set to some NANSENSE that wouldn't
    # be a valid value.  (Don't set to None... we want to make sure
    # these variable names are saved but not misinterpreted as having real values.)
    #
    # TODO: salvage the non-variable comments also?

    #for line in rawconfig.split('\n'):
    #    if line.strip().startswith('#'):
    #        line.
    pass


config = toml.loads(rawconfig, decoder=toml.TomlPreserveCommentDecoder()) 
print(config)

outp = toml.dumps(config, encoder=TomlPreserveCommentEncoder())
print(outp)




