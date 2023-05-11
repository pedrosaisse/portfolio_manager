SELECT date_payment as Date, sum(amount) as Total
from dividends_dates
WHERE country_id = %s AND class_id = %s
AND date_payment <= '2024-12-31'
GROUP BY date_payment
ORDER BY date_payment asc;
