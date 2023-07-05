from crawler import index


def test_index():
    assert index.hello() == "Hello ingestors-base-crawler"
