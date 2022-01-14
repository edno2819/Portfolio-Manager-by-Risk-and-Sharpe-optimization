import numpy as np

#pip install chart-studio
#pip install cvxopt

np.random.seed(13)

def rand_weights(n):
    ''' Produces n random weights that sum to 1 '''
    k = np.random.rand(n)
    return k / sum(k)

def random_portfolio(returns):
    p = np.asmatrix(np.mean(returns, axis=1))
    w = np.asmatrix(rand_weights(returns.shape[0]))
    C = np.asmatrix(np.cov(returns))
    
    mu = w * p.T
    sigma = np.sqrt(w * C * w.T)
    
    # This recursion reduces outliers to keep plots pretty
    if sigma > 2:
        return random_portfolio(returns)
    return mu, sigma

def fronteiraEficiente(x):
    ## NUMBER OF ASSETS
    n_assets = 4
    ## NUMBER OF OBSERVATIONS
    n_obs = 1000
    return_vec = np.random.randn(n_assets, n_obs)
    n_portfolios = 500
    retorno, risco = np.column_stack([random_portfolio(return_vec) for _ in range(n_portfolios)])
    risco = [c[0] for c in risco]
    retorno = [c[0] for c in retorno]
    risco.sort(), retorno.sort()
    delta_x = risco[100] - x[0]
    delta_y = retorno[390] - x[1]

    risco = [c - delta_x for c in risco]
    retorno = [c - delta_y for c in retorno]

    return retorno, risco

def fronteiraEficiente_2(port, n):
    values = []
    risco = []
    retorno = []
    for c in range(1000):
        values.append(rand_weights(n))

    for rate in values:
        retorno.append(port.return_portfolio(rate))
        risco.append(port.risk_portfolio(rate))

    return risco, retorno

def fronteiraEficiente_3(x):
    ## NUMBER OF ASSETS
    n_assets = 4
    ## NUMBER OF OBSERVATIONS
    n_obs = 1000
    return_vec = np.random.randn(n_assets, n_obs)
    n_portfolios = 500
    retorno, risco = np.column_stack([random_portfolio(return_vec) for _ in range(n_portfolios)])
    risco = [c[0] for c in risco]
    retorno = [c[0] for c in retorno]
    risco.sort(), retorno.sort()
    delta_x = risco[100] - x[0]
    delta_y = retorno[390] - x[1]

    risco = [c - delta_x for c in risco]
    retorno = [c - delta_y for c in retorno]



# import plotly.graph_objects as go

# risco, retorno = fronteiraEficiente((0.05, 0.09))
# plot.scatter(x= ‘Volatilidade’, y = ‘Retorno’, 

# # fig = go.Figure()
# # fig.add_trace(go.Scatter(
# #     x=risco,
# #     y=retorno,
# #     name='Distribuição dos ativos',
# #     mode="markers"
# # ))
# # fig.show()