import configparser
import logging
import os

import click
import yaml
from jinja2 import Environment, FileSystemLoader

try:
    from quollio_data_profiler.profilers.lineage_profiler import gen_column_lineage_payload, gen_table_lineage_payload
    from quollio_data_profiler.repository import dbt, qdc, snowflake
except ImportError:
    from profilers.lineage_profiler import gen_column_lineage_payload, gen_table_lineage_payload
    from repository import dbt, qdc, snowflake


logger = logging.getLogger(__name__)


def setup_dbt_profile(snowflake_connections: snowflake.SnowflakeConnectionConfig) -> None:
    connections_json = snowflake_connections.as_dict()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    profile_path = "{cur_dir}/{profile}".format(
        cur_dir=current_dir, profile="profilers/dbt_projects/snowflake_lineage_profiler/profiles.yml"
    )
    template_path = "{cur_dir}/{template}".format(cur_dir=current_dir, template="profilers/templates")
    loader = Environment(loader=(FileSystemLoader(template_path, encoding="utf-8")))
    template = loader.get_template("snowflake_lineage_project.j2")
    profiles_body = template.render(connections_json)
    with open(profile_path, "w") as profiles:
        yaml.dump(yaml.safe_load(profiles_body), profiles, default_flow_style=False, allow_unicode=True)
    return


def snowflake_table_to_table_lineage(
    company_id: str, snowflake_connections: snowflake.SnowflakeConnectionConfig, qdc_client: qdc.QDCExternalAPIClient
) -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    sf_executor = snowflake.SnowflakeQueryExecutor(snowflake_connections, "QUOLLIO_DATA_PROFILER", "PUBLIC")
    results = sf_executor.get_query_results(
        query="""
        SELECT
            *
        FROM
            QUOLLIO_DATA_PROFILER.PUBLIC.TABLE_TO_TABLE_LINEAGE
        """
    )
    update_table_lineage_inputs = gen_table_lineage_payload(
        company_id=company_id,
        endpoint=snowflake_connections.account_id,
        tables=results,
    )

    req_count = 0
    for update_table_lineage_input in update_table_lineage_inputs:
        logger.info(
            "Generating table lineage. downstream: {db} -> {schema} -> {table}".format(
                db=update_table_lineage_input.downstream_database_name,
                schema=update_table_lineage_input.downstream_schema_name,
                table=update_table_lineage_input.downstream_table_name,
            )
        )
        status_code = qdc_client.update_lineage_by_id(
            global_id=update_table_lineage_input.downstream_global_id,
            payload=update_table_lineage_input.upstreams.as_dict(),
        )
        if status_code == 200:
            req_count += 1
    logger.info(f"Generating table lineage is finished. {req_count} lineages are ingested.")
    return


def snowflake_column_to_column_lineage(
    company_id: str, snowflake_connections: snowflake.SnowflakeConnectionConfig, qdc_client: qdc.QDCExternalAPIClient
) -> None:
    sf_executor = snowflake.SnowflakeQueryExecutor(snowflake_connections, "QUOLLIO_DATA_PROFILER", "PUBLIC")
    results = sf_executor.get_query_results(
        query="""
        SELECT
            *
        FROM
            QUOLLIO_DATA_PROFILER.PUBLIC.COLUMN_TO_COLUMN_LINEAGE
        """
    )
    update_column_lineage_inputs = gen_column_lineage_payload(
        company_id=company_id,
        endpoint=snowflake_connections.account_id,
        columns=results,
    )

    req_count = 0
    for update_column_lineage_input in update_column_lineage_inputs:
        logger.info(
            "Generating column lineage. downstream: {db} -> {schema} -> {table} -> {column}".format(
                db=update_column_lineage_input.downstream_database_name,
                schema=update_column_lineage_input.downstream_schema_name,
                table=update_column_lineage_input.downstream_table_name,
                column=update_column_lineage_input.downstream_column_name,
            )
        )
        status_code = qdc_client.update_lineage_by_id(
            global_id=update_column_lineage_input.downstream_global_id,
            payload=update_column_lineage_input.upstreams.as_dict(),
        )
        if status_code == 200:
            req_count += 1
    logger.info(f"Generating column lineage is finished. {req_count} lineages are ingested.")
    return


def execute(
    company_id: str,
    sf_build_view_connections: snowflake.SnowflakeConnectionConfig,
    qdc_client: qdc.QDCExternalAPIClient,
    is_view_build_only: bool,
    sf_query_connections: snowflake.SnowflakeConnectionConfig = None,
) -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    logger.info("Create lineage view")
    setup_dbt_profile(snowflake_connections=sf_build_view_connections)

    dbt_client = dbt.DBTClient()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_path = "{cur_dir}/{profile}".format(
        cur_dir=current_dir, profile="/profilers/dbt_projects/snowflake_lineage_profiler"
    )
    # FIXME: when executing some of the commands, directory changes due to the library bug.
    # https://github.com/dbt-labs/dbt-core/issues/8997
    dbt_client.invoke(cmd="deps", project_dir=project_path, profile_dir=project_path)
    dbt_client.invoke(
        cmd="run", project_dir=".", profile_dir="."
    )  # MEMO: directory was changed when executing dbt deps.

    if is_view_build_only:
        logger.info("Skip ingesting metadata into QDC.")
        return

    logger.info("Generate snowflake table to table lineage.")
    snowflake_table_to_table_lineage(
        company_id=company_id, snowflake_connections=sf_query_connections, qdc_client=qdc_client
    )

    logger.info("Generate snowflake column to column lineage.")
    snowflake_column_to_column_lineage(
        company_id=company_id, snowflake_connections=sf_query_connections, qdc_client=qdc_client
    )

    logger.info("Snowflake lineage profiler is successfully finished.")
    return


@click.group()
def cli():
    pass


@cli.command()
@click.option("--conf-file", type=str)
@click.option("--mode", type=click.Choice(["DEV", "PROD"], case_sensitive=True))
@click.option("--view-build-only", is_flag=True)
def execute_local(conf_file, mode, view_build_only):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    logger.info("Initialize")
    conf = configparser.SafeConfigParser()
    conf.read(conf_file)

    company_id = conf.get(mode, "company_id")

    sf_build_view_connections = snowflake.SnowflakeConnectionConfig(
        account_id=conf.get(mode, "snowflake_account_id"),
        account_role=conf.get(mode, "snowflake_build_view_role"),
        account_user=conf.get(mode, "snowflake_user_name"),
        account_password=conf.get(mode, "snowflake_password"),
        account_warehouse=conf.get(mode, "snowflake_account_warehouse"),
    )

    qdc_client = qdc.QDCExternalAPIClient(
        client_id=conf.get(mode, "qdc_client_id"),
        client_secret=conf.get(mode, "qdc_client_secret"),
        base_url=conf.get(mode, "qdc_api_endpoint"),
    )

    if view_build_only:
        execute(
            company_id=company_id,
            sf_build_view_connections=sf_build_view_connections,
            qdc_client=qdc_client,
            is_view_build_only=view_build_only,
        )
    else:
        sf_query_connections = snowflake.SnowflakeConnectionConfig(
            account_id=conf.get(mode, "snowflake_account_id"),
            account_role=conf.get(mode, "snowflake_execute_query_role"),
            account_user=conf.get(mode, "snowflake_user_name"),
            account_password=conf.get(mode, "snowflake_password"),
            account_warehouse=conf.get(mode, "snowflake_account_warehouse"),
        )
        execute(
            company_id=company_id,
            sf_build_view_connections=sf_build_view_connections,
            qdc_client=qdc_client,
            is_view_build_only=view_build_only,
            sf_query_connections=sf_query_connections,
        )
    logger.info("Snowflake lineage profiler is successfully finished.")
    return


if __name__ == "__main__":
    cli()
