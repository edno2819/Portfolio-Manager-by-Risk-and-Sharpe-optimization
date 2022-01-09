from utils.math_calculate import *
import plotly.graph_objects as go
from utils.variaveis import QTD_RETORNO_PERIODICO
from utils.fronterEficiente import fronteiraEficiente




class GraphPort:
    def __init__(self, port, taxas_assets, taxas_dict, port_comp={}) -> None:
        self.port = port
        self.CHART_THEME = 'plotly_dark'  # others include seaborn, ggplot2, plotly_dark
        self.taxas_assets = taxas_assets
        self.taxas_dict = taxas_dict
        self.port_comp = port_comp


    def chart_to_portfolio_return_porcent(self, taxas):
        def calculate_return_portfolio(taxas):
            '''Calculando o crescimento em porcentagem em relação ao intervalo anterior'''
            porcent = self.port.taxas_to_dict(taxas)
            result = [0]
            for c in range(self.port.data_range-1):
                count = 0
                for asset in porcent.keys(): 
                    if len(self.port.port_porcent[asset])>=c+1:
                        count += porcent[asset] * self.port.port_porcent[asset][c]
                result.append(count)
            return result

        # with plt.style.context('Solarize_Light2'):
        #     values = calculate_return_portfolio(taxas)  
        #     for c in range(len(self.port.keys())): 
        #         asset = list(self.port.keys())[c]
        #         value_asset = round(taxas[c]*100,2)
        #         if value_asset>=0.01:
        #             plt.plot(self.dates_range[0], [min(values)], label=f'{asset}: {value_asset}%')


    def chart_to_portfolio_return_porcent_2(self, taxas):
        def calculate_return_portfolio(taxas):
            '''Calculando o crescimento em porcentagem em relação ao intervalo anterior'''
            porcent = self.port.taxas_to_dict(taxas)
            result = [0]
            for c in range(self.port.data_range-1):
                count = 0
                for asset in porcent.keys(): 
                    if len(self.port.port[asset])>=c+1:
                        data_to_porcent = [0]
                        data_to_porcent += datas_to_porcent_init(self.port.port[asset])
                        count += porcent[asset] * data_to_porcent[c]
                result.append(count)
            return result


        # with plt.style.context('Solarize_Light2'):
        #     values = calculate_return_portfolio(taxas)  
        #     for c in range(len(self.port.keys())): 
        #         asset = list(self.port.keys())[c]
        #         value_asset = round(taxas[c]*100,2)
        #         if value_asset>=0.01:
        #             plt.plot(self.dates_range[0], [min(values)], label=f'{asset}: {value_asset}%')

        #     plt.plot(self.dates_range, values)
        #     plt.title(f'Taxa de Variação - {self.interval}')
        #     plt.legend(loc="upper left")
        #     plt.xlabel('Periodo', fontsize=14)
        #     plt.ylabel('Porcentagem', fontsize=14)
        #     plt.xticks(rotation=105)
        #     plt.show()


    def chart_to_portfolio(self):
        fig = go.Figure() 
        for asset in self.port.port.keys():   
            fig.add_trace(go.Scatter(x=self.port.assets_dates[asset], y=self.port.port[asset],
                                mode="lines",  # you can also use "lines+markers", or just "markers"
                                name=asset))
        fig.layout.template = self.CHART_THEME
        fig.layout.height=500
        fig.update_layout(margin = dict(t=50, b=50, l=25, r=25))  
        fig.update_layout(
        #     title='Global Portfolio Value (USD $)',
            xaxis_tickfont_size=12,
            yaxis=dict(
                title='Value: $ USD',
                titlefont_size=14,
                tickfont_size=12,
                ))

        return fig


    def circle_chart_portifolio(self):
        lis = []
        name_lis = []
        for asset in self.taxas_dict.keys():
            if self.taxas_dict[asset]>0.01:
                lis.append(self.taxas_dict[asset])
                name_lis.append(asset)

        fig = go.Figure()
        fig.layout.template = self.CHART_THEME
        fig.add_trace(go.Pie(labels=name_lis, values=lis))
        fig.update_traces(hole=.7, hoverinfo="label+value+percent")
        fig.update_traces(textposition='outside', textinfo='label+value')
        fig.update_layout(showlegend=False)
        fig.update_layout(margin = dict(t=50, b=50, l=25, r=25))
        return fig


    def indicatorPeriod(self):
        fig = go.Figure()
        fig.layout.template = self.CHART_THEME
        fig.add_trace(go.Indicator(
            mode = "number+delta",
            value = 7,
            number = {'suffix': " %"},
            title = {"text": "<br><span style='font-size:0.7em;color:gray'>7 Days</span>"},
            delta = {'position': "bottom", 'reference': 2, 'relative': False},
            domain = {'row': 0, 'column': 0}))

        fig.add_trace(go.Indicator(
            mode = "number+delta",
            value = -3,
            number = {'suffix': " %"},
            title = {"text": "<span style='font-size:0.7em;color:gray'>15 Days</span>"},
            delta = {'position': "bottom", 'reference': 3, 'relative': False},
            domain = {'row': 1, 'column': 0}))

        fig.add_trace(go.Indicator(
            mode = "number+delta",
            value = 4,
            number = {'suffix': " %"},
            title = {"text": "<span style='font-size:0.7em;color:gray'>30 Days</span>"},
            delta = {'position': "bottom", 'reference': -2, 'relative': False},
            domain = {'row': 2, 'column': 0}))

        fig.update_layout(
            grid = {'rows': 4, 'columns': 1, 'pattern': "independent"},
            margin=dict(l=50, r=50, t=30, b=30)
        )
        return fig
    

    def returnPeriod(self):
        taxas = self.taxas_assets

        def calculate_return_portfolio(taxas, port):
            '''Calculando o crescimento em porcentagem em relação ao intervalo anterior'''
            porcent = port.taxas_to_dict(taxas)
            result = [0]
            for c in range(port.data_range-QTD_RETORNO_PERIODICO, port.data_range-1):
                count = 0
                for asset in porcent.keys(): 
                    if len(port.port_porcent[asset])>=c+1:
                        count += porcent[asset] * port.port_porcent[asset][c]
                result.append(count)
            return result

        values = calculate_return_portfolio(taxas, self.port)  
        VALORES_P = values
        NOME_X = self.port.dates_range

        data = [go.Bar(name='Portfolio', x=NOME_X, y=VALORES_P)]

        for comp in self.port_comp.keys():
            values_comp = calculate_return_portfolio([1], self.port_comp[comp])  
            data.append(go.Bar(name=comp, x=NOME_X, y=values_comp))

        fig= go.Figure(data=data, layout=go.Layout(title=go.layout.Title(text='Retorno Mensal(%)')))
        fig.layout.template = self.CHART_THEME
        fig.update_layout(barmode='group',
                    autosize=True,
                    #width=900,
                    height=380,
                    yaxis_range=[-1*max(values),max(values)])
        return fig


    def returnPortfolio(self):
        taxas = self.taxas_assets

        def calculate_return_portfolio(taxas, port):
            porcent = port.taxas_to_dict(taxas)
            result = [0]
            for c in range(port.data_range-1):
                count = 0
                for asset in porcent.keys(): 
                    if len(port.port[asset])>=c+1:
                        data_to_porcent = [0]
                        data_to_porcent += datas_to_porcent_init(port.port[asset])
                        count += porcent[asset] * data_to_porcent[c]
                result.append(count)
            return result

        values = calculate_return_portfolio(taxas, self.port)  

        NOME_X = self.port.dates_range
        fig = go.Figure() 
        fig.add_trace(go.Scatter(x=NOME_X, y=values, mode="lines", name='Portfolio'))

        for comp in self.port_comp.keys():
            values_comp = calculate_return_portfolio([1], self.port_comp[comp])  
            fig.add_trace(go.Scatter(x=NOME_X, y=values_comp, mode="lines",  name=comp))

        fig.layout.template = self.CHART_THEME

        return fig
    
    
    def fronteiraEficiente(self):
        risco, retorno = fronteiraEficiente()
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=retorno,
            y=risco,
            name='Distribuição dos ativos',
            marker=dict(
                size=5,
                cmax=0.04,
                cmin=-0.03,
                #color=[0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                colorbar=dict(
                    title="Sharpe Ratio"
                ),
                colorscale="Viridis"
            ),
            mode="markers"
        ))
        fig.add_trace(go.Scatter(
            x=[0.49],
            y=[0.022],
            marker=dict(color="red", size=12),
            mode="markers",
            name="Portfolio Minimizado",
            ))


        fig.layout.template = self.CHART_THEME
        fig.update_layout(
                legend=dict(
                            font_size=10,
                            yanchor='middle',
                            xanchor='right',
                            ),
                xaxis_title="Risco do Portfolio",
                yaxis_title="Retorno do Portfolio")


        return fig