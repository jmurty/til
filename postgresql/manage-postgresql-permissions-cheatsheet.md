# Manage PostgreSQL Permissions (Cheatsheet)


## Checks

Check user identity currently and at login (whoami?):
```sql
SELECT current_user, session_user;
```

Change database and user (use `-` as `db_name` for current database):
```sql
\c db_name user_name
```
- Other helpful tips at https://stackoverflow.com/a/50229617/4970
- Redshift only supports a subset, this works:
  `SET SESSION AUTHORIZATION user_name`

List users ("Role name") with permissions ("Attributes": `Superuser`,
`Create DB` etc) and group memberships:
```
\du
```

List schemas, with owner info:
```sql
\dn
```

List databases, with owner and privileges info:
```sql
\l
```

List ownership of tables within a schema:
```sql
-- Use \dt with schema name prefix (don't forget the dot)
\dt schema_name.

-- Equivalent SQL:
SELECT schemaname, tablename, tableowner
  FROM pg_tables WHERE schemaname = 'schema_name';
```

List ACL permissions for tables or views in a schema (compatible with
Redshift):
```sql
SELECT n.nspname AS schema, c.relname AS table, c.relacl AS acl
  FROM pg_class c
  LEFT JOIN pg_namespace n ON c.relnamespace = n.oid
 WHERE
       -- r = ordinary table, v = view, m = materialized view
       c.relkind IN ('r', 'v', 'm')
   AND schema = 'schema_name'
;
```
- "ACL Privilege Abbreviations" to interpret the `acl` column
  https://www.postgresql.org/docs/current/ddl-priv.html#PRIVILEGE-ABBREVS-TABLE
- `pg_class` reference
  https://www.postgresql.org/docs/current/catalog-pg-class.html
- Based on https://stackoverflow.com/a/21178589/4970


## Modifications

Create a group with users:
```sql
CREATE GROUP group_name WITH USER user_name_1, user_name_2;
```

Grant a group read access to a schema and its tables:
```sql
-- Grant the group access to the top-level schema
GRANT USAGE ON SCHEMA schema_name TO GROUP group_name;

-- Grant the group access to one table in the schema
GRANT SELECT ON schema_name.table_name TO GROUP group_name;

-- Grant the group access to ALL tables already in the schema
GRANT SELECT ON ALL TABLES IN SCHEMA schema_name TO GROUP group_name;

-- Grant the group access to FUTURE tables created in the schema
ALTER DEFAULT PRIVILEGES IN SCHEMA schema_name
GRANT SELECT ON TABLES TO GROUP group_name;
```
- Replace `GROUP group_name` with `user_name` to assign to a specific user.
- Use `ALL` (aka `ALL PRIVILEGES`) privilege instead of `USAGE` / `SELECT` to
  grant all privileges.

Change ownership of database:
```sql
ALTER DATABASE db_name OWNER TO user_name;
```

Change owner of table (necessary to permit some table changes that cannot be
permitted with just table-write permissions):
```sql
ALTER TABLE schema_name.table_name OWNER TO user_name;
```

Change table ownership in bulk:

- Create an `EXECUTE` function to simplify ownership changes, from
  https://www.depesz.com/2007/10/19/grantall/
  ```sql
  CREATE FUNCTION EXECUTE(text)
  RETURNS void AS $BODY$BEGIN EXECUTE $1; END;$BODY$ LANGUAGE plpgsql;
  ```
- Dynamically generate and execute `ALTER TABLE` statements:
  ```sql
  SELECT EXECUTE('ALTER TABLE ' || table_name || ' OWNER TO user_name')
    FROM information_schema.tables
   WHERE table_schema = 'public' AND table_catalog = '<DBNAME>';
  ```

## Other references

- Definitions of PostgreSQL privileges like `usage` etc are listed under
  "available privileges" at
  https://www.postgresql.org/docs/current/ddl-priv.html
- https://karloespiritu.github.io/cheatsheets/postgresql/
