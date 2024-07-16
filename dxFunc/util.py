import os
import re
import matplotlib.pyplot as plt
import pandas as pd
import json
import ipynbname


def series_flatten(df_series):
    df_out = pd.DataFrame()
    series_name = df_series.name
    for x in df_series:
        df_out = pd.concat([df_out, pd.DataFrame(x)], axis=0)
    df_out.columns = [series_name + '.' + x for x in df_out.columns]
    df_out.index = df_series.index
    return df_out


def load_json_to_df(json_filename):
    with open(json_filename, 'r') as fin:
        df_tmp = pd.json_normalize(json.load(fin))

        # Further edit needed, now specific for GDC metadata json
        df_tmp = df_tmp[[True if len(x) == 1 else False for x in df_tmp['associated_entities']]]
        for feature in df_tmp.columns:
            if isinstance(df_tmp[feature][0], list):
                df_tmp = pd.concat([df_tmp, series_flatten(df_tmp[feature])], axis=1)
                df_tmp = df_tmp.drop(columns=[feature])
    return df_tmp


def get_key(my_dict, val):
    for key, value in my_dict.items():
        if val in value:
            return key
    return "Key not found"


def dict_max_size(input_dict):
    dict_max_size_i = 0
    for x, y in input_dict.items():
        if len(y) > dict_max_size_i:
            dict_max_size_i = len(y)
    return dict_max_size_i


def render(nb=''):
    """Render the current jp notebook
    Example:
        ::

            dxutils.render()

    Args:
        nb:

    Returns:

    """
    if not nb:
        curr_nb_name = ipynbname.name()
        nb = curr_nb_name
    else:
        nb = nb.replace('.ipynb', '')
    os.system('quarto render ' + nb + '.ipynb --to html --quiet')


def save_fig(fn, types=('.pdf', '.png'), bbox_inches='tight', **kwargs):
    """

    Args:
        fn (str):
        types (list):
        bbox_inches (str):
        **kwargs:

    Returns:

    """
    fig = plt.gcf()
    for t in types:
        fig.savefig(fn.replace('.pdf', '').replace('.png', '') + t, bbox_inches=bbox_inches,
                    dpi=500, **kwargs)


def replacenth(string, sub, wanted, n):
    """
    Ref: https://stackoverflow.com/questions/35091557/replace-nth-occurrence-of-substring-in-string

    Args:
        string:
        sub:
        wanted:
        n:

    Returns:

    """
    where = [m.start() for m in re.finditer(sub, string)][n - 1]
    before = string[:where]
    after = string[where:]
    after = after.replace(sub, wanted, 1)
    new_string: str = before + after
    return new_string
