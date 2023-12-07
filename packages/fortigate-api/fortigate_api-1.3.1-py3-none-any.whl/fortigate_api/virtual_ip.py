"""Virtual IP Object."""

from fortigate_api.base import Base


class VirtualIP(Base):
    """Virtual IP Object."""

    def __init__(self, rest):
        """Virtual IP Object.

        ::
            :param rest: Fortigate REST API connector
            :type rest: Fortigate
        """
        super().__init__(rest=rest, url_obj="api/v2/cmdb/firewall/vip/")
