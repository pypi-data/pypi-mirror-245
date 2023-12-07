import logging

from dbt.cli.main import dbtRunner, dbtRunnerResult

logger = logging.getLogger(__name__)


class DBTClient:
    def __init__(self) -> None:
        self.dbt = dbtRunner()

    def invoke(self, cmd: str, project_dir: str, profile_dir: str) -> dbtRunnerResult:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
        req = [cmd, "--project-dir", project_dir, "--profiles-dir", profile_dir]
        res = self.dbt.invoke(req)

        if not res.success:
            logger.error(f"dbt.invoke failed. cmd: {cmd}", res)
            raise Exception(res.result)
        return res
