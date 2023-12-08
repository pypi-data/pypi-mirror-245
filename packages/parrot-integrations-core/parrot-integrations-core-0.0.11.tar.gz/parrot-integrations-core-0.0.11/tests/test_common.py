import uuid


def test_basic_data_formatter():
    from parrot_integrations.core.common import format_data
    complex_key = str(uuid.uuid4())
    schema = dict(
        complex=dict(path=f'"{complex_key}".val'),
        value=dict(value=True)
    )
    record = {
        complex_key: {
            'val': 1
        }
    }
    formatted = format_data(record=record, schema=schema)
    expected = dict(
        complex=1,
        value=True
    )
    assert formatted == expected