# -*- coding: utf-8 -*-
"""
    pygments.lexers.matlab
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for Matlab and related languages.

    :copyright: Copyright 2006-2017 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re

from pygments.lexer import Lexer, RegexLexer, bygroups, words, do_insertions
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation, Generic, Whitespace

from pygments.lexers import _scilab_builtins

__all__ = ['MatlabLexer']


class MatlabLexer(RegexLexer):
    """
    For Matlab source code.

    .. versionadded:: 0.10
    """
    name = 'Matlab'
    aliases = ['matlab']
    filenames = ['*.m']
    mimetypes = ['text/matlab']

    #
    # These lists are generated automatically.
    # Run the following in bash shell:
    #
    # for f in elfun specfun elmat; do
    #   echo -n "$f = "
    #   matlab -nojvm -r "help $f;exit;" | perl -ne \
    #   'push(@c,$1) if /^    (\w+)\s+-/; END {print q{["}.join(q{","},@c).qq{"]\n};}'
    # done
    #
    # elfun: Elementary math functions
    # specfun: Special Math functions
    # elmat: Elementary matrices and matrix manipulation
    #
    # taken from Matlab version 7.4.0.336 (R2007a)
    #
    elfun = ("sin", "sind", "sinh", "asin", "asind", "asinh", "cos", "cosd", "cosh",
             "acos", "acosd", "acosh", "tan", "tand", "tanh", "atan", "atand", "atan2",
             "atanh", "sec", "secd", "sech", "asec", "asecd", "asech", "csc", "cscd",
             "csch", "acsc", "acscd", "acsch", "cot", "cotd", "coth", "acot", "acotd",
             "acoth", "hypot", "exp", "expm1", "log", "log1p", "log10", "log2", "pow2",
             "realpow", "reallog", "realsqrt", "sqrt", "nthroot", "nextpow2", "abs",
             "angle", "complex", "conj", "imag", "real", "unwrap", "isreal", "cplxpair",
             "fix", "floor", "ceil", "round", "mod", "rem", "sign")
    specfun = ("airy", "besselj", "bessely", "besselh", "besseli", "besselk", "beta",
               "betainc", "betaln", "ellipj", "ellipke", "erf", "erfc", "erfcx",
               "erfinv", "expint", "gamma", "gammainc", "gammaln", "psi", "legendre",
               "cross", "dot", "factor", "isprime", "primes", "gcd", "lcm", "rat",
               "rats", "perms", "nchoosek", "factorial", "cart2sph", "cart2pol",
               "pol2cart", "sph2cart", "hsv2rgb", "rgb2hsv")
    elmat = ("zeros", "ones", "eye", "repmat", "rand", "randn", "linspace", "logspace",
             "freqspace", "meshgrid", "accumarray", "size", "length", "ndims", "numel",
             "disp", "isempty", "isequal", "isequalwithequalnans", "cat", "reshape",
             "diag", "blkdiag", "tril", "triu", "fliplr", "flipud", "flipdim", "rot90",
             "find", "end", "sub2ind", "ind2sub", "bsxfun", "ndgrid", "permute",
             "ipermute", "shiftdim", "circshift", "squeeze", "isscalar", "isvector",
             "ans", "eps", "realmax", "realmin", "pi", "i", "inf", "nan", "isnan",
             "isinf", "isfinite", "j", "why", "compan", "gallery", "hadamard", "hankel",
             "hilb", "invhilb", "magic", "pascal", "rosser", "toeplitz", "vander",
             "wilkinson")

    tokens = {
        'root': [
            # line starting with '!' is sent as a system command.  not sure what
            # label to use...
            (r'^!.*', String.Other),
            (r'%\{\s*\n', Comment.Multiline, 'blockcomment'),
            (r'%.*$', Comment),
            (r'^\s*function', Keyword, 'deffunc'),

            # from 'iskeyword' on version 7.11 (R2010):
            (words((
                'break', 'case', 'catch', 'classdef', 'continue', 'else', 'elseif',
                'end', 'enumerated', 'events', 'for', 'function', 'global', 'if',
                'methods', 'otherwise', 'parfor', 'persistent', 'properties',
                'return', 'spmd', 'switch', 'try', 'while'), suffix=r'\b'),
             Keyword),

            ("(" + "|".join(elfun + specfun + elmat) + r')\b',  Name.Builtin),

            # line continuation with following comment:
            (r'\.\.\..*$', Comment),

            # operators:
            (r'-|==|~=|<|>|<=|>=|&&|&|~|\|\|?', Operator),
            # operators requiring escape for re:
            (r'\.\*|\*|\+|\.\^|\.\\|\.\/|\/|\\', Operator),

            # punctuation:
            (r'\[|\]|\(|\)|\{|\}|:|@|\.|,', Punctuation),
            (r'=|:|;', Punctuation),

            # quote can be transpose, instead of string:
            # (not great, but handles common cases...)
            (r'(?<=[\w)\].])\'+', Operator),

            (r'(\d+\.\d*|\d*\.\d+)([eEf][+-]?[0-9]+)?', Number.Float),
            (r'\d+[eEf][+-]?[0-9]+', Number.Float),
            (r'\d+', Number.Integer),

            (r'(?<![\w)\].])\'', String, 'string'),
            (r'[a-zA-Z_]\w*', Name),
            (r'.', Text),
        ],
        'string': [
            (r'[^\']*\'', String, '#pop')
        ],
        'blockcomment': [
            (r'^\s*%\}', Comment.Multiline, '#pop'),
            (r'^.*\n', Comment.Multiline),
            (r'.', Comment.Multiline),
        ],
        'deffunc': [
            (r'(\s*)(?:(.+)(\s*)(=)(\s*))?(.+)(\()(.*)(\))(\s*)',
             bygroups(Whitespace, Text, Whitespace, Punctuation,
                      Whitespace, Name.Function, Punctuation, Text,
                      Punctuation, Whitespace), '#pop'),
            # function with no args
            (r'(\s*)([a-zA-Z_]\w*)', bygroups(Text, Name.Function), '#pop'),
        ],
    }
