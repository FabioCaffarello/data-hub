from botstatscollector import (
    statsd_collector,
    dummy_collector
)


STATS_COLLECTORS = {
    "statsd": statsd_collector.StatsDCollector,
    "none": dummy_collector.DummyCollector
}


def new_collector(botname, stats_collector_type):
    return STATS_COLLECTORS[stats_collector_type](botname)
