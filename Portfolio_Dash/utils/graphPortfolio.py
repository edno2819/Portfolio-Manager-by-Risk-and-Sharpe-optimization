from tkinter import N
from utils.math_calculate import *
import plotly.graph_objects as go
from utils.variaveis import QTD_RETORNO_PERIODICO, CHART_THEME, ASSETS
from utils.fronterEficiente import *
from statistics import variance, stdev




class GraphPort:
    def __init__(self, port, taxas_assets:list, port_comp={}, port_comp_taxa={}) -> None:
        self.port = port
        self.CHART_THEME = CHART_THEME
        self.taxas_assets = taxas_assets
        self.port_comp = port_comp
        self.port_comp_taxa = port_comp_taxa
        self.values_growth = {}
    

    def graphAssets(self):
        fig = go.Figure() 
        annotations = []
        port = self.port_comp['Portfolio Bruto']

        for asset in port.port.keys():   
            name = list(ASSETS.keys())[list(ASSETS.values()).index(asset)] if asset in list(ASSETS.values()) else asset
            fig.add_trace(go.Scatter(x=port.assets_dates[asset], y=port.port[asset],
                                mode="lines",  
                                name=name))


        annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                            xanchor='center', yanchor='top',
                            text='Source: Yahoo Finance',
                            font=dict(family='Arial',
                                        size=12,
                                        color='rgb(150,150,150)'),
                            showarrow=False))
                  
        fig.layout.template = self.CHART_THEME
        fig.update_layout(margin = dict(t=50, b=50, l=25, r=25))  
        fig.update_layout(
            xaxis_tickfont_size=12,
            yaxis=dict(
                title='Value: $ USD',
                titlefont_size=14,
                tickfont_size=12,
                ))

        fig.update_layout(annotations=annotations)
        fig.update_layout(legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ))

        return fig


    def circle_chart_portifolio(self, n=-1):
        lis = []
        name_lis = []
        taxas_dict = self.port[n].taxas_to_dict(self.taxas_assets[n])
        for asset in taxas_dict.keys():
            if taxas_dict[asset]>0.01:
                lis.append(taxas_dict[asset])
                name = list(ASSETS.keys())[list(ASSETS.values()).index(asset)] if asset in list(ASSETS.values()) else asset
                name_lis.append(name)
        
        date_start = self.port[n].dates[0].__str__()[:10]
        date_end = self.port[n].dates[-1].__str__()[:10]
        num = n+1 if n!=-1 else len(self.port)

        fig = go.Figure()
        fig.layout.template = self.CHART_THEME
        fig.add_trace(go.Pie(labels=name_lis, values=lis))
        fig.update_traces(hole=.7, hoverinfo="label+percent")
        fig.update_traces(textposition='outside', textinfo='label+percent')
        fig.update_layout(showlegend=False)
        fig.update_layout(title=go.layout.Title(text=f'N°{num}: {date_start}|{date_end}'))
        fig.update_layout(margin = dict(t=50, b=50, l=25, r=25))
        return fig


    def indicatorPeriod(self, main, comp):
        fig = go.Figure()
        fig.layout.template = self.CHART_THEME
        values = self.values_growth[main]

        fig.add_trace(go.Indicator(
            mode = "delta",
            value = values[-1],
            number = {'suffix': " %"},
            title = {"text": "<span style='font-size:0.9em;color:gray'>Crescimento</span>"},
            delta = {'position': "bottom", 'reference': 1, 'relative': True, "valueformat": ".1%"},
            domain = {'row': 0, 'column': 0}))

        fig.add_trace(go.Indicator(
            mode = "number",
            value = round(sdp(values),3),#round(stdev(values),3)
            number = {'suffix': ""},
            title = {"text": "<span style='font-size:0.9em;color:gray'>Desvio Padrão Neg</span>"},
            domain = {'row': 1, 'column': 0}))

        fig.add_trace(go.Indicator(
            mode = "delta",
            value = max_drawdowm(values)*-0.01,
            title = {"text": "<span style='font-size:0.9em;color:gray'>Drawdown</span>"},
            delta = {'position': "bottom", 'reference': 0, 'relative': False, "valueformat": ".1%"},
            domain = {'row': 2, 'column': 0}))


        a, b = superi(values, self.values_growth[comp])
        fig.add_trace(go.Indicator(
            mode = "delta",
            value = a/100,
            title = {"text": f"<span style='font-size:0.9em;color:gray'>VS {comp}</span>"},
            delta = {'position': "bottom", 'reference': 0, 'relative': False, "valueformat": ".1%"},
            domain = {'row': 3, 'column': 0}))

        fig.add_trace(go.Indicator(
            mode = "delta",
            value = b,
            title = {"text": "<span style='font-size:0.9em;color:gray'>% ACIMA</span>"},
            delta = {'position': "bottom", 'reference': 0, 'relative': False, "valueformat": ".1%"},
            domain = {'row': 4, 'column': 0}))

        a, b = superi(values, self.values_growth['IBOVESPA'])
        fig.add_trace(go.Indicator(
            mode = "delta",
            value = a/100,
            title = {"text": "<span style='font-size:0.9em;color:gray'>VS IBOVESPA</span>"},
            delta = {'position': "bottom", 'reference': 0, 'relative': False, "valueformat": ".1%"},
            domain = {'row': 5, 'column': 0}))

        fig.add_trace(go.Indicator(
            mode = "delta",
            value = b,
            title = {"text": "<span style='font-size:0.9em;color:gray'>% ACIMA</span>"},
            delta = {'position': "bottom", 'reference': 0, 'relative': False, "valueformat": ".1%"},
            domain = {'row': 6, 'column': 0}))

        fig.update_layout(
            grid = {'rows': 7, 'columns': 1, 'pattern': "independent"},
            margin=dict(l=50, r=50, t=30, b=30)
        )
        
        return fig
    

    def returnPeriod(self):
        def calculate_return_portfolio(taxas, port):
            '''Calculando o crescimento em porcentagem em relação ao intervalo anterior'''
            porcent = port.taxas_to_dict(taxas)
            result = [0]
            for c in range(0, port.data_range-1):
                count = 0
                for asset in porcent.keys(): 
                    if len(port.port_porcent[asset])>=c+1:
                        count += porcent[asset] * port.port_porcent[asset][c]
                result.append(count)
            return result


        values, dates = [], []
        for port, pesos in zip(self.port, self.taxas_assets):
            values += calculate_return_portfolio(pesos, port)
            dates += port.dates_range

        values = values[len(values)-QTD_RETORNO_PERIODICO:]
        dates = dates[len(dates)-QTD_RETORNO_PERIODICO:]


        data = [go.Bar(name='Portfolio', x=dates, y=values)]

        for comp in self.port_comp.keys():
            values_comp = calculate_return_portfolio(self.port_comp_taxa[comp+' TAXA'], self.port_comp[comp]) 
            data.append(go.Bar(name=comp, x=dates, y=values_comp))

        fig = go.Figure(data=data, layout=go.Layout(title=go.layout.Title(text=f'Retorno {self.port[-1].interval}(%)')))
        fig.layout.template = self.CHART_THEME
        fig.update_layout(barmode='group',
                    autosize=True,
                    yaxis_range=[-1*max(values),max(values)])
        return fig


    def returnPortfolio(self):
        annotations = []

        def calculate_return_portfolio_unique(taxas, port):
            porcent = port.taxas_to_dict(taxas)
            result = []
            for c in range(port.data_range-1):
                count = 1
                for asset in porcent.keys(): 
                    if len(port.port[asset])>c+1:
                        count += port.port_porcent_init[asset][c] * porcent[asset]
                result.append(round(count, 4))
            return result

        def calculate_return_portfolio(taxas, port):
            porcent = port.taxas_to_dict(taxas)
            result = []
            for c in range(port.data_range-1):
                count = 0
                for asset in porcent.keys(): 
                    if len(port.port[asset])>c+1:
                        count += port.port_porcent[asset][c] * porcent[asset]
                result.append(round(count, 4))
            return result

        values, dates = [1], []
        for port in self.port:
            dates += port.dates_range
        dates = list(set(dates))
        dates.sort()

        for port, pesos in zip(self.port, self.taxas_assets):
            p = calculate_return_portfolio(pesos, port)
            x = [values[-1] * (p[0] + 1)]
            for c in range(1, len(p)):
                x.append(x[c-1] * (p[c] + 1))
            values += x

        # teste = self.port_comp['Portfolio Bruto']
        # teste.port_porcent_init['ABEV3.SA']
        # self.port[0].port_porcent_init['ABEV3.SA']
        # self.port[1].port_porcent_init['ABEV3.SA']
            
        values = values[1:]
        self.values_growth['Portfolio'] = values
        fig = go.Figure() 
        fig.add_trace(go.Scatter(x=dates, y=values, mode="lines", name='Portfolio'))
        annotations.append(dict(xref='paper', x=1.01, y=values[-1],
                    xanchor='left', yanchor='middle',
                    text=f'{round(values[-1]*100,2)}%',
                    font=dict(family='Arial',
                                size=16),
                    showarrow=False))
        

        for comp in self.port_comp.keys():
            values_comp = calculate_return_portfolio_unique(self.port_comp_taxa[comp+' TAXA'][:len(dates)], self.port_comp[comp])  
            fig.add_trace(go.Scatter(x=dates, y=values_comp, mode="lines",  name=comp))
            self.values_growth[comp] = values_comp
            annotations.append(dict(xref='paper', x=1.01, y=values_comp[-1],
                            xanchor='left', yanchor='middle',
                            text=f'{round(values_comp[-1]*100,2)}%',
                            font=dict(family='Arial',
                                        size=16),
                            showarrow=False))

        fig.layout.template = self.CHART_THEME#"seaborn"#
        # Source
        annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                                    xanchor='center', yanchor='top',
                                    text='Source: Yahoo Finance',
                                    font=dict(family='Arial',
                                                size=12,
                                                color='rgb(150,150,150)'),
                                    showarrow=False))

        fig.update_layout(annotations=annotations)
        fig.update_layout(legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ))

        return fig
    
    
    def fronteiraEficiente(self, n=-1):
        #port = self.port_comp['Portfolio Bruto']
        port = self.ports_to_mini[n]
        taxas = self.taxas_assets[n]
        retorno_port, risco_port = port.return_portfolio(taxas), port.risk_portfolio(taxas)
        
        p = [round(1/len(taxas),3) for c in taxas]
        retorno_port2, risco_port2 = port.return_portfolio(p), port.risk_portfolio(p)

        risco, retorno = fronteiraEficiente_2(port, len(taxas))
        sharpe_ratio = [d/c for c, d in zip(risco, retorno)]


        date_start = port.dates[0].__str__()[:10]
        date_end = port.dates[-1].__str__()[:10]
        num = n+1 if n!=-1 else len(self.port)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=risco,
            y=retorno,
            name='Distribuição dos ativos',
            marker=dict(
                size=7,
                cmax=max(sharpe_ratio),
                cmin=min(sharpe_ratio),
                color=sharpe_ratio,
                colorbar=dict(
                    title="Sharpe Ratio"
                ),
                colorscale='Inferno'
            ),
            mode="markers"
        ))

        fig.add_trace(go.Scatter(
            x=[risco_port],
            y=[retorno_port],
            marker=dict(color="green", size=12),
            mode="markers",
            name="Portfolio Minimizado",
            ))

        fig.add_trace(go.Scatter(
            x=[risco_port2],
            y=[retorno_port2],
            marker=dict(color="blue", size=12),
            mode="markers",
            name="Portfolio Bruto",
            ))


        fig.layout.template = self.CHART_THEME
        fig.update_layout(title=go.layout.Title(text=f'N°{num}: {date_start}|{date_end}'))
        fig.update_layout(
                legend=dict(
                            font_size=13,
                            yanchor='middle',
                            xanchor='right',
                            ),
                xaxis_title="Risco do Portfolio",
                yaxis_title="Retorno do Portfolio")


        return fig