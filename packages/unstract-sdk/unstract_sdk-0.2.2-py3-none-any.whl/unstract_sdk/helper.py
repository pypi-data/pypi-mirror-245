class SdkHelper:
    def __init__(self) -> None:
        pass

    @classmethod
    def get_platform_base_url(cls, platform_host: str, platform_port: str) -> str:
        """Make base url from host and port.

        Args:
            platform_host (str): _description_
            platform_port (str): _description_

        Returns:
            str: _description_
        """
        if platform_host[-1] == "/":
            return f"{platform_host[:-1]}:{platform_port}"
        return f"{platform_host}:{platform_port}"
