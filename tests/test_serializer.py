import pytest

from roundhouse import serialize, deserialize, get_serializers


@pytest.mark.parametrize('format_', get_serializers().keys())
def test_serialization_cycle(format_):
    """Top-level basic test for comparison of input data to serialized then deserialized output data"""
    input_data = {
        u'example': {
            u'nested': u'valu\u00e9',
            u'key': [1, 2, 3]
        }
    }

    assert input_data == deserialize(serialize(input_data, format_), format_)
