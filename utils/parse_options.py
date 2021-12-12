def _get_options_string(options):
    options_str = "options:"
    suffix_ = ""
    if len(options.keys()) > 1:
        suffix_ = ";"

    for k in options.keys():
        v = options[k]
        options_str += k + "=" + str(v) + suffix_
    return options_str
