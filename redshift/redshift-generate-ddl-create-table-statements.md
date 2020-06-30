# Redshift: Generate DDL Create Table Statements

To generate DDL create statements for existing tables in Redshift, load the
[v_generate_tbl_ddl.sql](https://github.com/awslabs/amazon-redshift-utils/blob/master/src/AdminViews/v_generate_tbl_ddl.sql)
from the Amazon Redshift Utilities repository to create a view to do the work,
then select from it.

Create the `admin.v_generate_tbl_ddl` view one time:

- Create an 'admin' schema, if necessary:
  ```sql
  CREATE SCHEMA admin AUTHORIZATION dwadmin;
  ```

- Run the `v_generate_tbl_ddl.sql` script to create the DDL-creating view:
  ```sql
  \i v_generate_tbl_ddl.sql
  ```

Now you can generate DDL for all tables in a schema, or for specific tables:
```sql
SELECT DDL
  FROM admin.v_generate_tbl_ddl
 WHERE schemaname = 'SCHEMA_NAME'
   AND tablename IN ('TABLE_NAME_1', 'TABLE_NAME_2')
```

Be sure to check the comments in the header of the `v_generate_tbl_ddl.sql`
script for more usage tips and constraints.

Thanks to https://discourse.snowplowanalytics.com/t/556
