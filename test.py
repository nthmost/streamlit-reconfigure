import subprocess 
import re
import os

import toml   # .loads, .dumps

# TOML: background on the possibility of preserving comments as a decoder/encoder...
#       https://github.com/uiri/toml/issues/77
# 
# In July 2019, such a feature was merged in, a TomlPreserveCommentDecoder.
#
# https://github.com/uiri/toml/commit/3a169c68cbe98b3d32f96c3ec09422600473bddf
#
# The last pypi release of toml was in 2018, so this new feature isn't anywhere
# near stable.
#
#   I tried it; it didn't work. Possibly it can be patched, but who knows whether
#   that's a worthy use of my time?  I couldn't patch-fix it in 5 minutes, so...  -nm
#
# Also useless: some code in the official release that purports to do Ordered dicts.
#    from toml.ordered import TomlOrderedDecoder, TomlOrderedEncoder
#
#   ^^ Using TomlOrderedDecoder just errored out immediately and i was just totally bored.
 

DATADIR = './data'

# A portmanteau of "NAN" meaning Not A Number and "Nonsense".
NANSENSE = '"!NA!"'

# matches any comment that was commented out with a #
re_comment = re.compile('^\s?#+\s?(?P<comment>.*?)$')

# matches any key-val pair (or just a key) that was commented out w/ a #
re_commented_out_key = re.compile('^\s?#+\s?(?:(?P<key>.*)\s?=\s?(?P<val>.*?))?$')

#
# End globals, 4eva 
#### 


def comment_to_key(line):
    """ If line looks like a commented-out variable like this...

        #region = something

    ...convert to something like this:

        region = "something NANSENSE"

    (NANSENSE is a global defined as a noisy, unique string, like "!NAN!")

    :param line: (str) text
    :return: 'key = val' or empty string if no match.
    :rtype: (dict) 
    """
    tmpl = '{key} = {val} {tag}'
    match = re_commented_out_key.match(line)
    if match:
        return tmpl.format(tag=NANSENSE, **match.groupdict())
    return ''
    

def preprocess_rawconfig(raw):
    """ Preprocessing before TOML parsing that preserves commented-out
    variables and removes any breaking text (e.g. the top text output
    when you do `streamlit config show`).

    Lines found to contain variables are rewritten as non-comments per
    the heuristic in the function comment_to_key.  This is a transition
    move to allow us to learn that a variable can be named here, but 
    that it was commented out and (probably) unset.

    Commented-out lines not found to contain variables are untouched.

    :param raw: (str) streamlit config page 
    :return: rewritten config page
    :rtype: str
    """

    # Convert commented-out options to being set to some NANSENSE that wouldn't
    # be a valid value.  (Don't set to None... we want to make sure
    # these variable names are saved but not misinterpreted as having real values.)
    #
    # TODO: figure out (or ask A.) if None is a value or if None == unset.
    #
    # TODO: salvage the non-variable comments also? 

    # make sure the top-text from `stream config show` isn't there.
    raw = raw[raw.find('[global]'):]

    # scan for #-comment lines and replace (if vars) or drop (if plain comment).
    lines = raw.split('\n')
    for x in range(0, len(lines)):
        if lines[x].strip().startswith('#'):
            item = comment_to_key(lines[x])
            if item:
                lines[x] = '{}'.format(item)

    return '\n'.join(lines)


def rewrite_config(config):
    #DEMOLITION?
    """Recursive function that rewrites any values that the supplied dictionary
    contains that have NANSENSE (a tag)."""

    for key in config.keys():
        if type(config[key]) is dict:
            print(key, 'contains multitudes')
            rewrite_config(config[key])
        else:
            if type(config[key]) is str and NANSENSE in config[key]:
                config['#'+key] = config[key].replace(NANSENSE, '')
                print('removed !NAN!:', key, config[key])
    return 0


def postprocess_toml_dump(dump):
    """ The opposite of preprocess_rawconfig, kinda, except we're not recovering
    the original non-variable comments (not this time around...).

    All key-val pairs found to contain NANSENSE will be converted as a replacement
    line to be a commented-out variable ("key = " if it was unset, or "key = val").
    
    :param dump: (str)
    :rtype: str
    """
    lines = dump.split('\n')

    for x in range(0, len(lines)):
        if NANSENSE in lines[x]:
            lines[x] = '#{}'.format(lines[x].replace(NANSENSE, ''))

    return '\n'.join(lines)




if __name__ == '__main__':
    # get the output of `streamlit config show`
    cmd = 'streamlit config show'

    import subprocess

    process = subprocess.run(cmd.split(), check=True, stdout=subprocess.PIPE, universal_newlines=True)
    rawconfig = process.stdout

    # if you wanna READ FROM FILE INSTEAD
    #rawconfig = open(os.path.join(DATADIR, 'sample_output.raw')).read()

    config = toml.loads(preprocess_rawconfig(str(rawconfig)))   #, decoder=TomlOrderedDecoder)
    #print(config)

    outp = postprocess_toml_dump(toml.dumps(config))
    print(outp)
    #print(outp)


