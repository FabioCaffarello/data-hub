import statsd
from botstatscollector import base


class StatsDCollector(base.AbstractCollector):

    def __init__(self, botname):
        self._client = statsd.StatsClient()
        self._botname_tag = "bot.name={}".format(botname)

    def increment_metric(self, name, tags=None):
        self._client.incr(self.parse_statsd_metric(name, tags))

    def time_metric(self, name, time, tags=None):
        self._client.timing(self.parse_statsd_metric(name, tags), time)

    def parse_statsd_metric(self, metric_name, metric_tags=None):
        if metric_tags is None:
            metric_tags = list()
        if not isinstance(metric_tags, list):
            raise TypeError("tags must be a list")

        parsed_tags = ",".join(metric_tags)
        parsed_tags = "{},{}".format(self._botname_tag, parsed_tags).strip(",")
        return "{metric}#{tags}".format(metric=metric_name, tags=parsed_tags)

