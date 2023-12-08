# %%
from infinitum import main as inf

# %%
# create db connection
host = 'fdo-db-1-prod.cznqvelrikxc.us-east-1.rds.amazonaws.com'
database = 'fdoprod_'
user = 'postgres'
password = '8nfbuc_uFYRa5AL1EmW?EVzY%NE]'

# %%
try:
    schema = 'edison'
    table = 'chat_history'
    cur = conn.cursor()

    cur.execute(
        f"SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = '{schema}' and table_name = '{table}';"
    )

    ans = cur.fetchall()

    coltypes = {desc[0]: desc[1] for desc in ans}
    print(coltypes)
except Exception as e:
    print(e)
    # conn.close()
    # return {"status": 500, "description": str(e)}

# return {"status": 200, "description": "success", "result": coltypes}

# %%
# show all tables and schemas
conn = conn
cur.execute("SELECT table_catalog, table_schema, table_name FROM information_schema.tables;")
ans = cur.fetchall()
print(ans)


# %%
# create
conn = conn
schema = 'test'
table = 'test'
item = {
    'id': '1',
    'name': 'test'
}
res = inf.create_item()

# %%
# read
conn = conn
schema = 'edison'
table = 'chat_history'
item = {
    'id': '1',
    'name': 'test'
}
res = inf.get_item()

# %%
# update
conn = conn
schema = 'test'
table = 'test'
item = {
    'id': '1',
    'name': 'test'
}
res = inf.update_item()

# %%
# delete
conn = conn
schema = 'test'
table = 'test'
item = {
    'id': '1',
    'name': 'test'
}
res = inf.delete_item()

# %%
# list
conn = inf.connect_to_database(host, database, user, password)
schema = 'edison'
table = 'chat'
item = {}
res = inf.get_item(conn, schema, table, item)
# %%
print(res)
# %%
# print(len(res.get('data')))
# %%
