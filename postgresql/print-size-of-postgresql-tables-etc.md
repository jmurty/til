# Print size of PostgreSQL tables etc

Print total table size on disk (bytes):
```sql
SELECT pg_total_relation_size('TABLE_NAME');
```

Print total database size on disk (bytes):
```sql
SELECT pg_database_size('DB_NAME');
```

Pretty-print byte values to show human-friendly values in MB, GB, etc with
`pg_size_pretty()`:
```sql
SELECT pg_size_pretty(pg_database_size('DB_NAME'));
```

List a schema's tables in order of size, descending:
```sql
SELECT tablename,
       pg_total_relation_size(tablename::text) AS size,
       pg_size_pretty(pg_total_relation_size(tablename::text)) AS size_pretty
 FROM pg_tables
WHERE schemaname = 'SCHEMA_NAME'
ORDER BY size DESC;
```

See [Database Object Size
Functions](https://www.postgresql.org/docs/9.4/functions-admin.html#FUNCTIONS-ADMIN-DBSIZE)

## What about AWS Redshift?

AWS Redshift does **not** support "Database object size functions" so none of
the above functions will help, instead they will return zero or even non-zero
values without error responses to let you know they are lying to you.

To print DB table sizes in Redshift, use the `table_info.sql` script in [Amazon
Redshift Utilities |
AdminScripts](https://github.com/awslabs/amazon-redshift-utils/tree/master/src/AdminScripts)
with variations suggested by AJ Welch in [How to Find the Size of Tables,
Schemas and Databases in Amazon
Redshift](https://chartio.com/resources/tutorials/how-to-find-the-size-of-tables-schemas-and-databases-in-amazon-redshift/)
