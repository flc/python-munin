from munin.redis import MuninRedisPlugin


class MuninRedisDBPlugin(MuninRedisPlugin):
    title = "Redis %(db_name)s"
    args = "--base 1000"
    vlabel = "num"
    info = "%(db_name)s"
    fields = (
        ('%(db_name)s_keys', dict(
            label = "%(db_name)s_keys",
            info = "%(db_name)s_keys",
            type = "GAUGE",
        )),
        ('%(db_name)s_expires', dict(
            label = "%(db_name)s_expires",
            info = "%(db_name)s_expires",
            type = "GAUGE",
        )),
    )

    def get_config(self):
        conf = super(MuninRedisDBPlugin, self).get_config()
        return [c % {'db_name': self.db_name} for c in conf]

    def execute(self):
        stats = self.get_info()
        r_values = stats.get(self.db_name, None)
        values = []
        if r_values is not None:
            values = [v.split("=")[1] for v in r_values.split(",")]
        ret_values = {}
        for index, (k, v) in enumerate(self.fields):
            try:
                value = values[index]
            except IndexError:
                value = "U"
            ret_values[k % {'db_name': self.db_name}] = value
        return ret_values
