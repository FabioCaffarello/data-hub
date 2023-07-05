import os


def new_from_env():
    return ServiceDiscovery(os.environ)


class ServiceDiscovery():
    def __init__(self, envvars):
        if envvars is None:
            raise UnrecoverableError("envvars can't be None")
        self._vars = envvars

    def _get_endpoint(self, varname, protocol="http"):
        if varname not in self._vars:
            raise ServiceUnavailableError(
                "Unable to find env variable: {}".format(varname)
            )
        tcp_addr = self._vars[varname]
        return tcp_addr.replace("tcp", protocol)

    def rabbitmq_endpoint(self):
        return self._get_endpoint("RABBITMQ_PORT_5672", "amqp")


class UnrecoverableError(Exception):
    pass


class ServiceUnavailableError(Exception):
    pass



