"""Quollio Data Profiler"""

__version__ = "0.1.1"
__author__ = "Quollio technologies"


from quollio_data_profiler.repository.snowflake import SnowflakeConnectionConfig  # noqa:F401
from quollio_data_profiler.snowflake_lineage_profiler import execute  # noqa:F401
