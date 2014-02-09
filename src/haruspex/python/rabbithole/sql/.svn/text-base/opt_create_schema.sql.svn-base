create table symbol (
  sid Bigint NOT NULL AUTO_INCREMENT,
  symbol varchar(10),
  name varchar(128),
  industry varchar(128),
  exchange varchar(32),
  type varchar(32),
 Primary Key (sid)
) ENGINE = InnoDB;

create table quote (
  sid Bigint NOT NULL AUTO_INCREMENT,
  time timestamp,
  symbol_sid Bigint NOT NULL,
  symbol varchar(10),
  last_price decimal(11,4),
  open_price decimal(11,4),
  prev_close_price decimal(11,4),
  volume int,
  av_10 int,
  pe_ratio decimal(11,4),
  pb_ratio decimal(11,4),
  beta decimal(9,4),
  market_cap bigint,
  ma_200 decimal(11,4),
  ma_50 decimal(11,4),
  ma_21 decimal(11,4),
 Primary Key (sid)
) ENGINE = InnoDB;

create table series (
  sid bigint NOT NULL AUTO_INCREMENT,
  time timestamp,
  market_open bit, -- 'marketOpen'
  symbol_sid bigint not null,
  symbol varchar(10),
  symbol_last_price decimal(11,4),
  series_name varchar(32), -- series 
  series_id varchar(32), -- id
  exp_date_str varchar(32), -- expDate
  exp_date_day int, -- expDay
  exp_date_month int, -- expMonth
  exp_date_year int, -- expYear
  strike_raw int, -- strikePrice
  strike_decimal decimal(9,2), -- strikeString
  in_out varchar(5), --inOut
  call_bid decimal(6,2), -- cbid
  call_ask decimal(6,2), -- cask
  call_last decimal(6,2), -- clast
  call_change decimal(6,2), -- cchange
  call_ask_size int, -- callAskSize
  call_bid_size int, -- callBidSize
  call_volume int, -- cvol
  call_open_interest int, -- coi
  call_delta int, -- cdelt
  call_implied_volatility decimal(6,2), -- civ
  call_theta decimal(8,4), -- cthet
  call_gamma decimal(8,4), -- cgam
  call_vega decimal(8,4), -- cveg
  put_bid decimal(6,2), -- pbid
  put_ask decimal(6,2), -- pask
  put_last decimal(6,2), -- plast
  put_change decimal(6,2), -- pchange
  put_ask_size int, -- putAskSize
  put_bid_size int, -- putBidSize
  put_volume int, -- pvol
  put_open_interest int, -- poi
  put_delta int, -- pdelt
  put_implied_volatility decimal(6,2), -- piv
  put_theta decimal(8,4), -- pthet
  put_gamma decimal(8,4), -- pgam
  put_vega decimal(8,4), -- pveg
 Primary Key (sid)	
) ENGINE = InnoDB;

create table earnings (
  sid Bigint NOT NULL AUTO_INCREMENT,
  symbol_sid Bigint NOT NULL,
  symbol varchar(10),
  date timestamp,
  time varchar(5),
  expected_eps decimal(8,2), 
  actual_eps decimal(8,2),
 Primary Key (sid) 
) ENGINE = InnoDB;