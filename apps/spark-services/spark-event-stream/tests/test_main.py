from event_stream import index


def test_index():
    assert index.hello() == "Hello spark-services-spark-event-stream"
