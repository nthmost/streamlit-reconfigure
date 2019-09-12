from unittest import TestCase

from slreconfig.clickload import generate_options, OPTION_TMPL, load_defaults

#FIXTURES, as it were
testd = {'tron':  {'legacy': 'soundtrack'},
         'marvel': {'Thor': 2, 'captainA': False, 'IronMan': 'Pepper Potts'},
         'cats': {'Minnie': 'grass', 'Spartacus': 'minnows'},
         'karaoke': {'songs': []},
        }


class TestGenerateOptions(TestCase):

    def setUp(self):
        pass

    def test_load_defaults(self):
        defaults = load_defaults()
        assert len(defaults) > 1

    def test_generate_options(self):
        options = generate_options(testd)
        assert len(options) > len(testd)

        all_names = set()
        for topkey in testd.keys():
            for key in testd[topkey]:
                # create the set here with the way they are stored on the Option object
                all_names.add('{}_{}'.format(topkey, key).lower())

        for opt in options:
            assert opt.name in all_names

