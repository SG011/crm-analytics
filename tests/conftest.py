import sys
from unittest.mock import MagicMock

# PyFlink does not support Python 3.13. Mock the module so unit tests
# can exercise aggregation logic without a running Flink cluster.
if "pyflink" not in sys.modules:
    pyflink_mock = MagicMock()

    class _AggregateFunction:
        pass

    pyflink_mock.datastream.functions.AggregateFunction = _AggregateFunction
    sys.modules["pyflink"] = pyflink_mock
    sys.modules["pyflink.datastream"] = pyflink_mock.datastream
    sys.modules["pyflink.datastream.functions"] = pyflink_mock.datastream.functions
