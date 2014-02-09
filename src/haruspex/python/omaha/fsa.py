from .. import stats.py

#DuPont Ratios
net_margin = net_income / sales
asset_turnover = sales / total_assets

roa = net_income / total_assets
roa = net_margin * asset_turnover


tax_burden = net_income / pretax_income
interest_burden = pretax_income / ebit
ebit_margin = ebit / sales
leverage_ratio = total_assets / equity
compound_leverage_factor = interest_burden * leverage_ratio

roe = net_income / equity
roe = tax_burden * interest_burden * ebit_margin * asset_turnover * leverage_ratio
roe = tax_burden * roa * compound_leverage_factor

