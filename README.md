# Streamlit-Reconfigure

This code defines a command-line tool called `streamlit-reconfigure` that ingests 
the output of the streamlit command `streamlit config show`, parses it into a data 
structure via TOML, and allows changes to that data structure via the use of options 
on the command line.

For example:

    streamlit-reconfigure  --server-thing1="red" --server-thing2="blue" --dr-cat="hat"

Of course none of the options in that example will work with streamlit. 
You can see the real options available by typing `streamlit-reconfigure --help`


## How to Get It Going

Clone this repo.  Then navigate into the root of this repo and do:

    python3 -m venv ve
    source ve/bin/activate
    python setup.py develop

If all went well, you should now have the command-line app `streamlit-reconfigure` at
your disposal.

I also made `streamlit-defaults` (another command line tool) that simply prints the 
default values of all of the variables.

Try `streamlit-reconfigure --help` to see all the options you can now configure.

You'll probably want to redirect output to a file when you change the options, like so:

        streamlit-reconfigure --browser-serverPort 8000 > newconfig.toml


## What's Cool About This

None of the options are hard-coded in any way.  Both the names and the expected types are 
dynamically generated by reading the contents of a dumped streamlit config page.

Also, the states of unset, commented-out variables are conserved.  TOML cannot tolerate 
empty values, so there's a workaround in slreconfigure.gears.


## CURRENT ISSUES

* (BUG) Not handling lists correctly.  The output of `streamlit-reconfigure --server-folderWatchBlacklist=['1','2']` is the following very wrong result:

        [server]
        folderWatchBlacklist = [ "[", "1", ",", "2", "]",]
        headless = false
        liveSave = false
        runOnSave = false
        port = 8000
        enableCORS = true

  this also doesn't work:  `streamlit-reconfigure --server-folderWatchBlacklist=1,2`
  nor does this:  `streamlit-reconfigure --server-folderWatchBlacklist="1","2"`

* (bug) CLI options that might indicate an intention to *unset* a variable will not work.  i.e. there is no way to do, say, `streamlit-reconfigure --s3-bucket=None` and have the result be a commented-out variable.
* (story) There should be a way to unset a variable; this is a user interaction feature that needs to be designed.


## Scope Limitations

* Cannot handle config files nested more than 2 deep.  Not hard to do, just not in scope for this one.
* Not responsive to changes in the config that would be evident from `streamlit show config`.  Wouldn't be hard to make it so we check our existing click options against the newly sourced config, and then rewrite the defaults (from which the Click options are sourced) right then and there (and then restart the CLI in a subprocess or something).
* Original comments aren't preserved.  I thought about it, tho.  A little too long.


## Major Dependencies and Their Documentation

* *Python3*: this project was built in Python3.7 but should work in earlier versions of Python 3.
* *streamlit*: **docs coming soon???**
* *toml*:  https://github.com/toml-lang/toml
* *click*:  https://click.palletsprojects.com/en/7.x/

## How to Run the Tests

Run tests for this app with the batch unit test runner of your choice
against the "tests" directory in this repo. Here's what I like to do:

    pip install pytest
    py.test tests/


