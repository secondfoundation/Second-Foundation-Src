-- first_quote_time
select
  symbol,
  cast(q.time as date) date,
  min(q.time) first_quote_time
from quote q
group by symbol, cast(q.time as date)