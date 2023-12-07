# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.test namespace
"""

import sys as _sys

from tensorflow._api.v2.compat.v1.test import experimental
from tensorflow.python.framework.test_util import TensorFlowTestCase as TestCase # line: 2550
from tensorflow.python.framework.test_util import assert_equal_graph_def_v1 as assert_equal_graph_def # line: 244
from tensorflow.python.framework.test_util import create_local_cluster # line: 4003
from tensorflow.python.framework.test_util import gpu_device_name # line: 170
from tensorflow.python.framework.test_util import is_gpu_available # line: 2060
from tensorflow.python.framework.test_util import with_eager_op_as_function # line: 1290
from tensorflow.python.ops.gradient_checker import compute_gradient # line: 269
from tensorflow.python.ops.gradient_checker import compute_gradient_error # line: 346
from tensorflow.python.platform.benchmark import TensorFlowBenchmark as Benchmark # line: 287
from tensorflow.python.platform.benchmark import benchmark_config # line: 274
from tensorflow.python.platform.googletest import StubOutForTesting # line: 111
from tensorflow.python.platform.test import disable_with_predicate # line: 131
from tensorflow.python.platform.test import get_temp_dir # line: 56
from tensorflow.python.platform.test import is_built_with_cuda # line: 89
from tensorflow.python.platform.test import is_built_with_gpu_support # line: 149
from tensorflow.python.platform.test import is_built_with_rocm # line: 110
from tensorflow.python.platform.test import is_built_with_xla # line: 170
from tensorflow.python.platform.test import main # line: 49
from tensorflow.python.platform.test import mock # line: 40
from tensorflow.python.platform.test import test_src_dir_path # line: 75

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "test", public_apis=None, deprecation=False,
      has_lite=False)
