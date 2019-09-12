"Everybody hates utils.py but THIS time it's for a good reason!"

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



