from typing import Optional

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import sql

def __connect(as_dict=False):
    db_con = {
        "host": "database_money", 
        "user":"admin", 
        "password":"pgsadmin", 
        "port":5432, 
        "dbname":"the_money"
    }

    try:
        from portfolio_api.dev.db_config import DB_CONFIG
        db_con = DB_CONFIG
    except:
        pass

    if as_dict:
        db_con.update(
            {"cursor_factory": RealDictCursor}
        )
        
    return psycopg2.connect(**db_con)

def get_data(args: tuple) -> list:
    query = """
        SELECT *
        FROM assets
        WHERE country_id IN (%s)
    """
    
    conn = __connect(as_dict=True)
    cursor = conn.cursor()
    cursor.execute(query, args)
    results = [ i for i in cursor.fetchall()]
    conn.close()
    return results

def insert_data(table_name: str, args):
    if not args:
        raise AttributeError('No elements in the requisition')

    cols = [col for col in args[0].dict().keys()]
    values = []
    
    for elem in args:
        values.append([val for val in elem.dict().values()])
    
    query = sql.SQL(
        """
            INSERT INTO {} ({}) VALUES ({}) 
            ON CONFLICT (ticker, api_request_ticker) DO NOTHING;
        """
    ).format(
        sql.Identifier(table_name),
        sql.SQL(', ').join(map(sql.Identifier, cols)),
        sql.SQL(', ').join(sql.Placeholder() * len(cols))
    )

    conn = __connect()
    cursor = conn.cursor()
    cursor.executemany(query, values)
    conn.commit()
    conn.close()
    return 1


def api_tickers(country_id: int, class_id: int, tickers_ignore: list = []):
    if len(tickers_ignore) > 0:
        print(f'Ignoring tickers {tickers_ignore}')

    select_qry = sql.SQL("""
        SELECT api_request_ticker FROM assets
        WHERE class_id = {cl_id} AND country_id = {ct_id}
            AND ticker NOT IN ({tk_ign})
        GROUP BY api_request_ticker
        ORDER BY api_request_ticker ASC;
    """).format(
        cl_id=sql.Placeholder(),
        ct_id=sql.Placeholder(),
        tk_ign=sql.SQL(',').join(sql.Placeholder() * len(tickers_ignore))
    )
    results = None
    conn = None

    try:
        conn = __connect()
        cur = conn.cursor()
        cur.execute(select_qry, (class_id, country_id, *tickers_ignore))
        
        results = [ i[0] for i in cur.fetchall()]
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()
    
    return results

def insert_quotes(quote_data):
    cols = len(quote_data[0].dict().keys())
    insert_qry = sql.SQL(
        """
            INSERT INTO stock_daily_price 
            VALUES ({}) 
            ON CONFLICT (read_date, ticker) 
            DO NOTHING;
        """
    ).format(
        sql.SQL(',').join(sql.Placeholder() * cols)
    )

    insert_values = []
    for elem in quote_data:
        insert_values.append([val for val in elem.dict().values()])

    conn = None
    try:
        conn = __connect()
        cursor = conn.cursor()
        cursor.executemany(insert_qry, insert_values)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()


def wallet_balance(wallet_id: int, country_id: int, class_id: int):
    select_qry = sql.SQL("""
        WITH last_read AS (
	SELECT 
		p.read_date, p.ticker, p.open_price, 
		p.high_price, p.low_price, close_price, 
		p.volume
	FROM stock_daily_price p
	INNER JOIN (
		SELECT
			max(read_date) AS reading,
			ticker
		FROM stock_daily_price
		GROUP BY ticker
	) last_read
	ON p.ticker = last_read.ticker AND p.read_date = last_read.reading
), 
asset_total_value as (
	SELECT 
		SUM(a.position * lr.close_price) as total_value
	from assets a
	inner join last_read lr
	on lr.ticker = a.ticker
	where a.class_id = %s AND country_id = %s and wallet_id = %s
)
SELECT
	a.company,
	lr.ticker,
	sp.close_price,
	a.position,
	(a. "position" * sp.close_price) AS balance,
	(a. "position" * sp.close_price)/ total_value as size,
	w.ideal_position_size - (((a.position * lr.close_price) / total_value) :: NUMERIC(15,4)) as desired_position_pct,
    (w.ideal_position_size - (((a.position * lr.close_price) / total_value) :: NUMERIC(15,4))) * total_value as desired_position_value,
    case 
		when a.country_id = 1 
		then round( ((w.ideal_position_size - (((a.position * lr.close_price) / total_value) :: NUMERIC(15,4))) * total_value) / lr.close_price)
		else (( ((w.ideal_position_size - (((a.position * lr.close_price) / total_value) :: NUMERIC(15,10))) * total_value) / lr.close_price) :: NUMERIC(15,5))
	end as desired_position_qtt,
	a.average_price,
	(a.position * a.average_price) as average_cost,
    (a.position * lr.close_price) - (a.position * a.average_price) as pnl,
    case when a.position = 0 then 0 else (((a.position * lr.close_price) - (a.position * a.average_price)) / (a.position * a.average_price)) end as pnl_pct,
    lr.read_date
FROM
	last_read lr
	INNER JOIN stock_daily_price sp ON lr.read_date = sp.read_date
		AND lr.ticker = sp.ticker
	INNER JOIN assets a ON lr.ticker = a.ticker
	INNER JOIN wallet w on a.wallet_id = w.id
	CROSS JOIN asset_total_value atv
WHERE a.class_id = %s AND country_id = %s and wallet_id = %s
ORDER BY balance DESC;
    """)
    results = None
    conn = None

    try:
        conn = __connect(as_dict=True)
        cur = conn.cursor()
        cur.execute(select_qry, (class_id, country_id, wallet_id, class_id, country_id, wallet_id))
        
        results = [ i for i in cur.fetchall()]
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()
    
    return results



def dividends_month(country_id, class_id):
    divindends_qry = """
        SELECT to_char(date_payment, 'YYYY-MM') as date_payment, sum(amount) as payment
        FROM dividends_dates
        WHERE country_id = %s AND class_id = %s
        GROUP BY to_char(date_payment, 'YYYY-MM')
        ORDER BY to_char(date_payment, 'YYYY-MM') asc;
    """

    conn = __connect(as_dict=True)
    results = None
    
    try:
        conn = __connect(as_dict=True)
        cur = conn.cursor()
        cur.execute(divindends_qry, (country_id, class_id))
        
        results = [ i for i in cur.fetchall()]
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return results