from python import stats

#CAPM
asset_beta = stats.covar(asset_return,market_return) / stats.var(market_return)
market_risk_premium = market_return - risk_free_rate
cost_of_equity = risk_free_rate + asset_beta * market_risk_premium

#WACC
after_tax_cost_of_debt = cost_of_debt * (1 - tax_rate)
equity_weight = total_equity / (total_debt + total_equity)
debt_weight = total_debt / (total_debt + total_equity)
wacc = equity_weight * cost_of_equity + debt_weight * cost_of_debt

#Returns
portfolio_beta = stats.covar(portfolio_return,market_return) / stats.var(market_return)
portfolio_alpha = portfolio_return - (risk_free_rate + portfolio_beta * market_risk_premium)

sharpe_ratio = (portfolio_return - risk_free_rate) / stats.sigma(portfolio_return - risk_free_rate)
treynor_ratio = (portfolio_return - risk_free_rate) / portfolio_beta
