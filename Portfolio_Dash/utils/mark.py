import numpy as np

np.random.seed(123)



def rand_weights(n):
    k = np.random.rand(n)
    return k / sum(k)


def random_portfolio(returns, x):

    risk_free_rate = 0.002
    
    p = np.asmatrix(np.mean(returns, axis=1))
    w = np.asmatrix(rand_weights(returns.shape[0]))
    C = np.asmatrix(np.cov(returns))

    retorno = 3
    risco = 0.009

    mu = (w * p.T) * retorno

    sigma = np.sqrt(w * C * w.T) * np.sqrt(risco)
    sharpe = (mu - risk_free_rate) / sigma 
    
    return mu, sigma, sharpe


n_assets = 4
n_obs = 1000
x = (0.05, 0.012)
return_vec = np.random.randn(n_assets, n_obs)
n_portfolios = 600
means, stds, sharpe = np.column_stack([
    random_portfolio(return_vec, x) 
    for _ in range(n_portfolios)
])
risco = stds.flatten()
retorno = means.flatten()


title_text = "Risco x Retorno para os portfólios gerados"
title={'text': title_text, 'xanchor': 'center', 'yanchor': 'bottom', 'y':0, 'x':0.5,}

import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')


plt.scatter(risco, retorno)
plt.scatter([x[0]], [x[1]])
plt.show()