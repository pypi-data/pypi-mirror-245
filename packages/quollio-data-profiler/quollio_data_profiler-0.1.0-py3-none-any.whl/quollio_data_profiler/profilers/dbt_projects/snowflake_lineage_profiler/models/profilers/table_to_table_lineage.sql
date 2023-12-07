WITH table_lineage_history AS (
	SELECT
		doa.value:"objectName"::varchar AS upstream_table_name
		, doa.value:"objectDomain"::varchar AS upstream_table_domain
		, om.value:"objectName"::varchar AS downstream_table_name
		, om.value:"objectDomain"::varchar AS downstream_table_domain
		, om.value:"columns" AS downstream_table_columns
		, ah.query_start_time AS query_start_time
	FROM
        snowflake.account_usage.access_history as ah
		,lateral flatten (input => ah.DIRECT_OBJECTS_ACCESSED) doa
		,lateral flatten (input => ah.OBJECTS_MODIFIED) om
	WHERE
		doa.value:"objectId" IS NOT NULL
		AND om.value:"objectId" IS NOT NULL
		AND om.value:"objectName" NOT LIKE '%.GE_TMP_%'
		AND om.value:"objectName" NOT LIKE '%.GE_TEMP_%'
		AND doa.value:"objectDomain" = 'Table'
		-- AND ah.query_start_time >= to_timestamp_ltz({start_time_millis}, 3)
		-- AND ah.query_start_time < to_timestamp_ltz({end_time_millis}, 3)
		AND (
			NOT RLIKE (
				upstream_table_name,
				'.*\.FIVETRAN_.*_STAGING\..*',
				'i'
			)
			AND upstream_table_name != downstream_table_name
			AND NOT RLIKE (upstream_table_name, '.*__DBT_TMP$', 'i')
			AND NOT RLIKE (upstream_table_name, '.*\.SEGMENT_.*', 'i')
			AND NOT RLIKE (upstream_table_name, '.*\.STAGING_.*_.*', 'i')
		)
		AND (
			NOT RLIKE (
				downstream_table_name,
				'.*\.FIVETRAN_.*_STAGING\..*',
				'i'
			)
			AND upstream_table_name != downstream_table_name
			AND NOT RLIKE (downstream_table_name, '.*__DBT_TMP$', 'i')
			AND NOT RLIKE (downstream_table_name, '.*\.SEGMENT_.*', 'i')
			AND NOT RLIKE (downstream_table_name, '.*\.STAGING_.*_.*', 'i')
		)
), table_lineage AS (
    SELECT
    	downstream_table_name AS "DOWNSTREAM_TABLE_NAME"
    	, ANY_VALUE (downstream_table_domain) as "DOWNSTREAM_TABLE_DOMAIN"
    	, ARRAY_UNIQUE_AGG (
    		OBJECT_CONSTRUCT (
    			'upstream_object_name',
    			upstream_table_name,
    			'upstream_object_domain',
    			upstream_table_domain
    		)
    	) as "UPSTREAM_TABLES"
    FROM
    	table_lineage_history
    GROUP BY
    	downstream_table_name
), view_lineage_history AS (
    SELECT
       ombd.this:"objectDomain"::varchar downstream_object_domain
       , ombd.this:"objectName"::varchar downstream_object_name
       , doa.value:"objectName"::varchar AS upstream_object_name
       , doa.value:"objectDomain"::varchar AS upstream_object_domain
    FROM
        snowflake.account_usage.access_history ah
        , lateral flatten (input => ah.OBJECT_MODIFIED_BY_DDL) ombd
        , lateral flatten (input => ah.DIRECT_OBJECTS_ACCESSED) doa
    WHERE
        object_modified_by_ddl is not null
        AND ombd.this:"objectId" IS NOT NULL
        AND doa.value:"objectId" IS NOT NULL
        AND doa.value:"objectName" NOT LIKE '%.GE_TMP_%'
        AND doa.value:"objectName" NOT LIKE '%.GE_TEMP_%'
        AND (
    		NOT RLIKE (
    			upstream_object_name,
    			'.*\.FIVETRAN_.*_STAGING\..*',
    			'i'
    		)
    		AND NOT RLIKE (upstream_object_name, '.*__DBT_TMP$', 'i')
    		AND NOT RLIKE (upstream_object_name, '.*\.SEGMENT_.*', 'i')
    		AND NOT RLIKE (upstream_object_name, '.*\.STAGING_.*_.*', 'i')
    	)
), view_lineage AS (
    SELECT
       downstream_object_name
       , downstream_object_domain
       , array_unique_agg (
           object_construct (
               'upstream_object_name'
               , upstream_object_name
               , 'upstream_object_domain'
               , upstream_object_domain
           )
       ) AS upstream_tables
    FROM 
        view_lineage_history
    GROUP BY
        downstream_object_name
        , downstream_object_domain
)
SELECT
    *
FROM
    table_lineage
WHERE
    DOWNSTREAM_TABLE_DOMAIN in ('Table', 'View', 'Materialized view')
UNION
SELECT
    *
FROM
    view_lineage
WHERE
    downstream_object_domain in ('Table', 'View', 'Materialized view')
