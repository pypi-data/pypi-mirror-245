from cgi import test
from importlib.abc import ResourceLoader
from lib2to3.pytree import convert
import psycopg2
import json

# connect to database
def connect_to_database(host, database, user, password):
    try:
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        return conn
    except Exception as e:
        print(e)

def convert_to_string(item, dtype):
    '''using all known postgres data types'''
    if dtype == "bigint":
        return str(item)
    elif dtype == "boolean":
        return str(item)
    elif dtype == "character varying":
        if item is None:
            return ""
        return item
    elif dtype == "date":
        return f"{item}"
    elif dtype == "double precision":
        return str(item)
    elif dtype == "integer":
        return str(item)
    elif dtype == "numeric":
        return str(item)
    elif dtype == "real":
        return str(item)
    elif dtype == "smallint":
        return str(item)
    elif dtype == "text":
        return f"{item}"
    elif dtype == "timestamp without time zone":
        return f"{item}"
    elif dtype == "timestamp with time zone":
        return f"{item}"
    elif dtype == "time without time zone":
        return f"{item}"
    elif dtype == "time with time zone":
        return f"{item}"
    elif dtype == "uuid":
        return f"{item}"
    # elif dtype == "date":
    #     return item.strftime("%Y-%m-%d")
    else:
        return f"{item}"
    
def show_table(conn, schema, table):
    try:
        cur = conn.cursor()

        cur.execute(
            f"SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = '{schema}' and table_name = '{table}';"
        )

        ans = cur.fetchall()
        print(ans)

        coltypes = {desc[0]: desc[1] for desc in ans}
        print(coltypes)
    except Exception as e:
        print(e)
        conn.close()
        return {"status": 500, "description": str(e)}

    return {"status": 200, "description": "success", "result": coltypes}
        

# create item in table from json object
def create_item(conn, schema, table, item):
    try:
        cur = conn.cursor()

        cur.execute(f"Select * FROM {schema}.{table} LIMIT 0")
        columns = {desc[0]: item.get(desc[0], None) for desc in cur.description}
        print(columns)

        cur.execute(
            f"SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = '{schema}' and table_name = '{table}';"
        )

        ans = cur.fetchall()
        print(ans)

        coltypes = {desc[0]: desc[1] for desc in ans}
        print(coltypes)

        dels = []
        # remove first item from columns
        for item in columns:
            if columns[item] is None:
                dels.append(item)
        
        cur.execute(
            f"""
                select
                    kcu.column_name as key_column
                from information_schema.table_constraints tco
                join information_schema.key_column_usage kcu 
                    on kcu.constraint_name = tco.constraint_name
                    and kcu.constraint_schema = tco.constraint_schema
                    and kcu.constraint_name = tco.constraint_name
                where tco.constraint_type = 'PRIMARY KEY'
                and kcu.table_name = '{table}'
            """
        )

        res = cur.fetchall()

        print(f"PRIMARY KEY: {res}")

        primary_key = res[0][0]
        print(primary_key)
        # drop primary_key from list
        dels.append(primary_key)
        
        print(dels)
        
        for item in dels:
            del columns[item]
        
        insert_strings = {item: f"cast('{columns[item]}' as {coltypes[item]})" for item in columns}
        print(insert_strings)

        # create sql statement
        sql = f"INSERT INTO {schema}.{table} ({', '.join(insert_strings.keys())}) VALUES ({', '.join(insert_strings.values())}) RETURNING *;"
        print(sql)

        cur.execute(sql)

        test = cur.fetchone()

        res = dict(zip([col[0] for col in cur.description], test))
        
        print(res)
        for item in res:
            res[item] = convert_to_string(res[item], coltypes[item])

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(e)
        conn.close()
        return {"status": 500, "description": str(e)}
    
    return {"status": 201, "description": "success", "result": res}

def get_item(conn, schema, table, item):
    try:
        cur = conn.cursor()
        cur.execute(f"Select * FROM {schema}.{table} LIMIT 0")
        columns = {desc[0]: item.get(desc[0], None) for desc in cur.description}
        print(columns)

        id_dict = {item: columns[item] for item in columns if "id" in item}
        print(f'id_dict: {id_dict}')

        # TODO: add optional required IDs for individualized schema config
        # if id_dict['userid'] is None and columns['oidcid'] is None:
        #     return {"status": 400, "description": "user_id is required"}
        # elif id_dict['userid'] is None and id_dict['oidcid'] is not None:
        #     sql = f"select userid from gift_and_note.users where oidcid = '{id_dict['oidcid']}'"
        #     print(sql)
        #     cur.execute(sql)
        #     id_dict['userid'] = cur.fetchone()[0]
        #     # print(id_dict['userid'])
        #     return {"status": 200, "description": "success", "result": id_dict['userid']}

        cur.execute(
            f"SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = '{schema}' and table_name = '{table}';"
        )

        ans = cur.fetchall()
        print(ans)

        coltypes = {desc[0]: desc[1] for desc in ans}
        print(coltypes)

        dels = []
        # remove None items from columns
        for item in id_dict:
            if id_dict[item] is None:
                dels.append(item)
        
        print(dels)
        
        for item in dels:
            del id_dict[item]
        
        id_strings = {item: f"cast('{id_dict[item]}' as {coltypes[item]})" for item in id_dict}
        
        sql = f"SELECT * FROM {schema}.{table} WHERE"
        for item in id_strings:
            sql += f" {item} = {id_strings[item]} AND"
        sql = sql[:-4]
        print(sql)

        cur.execute(sql)
        conn.commit()
        ans = cur.fetchall()
        desc = cur.description
        data = []
        print(ans)
        for item in ans:
            print(f"***** {item}")
            print(desc)
            # Convert all items to string
            res = dict(zip([col[0] for col in desc], item))
            print(res)
            for item in res:
                res[item] = convert_to_string(res[item], coltypes[item])
            data.append(res)
            
        print(data)
        cur.close()
        conn.close()
    except Exception as e:
        print(e)
        conn.close()
        return {"status": 500, "description": str(e)}

    return {"status": 200, "description": "success", "data": data}

def update_item(conn, schema, table, item):
    try:
        cur = conn.cursor()

        cur.execute(f"Select * FROM {schema}.{table} LIMIT 0")
        columns = {desc[0]: item.get(desc[0], None) for desc in cur.description}
        print(columns)

        cur.execute(
            f"SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = '{schema}' and table_name = '{table}';"
        )

        ans = cur.fetchall()
        print(ans)

        coltypes = {desc[0]: desc[1] for desc in ans}
        print(coltypes)

        dels = []
        # remove first item from columns
        for item in columns:
            if columns[item] is None:
                dels.append(item)
        
        print(dels)
        
        for item in dels:
            del columns[item]

        id_dict = {item: columns[item] for item in columns if "id" in item}
        col_list = {item: columns[item] for item in columns if "id" not in item}
        
        insert_strings = {item: f"cast('{col_list[item]}' as {coltypes[item]})" for item in col_list}
        id_strings = {item: f"cast('{id_dict[item]}' as {coltypes[item]})" for item in id_dict}

        # create sql statement
        sql = f"UPDATE {schema}.{table} SET"
        for item in insert_strings:
            sql += f" {item} = {insert_strings[item]},"
        sql = sql[:-1]
        sql += f" WHERE"
        for item in id_strings:
            sql += f" {item} = {id_dict[item]} and"
        sql = sql[:-4]
        sql = sql + " RETURNING *;"
        print(sql)

        cur.execute(sql)

        test = cur.fetchone()

        res = dict(zip([col[0] for col in cur.description], test))
        
        print(res)
        for item in res:
            res[item] = convert_to_string(res[item], coltypes[item])
        
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(e)
        conn.close()
        return {"status": 500, "description": str(e)}
    
    return {"status": 200, "description": "success", "result": res}

def delete_item(conn, schema, table, item):
    try:
        cur = conn.cursor()

        cur.execute(f"Select * FROM {schema}.{table} LIMIT 0")
        columns = {desc[0]: item.get(desc[0], None) for desc in cur.description}
        print(columns)

        cur.execute(
            f"SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = '{schema}' table_name = '{table}';"
        )

        ans = cur.fetchall()
        print(ans)

        coltypes = {desc[0]: desc[1] for desc in ans}
        print(coltypes)

        dels = []
        # remove first item from columns
        for item in columns:
            if columns[item] is None:
                dels.append(item)
        
        print(dels)
        
        for item in dels:
            del columns[item]

        id_dict = {item: columns[item] for item in columns if "id" in item}
        col_list = {item: columns[item] for item in columns if "id" not in item}
        
        insert_strings = {item: f"cast('{col_list[item]}' as {coltypes[item]})" in item for item in col_list}
        id_strings = {item: f"cast('{id_dict[item]}' as {coltypes[item]})" for item in id_dict}

        # create sql statement
        sql = f"DELETE FROM {schema}.{table} WHERE"
        for item in id_strings:
            sql += f" {item} = {id_dict[item]} AND"
        sql = sql[:-4]
        print(sql)

        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(e)
        conn.close()
        return {"status": 500, "description": str(e)}
    
    return {"status": 200, "description": "success"}

if __name__ == "__main__":
    pass