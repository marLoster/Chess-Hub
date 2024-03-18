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
    db = connection.DBconnection()

    sql = """
           with white_games as (
            select 
                left(date, 8) as date,
                white,
                sum(cast(winner=-1 as int)) as draws,
                sum(cast(winner=1 as int)) as wins,
                sum(cast(winner=0 as int)) as defeats,
                count(*) as games_played
            from 
                games
            where 1=1 
                and white != black
                and date like %s
            group by
                white,
                left(date, 8)
        ),
         
        black_games as (
            select 
                left(date, 8) as date,
                black,
                sum(cast(winner=-1 as int)) as draws,
                sum(cast(winner=0 as int)) as wins,
                sum(cast(winner=1 as int)) as defeats,
                count(*) as games_played
            from 
                games
            where 1=1 
                and white != black
                and date like %s
            group by
                black,
                left(date, 8)
        )
        
        insert into dwh_bots (id, games_played, wins, defeats, draws, date)
        select 
            coalesce(white, black) as id, 
            coalesce(black_games.games_played, 0) + coalesce(white_games.games_played, 0) as games_played, 
            coalesce(black_games.wins, 0) + coalesce(white_games.wins, 0) as wins, 
            coalesce(black_games.defeats, 0) + coalesce(white_games.defeats, 0) as defeats,  
            coalesce(black_games.draws, 0) + coalesce(white_games.draws, 0) as draws,
            coalesce(white_games.date, black_games.date) as date
        from
            white_games
                full outer join black_games
                    on white=black;
    """

    today = datetime.now()
    yesterday = today - timedelta(days=1)
    current_date = yesterday.strftime("%Y%m%d")
    date_criterion = current_date + "%"

    clear_partition_sql = r"delete from dwh_bots where date=%s;"
    db.execute(clear_partition_sql, [current_date])
    db.execute(sql, [date_criterion, date_criterion])

    update_time = datetime.now().strftime("%Y%m%d%H%M")
    update_sql = "insert into dwh_updates (table_name, date) values ('dwh_bots', %s)"
    db.execute(update_sql, [update_time])


if __name__ == "__main__":
    main()
