from datetime import datetime, timedelta
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the parent directory
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

# Append the parent directory to sys.path
sys.path.append(parent_dir)

import database.connection as connection


def main():
    # both objects connect to the same db but, just for fun let's do it as if it were different db.
    input_db = connection.DBconnection()
    output_db = connection.DBconnection()

    sql = """
        select 
            id, 
            white, 
            black, 
            winner, 
            left(date, 8) as date
        from
            games
        where
            date like %s;
    """

    today = datetime.now()
    yesterday = today - timedelta(days=1)
    current_date = yesterday.strftime("%Y%m%d")
    date_criterion = current_date + "%"

    filename = "temp_dwh_games.csv"
    input_db.create_csv(sql, filename, [date_criterion])
    # print("csv_created")

    clear_partition_sql = r"delete from dwh_games where date=%s;"
    output_db.execute(clear_partition_sql, [current_date])
    with open(filename) as f:
        output_db.copy(f, "dwh_games", columns=("id", "white", "black", "winner", "date"), sep=",")

    update_time = datetime.now().strftime("%Y%m%d%H%M")
    update_sql = "insert into dwh_updates (table_name, date) values ('dwh_games', %s)"
    output_db.execute(update_sql, [update_time])
    os.remove(filename)


if __name__ == "__main__":
    main()
