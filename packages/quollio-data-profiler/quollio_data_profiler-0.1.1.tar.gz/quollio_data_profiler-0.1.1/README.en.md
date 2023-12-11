# quollio-data-profiler

# Description
This system collects advanced metadata like table to table lineage or anomaly record and ingests them to QDC.


# Prerequisite
Before you begin to use this, you need to do the following.
- Add your assets to QDC with metadata agent.
- Issue External API client id and client secret on QDC.

# Install
Install with the following command.  
`pip install quollio-data-profiler`

# Usage
Here is an example of creating a view. Please enter any values for <>.  
```
from quollio_data_profiler.repository.qdc import QDCExternalAPIClient
from quollio_data_profiler.repository.snowflake import SnowflakeConnectionConfig
from quollio_data_profiler.snowflake_lineage_profiler import execute


def view_build_only():
    company_id = "<company id issued by quollio.>"
    build_view_connection = SnowflakeConnectionConfig(
            account_id="<Snowflake account id. Please use the same id of metadata agent.>",
            account_role="<Role necessary for creating view in your account>",
            account_user="<user name>",
            account_password="<password>",
            account_warehouse="<compute warehouse>", 
    )
    qdc_client = QDCExternalAPIClient(
        client_id="<client id issued on QDC.>",
        client_secret="<client secret>",
        base_url="<base endpoint>",
    )
    execute(
        company_id=company_id,
        sf_build_view_connections=build_view_connection,
        qdc_client=qdc_client,
        is_view_build_only=True,
    )

if __name__ == "__main__":
    view_build_only()
``` 
Please refer to the scripts in `./examples` for other usages.


# Development
## How to test
### Unittest
1. Run `make test`
