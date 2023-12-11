('Lisscad’s bundled macros.')

# hissp.macros.._macro_.prelude
__import__('builtins').exec(
  ('from functools import partial,reduce\n'
   'from itertools import *;from operator import *\n'
   'def engarde(xs,h,f,/,*a,**kw):\n'
   ' try:return f(*a,**kw)\n'
   ' except xs as e:return h(e)\n'
   'def enter(c,f,/,*a):\n'
   ' with c as C:return f(*a,C)\n'
   "class Ensue(__import__('collections.abc').abc.Generator):\n"
   ' send=lambda s,v:s.g.send(v);throw=lambda s,*x:s.g.throw(*x);F=0;X=();Y=[]\n'
   ' def __init__(s,p):s.p,s.g,s.n=p,s._(s),s.Y\n'
   ' def _(s,k,v=None):\n'
   "  while isinstance(s:=k,__class__) and not setattr(s,'sent',v):\n"
   '   try:k,y=s.p(s),s.Y;v=(yield from y)if s.F or y is s.n else(yield y)\n'
   '   except s.X as e:v=e\n'
   '  return k\n'
   "_macro_=__import__('types').SimpleNamespace()\n"
   "try:exec('from hissp.macros._macro_ import *',vars(_macro_))\n"
   'except ModuleNotFoundError:pass'),
  __import__('builtins').globals())

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda :(
  ('Provide an OpenSCAD-like API with added consistency, safety and convenience.'),
  (lambda * _: _)(
    'lisscad.prelude.._macro_.progn',
    (lambda * _: _)(
      'lisscad.prelude.._macro_.prelude'),
    (lambda * _: _)(
      'builtins..exec',
      "('from lisscad.vocab.base import *')",
      (lambda * _: _)(
        'builtins..globals')),
    (lambda * _: _)(
      'builtins..exec',
      "('from lisscad.app import write')",
      (lambda * _: _)(
        'builtins..globals')),
    (lambda * _: _)(
      'builtins..exec',
      "('from lisscad.data.other import Asset')",
      (lambda * _: _)(
        'builtins..globals')),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'lisscad.prelude..π',
      'math..pi'),
    (lambda * _: _)(
      'builtins..delattr',
      '_macro_',
      (lambda * _: _)(
        'quote',
        'QzPCENT_')),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'lisscad.prelude..QzPCENT_',
      'lisscad.op..background_dict'),
    (lambda * _: _)(
      'builtins..delattr',
      '_macro_',
      (lambda * _: _)(
        'quote',
        'QzHASH_')),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'lisscad.prelude..QzHASH_',
      'lisscad.op..debug_set'),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'lisscad.prelude..QzBANG_',
      'lisscad.vocab.base..root'),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'lisscad.prelude..QzSTAR_',
      'lisscad.op..mul'),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'lisscad.prelude..QzVERT_',
      'lisscad.vocab.base..union'),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'lisscad.prelude..QzET_',
      'lisscad.vocab.base..intersection'),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'lisscad.prelude..QzPLUS_',
      'lisscad.op..add'),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'lisscad.prelude..Qz_',
      'lisscad.op..sub'),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'lisscad.prelude..QzSOL_',
      'lisscad.op..div'),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'lisscad.prelude..first',
      (lambda * _: _)(
        'operator..itemgetter',
        (0))),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'lisscad.prelude..second',
      (lambda * _: _)(
        'operator..itemgetter',
        (1))),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'lisscad.prelude..third',
      (lambda * _: _)(
        'operator..itemgetter',
        (2))),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'lisscad.prelude..QzDOLR_fa',
      partial(
        __import__('lisscad.vocab.base',fromlist='?').special,
        ('$fa'))),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'lisscad.prelude..QzDOLR_fn',
      partial(
        __import__('lisscad.vocab.base',fromlist='?').special,
        ('$fn'))),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'lisscad.prelude..QzDOLR_fs',
      partial(
        __import__('lisscad.vocab.base',fromlist='?').special,
        ('$fs')))))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('Provide an OpenSCAD-like API with added consistency, safety and convenience.')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'standard',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'standard',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda :(
  ('Provide unambiguous aliases in kebab case, traditionally idiomatic for '
   'Lisp.\n'
   '  This is a superset of the standard prelude.'),
  (lambda * _: _)(
    'lisscad.prelude.._macro_.progn',
    (lambda * _: _)(
      'lisscad.prelude.._macro_.standard'),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'lisscad.prelude..callQz_module',
      (lambda * _: _)(
        'lisscad.prelude..QzMaybe_.partial',
        'lisscad.vocab.base..module',
        ':',
        'lisscad.prelude..call',
        True)),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'lisscad.prelude..linearQz_extrude',
      (lambda * _: _)(
        'lisscad.prelude..QzMaybe_.partial',
        'lisscad.vocab.base..extrude',
        ':',
        'lisscad.prelude..rotate',
        False)),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'lisscad.prelude..rotateQz_extrude',
      (lambda * _: _)(
        'lisscad.prelude..QzMaybe_.partial',
        'lisscad.vocab.base..extrude',
        ':',
        'lisscad.prelude..rotate',
        True))))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('Provide unambiguous aliases in kebab case, traditionally idiomatic for '
     'Lisp.\n'
     '  This is a superset of the standard prelude.')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'lisp',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'lisp',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda :(
  ('Patch over parts of the OpenSCAD vocabulary with more literal English.\n'
   '  This is a superset of the lisp prelude.'),
  (lambda * _: _)(
    'lisscad.prelude.._macro_.progn',
    (lambda * _: _)(
      'lisscad.prelude.._macro_.lisp'),
    (lambda * _: _)(
      'builtins..exec',
      "('from lisscad.vocab.english import *')",
      (lambda * _: _)(
        'builtins..globals'))))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('Patch over parts of the OpenSCAD vocabulary with more literal English.\n'
     '  This is a superset of the lisp prelude.')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'english',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'english',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda :(
  ('Provide higher-level utilities only.'),
  (lambda * _: _)(
    'lisscad.prelude.._macro_.progn',
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'lisscad.prelude..slidingQz_hull',
      'lisscad.vocab.util..sliding_hull'),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'lisscad.prelude..radiate',
      'lisscad.vocab.util..radiate'),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'builtins..round',
      'lisscad.vocab.util..round'),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'lisscad.prelude..wafer',
      'lisscad.vocab.util..wafer'),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'lisscad.prelude..QzVERT_map',
      'lisscad.vocab.util..union_map'),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'lisscad.prelude..bilateralQz_symmetryQz_x',
      'lisscad.vocab.util..bilateral_symmetry_x'),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'lisscad.prelude..bilateralQz_symmetryQz_y',
      'lisscad.vocab.util..bilateral_symmetry_y'),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.define',
      'lisscad.prelude..bilateralQz_symmetryQz_xy',
      'lisscad.vocab.util..bilateral_symmetry_xy')))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('Provide higher-level utilities only.')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'util',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'util',
    _QzX3UIMF7Uz_fn))[-1])()

# defmacro
# hissp.macros.._macro_.let
(lambda _QzX3UIMF7Uz_fn=(lambda :(
  ('Provide higher-level utilities with English-language vocabulary.'),
  (lambda * _: _)(
    'lisscad.prelude.._macro_.progn',
    (lambda * _: _)(
      'lisscad.prelude.._macro_.english'),
    (lambda * _: _)(
      'lisscad.prelude.._macro_.util')))[-1]):(
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__doc__',
    ('Provide higher-level utilities with English-language vocabulary.')),
  __import__('builtins').setattr(
    _QzX3UIMF7Uz_fn,
    '__qualname__',
    ('.').join(
      ('_macro_',
       'englishQz_util',))),
  __import__('builtins').setattr(
    __import__('operator').getitem(
      __import__('builtins').globals(),
      '_macro_'),
    'englishQz_util',
    _QzX3UIMF7Uz_fn))[-1])()