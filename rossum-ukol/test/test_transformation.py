from transform import transform


def test_transform():
    with open('rossum-ukol/test/res/input.xml') as input, open('rossum-ukol/test/res/output.xml') as output:
        result = transform(input.read().encode())
        assert result == output.read().encode()
