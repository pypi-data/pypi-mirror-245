# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.initializers namespace
"""

import sys as _sys

from tensorflow.python.ops.init_ops import Constant as constant # line: 219
from tensorflow.python.ops.init_ops import GlorotNormal as glorot_normal # line: 1627
from tensorflow.python.ops.init_ops import GlorotUniform as glorot_uniform # line: 1595
from tensorflow.python.ops.init_ops import he_normal # line: 1737
from tensorflow.python.ops.init_ops import he_uniform # line: 1762
from tensorflow.python.ops.init_ops import Identity as identity # line: 1555
from tensorflow.python.ops.init_ops import lecun_normal # line: 1682
from tensorflow.python.ops.init_ops import lecun_uniform # line: 1710
from tensorflow.python.ops.init_ops import Ones as ones # line: 182
from tensorflow.python.ops.init_ops import Orthogonal as orthogonal # line: 895
from tensorflow.python.ops.init_ops import RandomNormal as random_normal # line: 487
from tensorflow.python.ops.init_ops import RandomUniform as random_uniform # line: 397
from tensorflow.python.ops.init_ops import TruncatedNormal as truncated_normal # line: 577
from tensorflow.python.ops.init_ops import UniformUnitScaling as uniform_unit_scaling # line: 673
from tensorflow.python.ops.init_ops import VarianceScaling as variance_scaling # line: 741
from tensorflow.python.ops.init_ops import Zeros as zeros # line: 97
from tensorflow.python.ops.lookup_ops import tables_initializer # line: 67
from tensorflow.python.ops.variables import global_variables_initializer as global_variables # line: 1898
from tensorflow.python.ops.variables import local_variables_initializer as local_variables # line: 1925
from tensorflow.python.ops.variables import variables_initializer as variables # line: 1859

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "initializers", public_apis=None, deprecation=False,
      has_lite=False)
