"Config file extrusion, conversion, processing, and repackaging."

import subprocess
import re
import toml

### A FEW WELL CHOSEN GLOBALS 
#
# A portmanteau of "NAN" meaning Not A Number and "Nonsense".
NANSENSE = '"!NA!"'

# matches any comment that was commented out with a #
re_comment = re.compile('^\s?#+\s?(?P<comment>.*?)$')

# matches any key-val pair (or just a key) that was commented out w/ a #
re_commented_out_key = re.compile('^\s?#+\s?(?:(?P<key>.*)\s?=\s?(?P<val>.*?))?$')

### THAT'S ALL FOR GLOBALS.


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
    Pragmatically speaking, this means non-variable comments will be lost.

    :param raw: (str) streamlit config page 
    :return: rewritten config page
    :rtype: str
    """

    # Convert commented-out options to being set to some NANSENSE that wouldn't
    # be a valid value.  (Don't set to None... we want to make sure
    # these variable names are saved but not misinterpreted as having real values.)
    #
    # Maybe later: try to salvage the non-variable comments also? 

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


def postprocess_toml_dump(dump):
    """ Scrubs output of TOML dump to replace instances of NANSENSE with their
    appropriate representations.

    All key-val pairs found to contain NANSENSE will be converted as a replacement
    line to be a commented-out variable ("key = " if it was unset, or "key = val").
    
    :param dump: (str) output of toml.dumps(config)
    :rtype: str
    """
    lines = dump.split('\n')

    for x in range(0, len(lines)):
        if NANSENSE in lines[x]:
            lines[x] = '#{}'.format(lines[x].replace(NANSENSE, ''))

    return '\n'.join(lines)


def gather_rawconfig():
    """Runs `streamlit config show` in shell and returns its output as string.

    :rtype: str
    """
    cmd = 'streamlit config show'
    process = subprocess.run(cmd.split(), check=True, stdout=subprocess.PIPE, universal_newlines=True)
    rawconfig = process.stdout
    return str(rawconfig)



