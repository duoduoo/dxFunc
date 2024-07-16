import numpy as np
import rpy2
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri


def rdf2py(in_rdf):
    with (ro.default_converter + pandas2ri.converter).context():
        return ro.conversion.get_conversion().rpy2py(in_rdf)


def py2rdf(in_py):
    with (ro.default_converter + pandas2ri.converter).context():
        return ro.conversion.get_conversion().py2rpy(in_py)


def dict2rlist(in_dict):
    pairs = ro.vectors.ListVector([])
    for k, v in in_dict.items():
        pairs.rx[k] = ro.vectors.StrVector(v)
    return pairs


def is_NA_character_(input_list):
    output_list = []
    for x in input_list:
        output_list.append(type(x) == rpy2.rinterface_lib.sexp.NACharacterType)

    return np.array(output_list, dtype='bool')


def replace_NA_character_(input_df):
    output_df = input_df.copy()
    for i, iList in input_df.iterrows():
        output_df.loc[i, :] = ['NA_character_' if type(x) == rpy2.rinterface_lib.sexp.NACharacterType \
                                   else x for x in iList]

    return output_df
