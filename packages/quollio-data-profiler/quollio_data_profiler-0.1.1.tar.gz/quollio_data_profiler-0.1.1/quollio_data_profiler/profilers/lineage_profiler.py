import json
from dataclasses import asdict, dataclass
from typing import Dict, List

try:
    from quollio_data_profiler.core.core import new_global_id
except ImportError:
    from core.core import new_global_id


@dataclass
class LineageInput:
    upstream: List[str]

    def as_dict(self) -> Dict[str, str]:
        return asdict(self)


@dataclass
class LineageInputs:
    downstream_global_id: str
    downstream_database_name: str
    downstream_schema_name: str
    downstream_table_name: str
    downstream_column_name: str
    upstreams: LineageInput


def gen_table_lineage_payload(company_id: str, endpoint: str, tables: List[Dict[str, str]]) -> List[LineageInputs]:
    payload = list()
    for table in tables:
        downstream_table_fqdn = table["DOWNSTREAM_TABLE_NAME"].split(".")
        if len(downstream_table_fqdn) != 3:
            continue
        else:
            global_id_arg = "{db}{schema}{table}".format(
                db=downstream_table_fqdn[0], schema=downstream_table_fqdn[1], table=downstream_table_fqdn[2]
            )
            downstream_table_global_id = new_global_id(
                company_id=company_id, cluster_id=endpoint, data_id=global_id_arg, data_type="table"
            )
            upstream_tables: List[Dict[str, str]] = json.loads(table["UPSTREAM_TABLES"])
            lineage_input = LineageInput(upstream=[])
            for upstream_table in upstream_tables:
                upstream_table_fqdn = upstream_table["upstream_object_name"].split(".")
                if len(upstream_table_fqdn) != 3:
                    continue
                else:
                    upstream_global_id_arg = "{db}{schema}{table}".format(
                        db=upstream_table_fqdn[0], schema=upstream_table_fqdn[1], table=upstream_table_fqdn[2]
                    )
                    upstream_table_global_id = new_global_id(
                        company_id=company_id, cluster_id=endpoint, data_id=upstream_global_id_arg, data_type="table"
                    )
                    lineage_input.upstream.append(upstream_table_global_id)
            lineage_inputs = LineageInputs(
                downstream_global_id=downstream_table_global_id,
                downstream_database_name=downstream_table_fqdn[0],
                downstream_schema_name=downstream_table_fqdn[1],
                downstream_table_name=downstream_table_fqdn[2],
                downstream_column_name="",
                upstreams=lineage_input,
            )
            payload.append(lineage_inputs)
    return payload


def gen_column_lineage_payload(company_id: str, endpoint: str, columns: List[Dict[str, str]]) -> List[LineageInputs]:
    payload = list()
    for column in columns:
        downstream_table_fqdn = column["DOWNSTREAM_TABLE_NAME"].split(".")
        if len(downstream_table_fqdn) != 3:
            continue
        else:
            global_id_arg = "{db}{schema}{table}{column}".format(
                db=downstream_table_fqdn[0],
                schema=downstream_table_fqdn[1],
                table=downstream_table_fqdn[2],
                column=column["DOWNSTREAM_COLUMN_NAME"],
            )
            downstream_column_global_id = new_global_id(
                company_id=company_id, cluster_id=endpoint, data_id=global_id_arg, data_type="column"
            )
            upstream_columns: List[Dict[str, str]] = json.loads(column["UPSTREAM_COLUMNS"])
            lineage_input = LineageInput(upstream=[])
            for upstream_column in upstream_columns:
                upstream_table_fqdn = upstream_column["upstream_table_name"].split(".")
                if len(upstream_table_fqdn) != 3:
                    continue
                elif not upstream_column.get("upstream_column_name"):
                    continue
                else:
                    upstream_global_id_arg = "{db}{schema}{table}{column}".format(
                        db=upstream_table_fqdn[0],
                        schema=upstream_table_fqdn[1],
                        table=upstream_table_fqdn[2],
                        column=upstream_column["upstream_column_name"],
                    )
                    upstream_column_global_id = new_global_id(
                        company_id=company_id, cluster_id=endpoint, data_id=upstream_global_id_arg, data_type="column"
                    )
                    lineage_input.upstream.append(upstream_column_global_id)
            lineage_inputs = LineageInputs(
                downstream_global_id=downstream_column_global_id,
                downstream_database_name=downstream_table_fqdn[0],
                downstream_schema_name=downstream_table_fqdn[1],
                downstream_table_name=downstream_table_fqdn[2],
                downstream_column_name=column["DOWNSTREAM_COLUMN_NAME"],
                upstreams=lineage_input,
            )
            payload.append(lineage_inputs)
    return payload
