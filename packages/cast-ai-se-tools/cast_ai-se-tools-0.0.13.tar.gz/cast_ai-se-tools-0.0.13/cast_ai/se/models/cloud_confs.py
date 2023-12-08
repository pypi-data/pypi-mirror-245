from cast_ai.se.services.logging_svc import setup_logging


class AwsConfig:
    def __init__(self, aws_conf: dict, log_level: str):
        self._logger = self._logger = setup_logging(__name__, log_level)
        try:
            self.region = aws_conf["AWS_REGION"]
            self.default_node_group = aws_conf["AWS_DEFAULT_NODE_GROUP"]
            self.access_key = aws_conf["AWS_ACCESS_KEY"]
            self.access_secret_key = aws_conf["AWS_ACCESS_SECRET_KEY"]
        except Exception as e:
            self._logger.critical(f"Was not able to initialize aws config:{str(e)}")
            raise RuntimeError(f"Was not able to initialize aws config:{str(e)}")
