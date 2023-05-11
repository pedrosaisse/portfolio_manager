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
	where a.class_id = 1 AND country_id = 1
)
SELECT
	lr.ticker,
	sp.close_price,
	a.position,
	(a. "position" * sp.close_price) AS balance,
	(a. "position" * sp.close_price)/ total_value as size,
	0.04 - (((a.position * lr.close_price) / total_value) :: NUMERIC(15,4)) as desired_position_pct,
    (0.04 - (((a.position * lr.close_price) / total_value) :: NUMERIC(15,4))) * total_value as desired_position_value,
    round( ((0.04 - (((a.position * lr.close_price) / total_value) :: NUMERIC(15,4))) * total_value) / lr.close_price) as desired_position_qtt,
	a.average_price,
	(a.position * a.average_price) as average_cost,
    (a.position * lr.close_price) - (a.position * a.average_price) as pnl,
    case when a.position = 0 then 0 else (((a.position * lr.close_price) - (a.position * a.average_price)) / (a.position * a.average_price)) end as pnl_pct
FROM
	last_read lr
	INNER JOIN stock_daily_price sp ON lr.read_date = sp.read_date
		AND lr.ticker = sp.ticker
	INNER JOIN assets a ON lr.ticker = a.ticker
	CROSS JOIN asset_total_value atv
WHERE a.class_id = 1 AND country_id = 1
ORDER BY balance DESC;