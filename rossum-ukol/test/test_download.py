from data_downloader import get_data


def test_download(mock_requests):
    with open('rossum-ukol/test/res/input.xml') as input:
        result = get_data("1234", "5678")
        assert result == input.read().encode()
        # TODO assert called once
        # TODO basic auth
