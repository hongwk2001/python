import itertools

import pandas as pd
import sqlite3 as sq

def csv_to_db(v_file_path) ->str:
    try:
        df = pd.read_csv(v_file_path)
    except:
        print('could not load csv files with pandas')
        print('please check')
        return

    table_name = "test"  # table and file name

    db_path = '{}.sqlite'.format(table_name)

    conn = sq.connect(db_path)  # creates file
    df.to_sql(table_name, conn, if_exists='replace', index=False)  # writes to file
    conn.close()  # good practice: close connection

    return db_path

from pathlib import Path

def show_data(db_path):
    conn=sq.connect(db_path)
    try:
        table_name=Path(db_path).stem
        df = pd.read_sql( f'select * From {table_name}', conn)
        print(df.head())
    finally:
        conn.close()

def get_col_n_position(column_names,combination):
    list=[]
    for column in combination :
        list.append (f'{column}:{column_names.index(column)+1}')
    results = ",".join(list)
    return results

def find_uniq_combination(db_path)->None:
    conn =sq.connect(db_path)
    try:
        table_name = db_path.rsplit('.')[0]

        total_cnt = get_total_cnt(conn, table_name)

        column_names = get_column_names(conn, table_name)

        pkFound = False

        for i in range ( 1, len(column_names) +1) :
            if i == 11: break  # no more than 10 combination
            for combination in itertools.combinations(column_names, i):
                sql_count_distinct = ("select count(1) from (select distinct "
                                    +", ".join ([str(x) for x in combination])
                                    +f" from  {table_name} )" )

                results = conn.cursor().execute(sql_count_distinct)
                trial_cnt = results.fetchone()[0]

                print ( sql_count_distinct + " : " + str(trial_cnt))

                if total_cnt == trial_cnt :
                    print(f'totoal_cnt {total_cnt} tried count {trial_cnt} is matching. Stopping search')
                    print( "columns and positions " + get_col_n_position(column_names,combination))
                    break

    finally:
        conn.close()


def get_column_names(conn, table_name) -> list:
    # get column names
    sql_select_non = f'select * From {table_name} where 1 =2'
    cursor = conn.cursor().execute(sql_select_non)
    #cursor.execute(sql_select_non)
    return [description[0] for description in cursor.description]


def get_total_cnt(conn, table_name):
    # get total_cnt
    sql_select_total_cnt = f'select count(1) from {table_name}'
    #cursor = conn.cursor()
    results = conn.cursor().execute(sql_select_total_cnt)
    total_cnt = results.fetchone()[0]
    print('total_cnt sql :' + sql_select_total_cnt)
    print('totoal_cnt :' + str(total_cnt))
    return total_cnt


if __name__ == "__main__":
    v_file_path = "testdata.csv"

    # try save to db, when successful it will return db or none
    db_path =  csv_to_db(v_file_path)

    #as test
    if db_path:
        show_data(db_path)

    #only when successfull
    if db_path :
        find_uniq_combination(db_path)
