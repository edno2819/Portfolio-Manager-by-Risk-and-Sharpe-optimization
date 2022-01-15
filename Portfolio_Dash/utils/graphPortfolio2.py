from tkinter import N
from utils.math_calculate import *
import plotly.graph_objects as go
from utils.variaveis import QTD_RETORNO_PERIODICO, CHART_THEME
from utils.fronterEficiente import *




class GraphPort:
    def __init__(self, port, taxas_assets:list, port_comp={}, port_comp_taxa={}) -> None:
        self.port = port
        self.CHART_THEME = CHART_THEME
        self.taxas_assets = taxas_assets
        self.port_comp = port_comp
        self.port_comp_taxa = port_comp_taxa
    

    def graphAssets(self):
        fig = go.Figure() 
        annotations = []
        port = self.port_comp['Portfolio Bruto']

        for asset in port.port.keys():   
            fig.add_trace(go.Scatter(x=port.assets_dates[asset], y=port.port[asset],
                                mode="lines",  # you can also use "lines+markers", or just "markers"
                                name=asset))

            annotations.append(dict(xref='paper', x=1.01, y=port.port[asset][-1],
                            xanchor='left', yanchor='middle',
                            text=f'{round(port.port[asset][-1],2)*100}%',
                            font=dict(family='Arial',
                                        size=16),
                            showarrow=False))


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
                name_lis.append(asset)
        
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
            result = [0]
            for c in range(port.data_range-1):
                count = 0
                for asset in porcent.keys(): 
                    if len(port.port[asset])>c+1:
                        count += port.port_porcent_init[asset][c] * porcent[asset]
                result.append(count)
            return result

        def calculate_return_portfolio(taxas, port):
            porcent = port.taxas_to_dict(taxas)
            result = [0]
            for c in range(port.data_range-1):
                count = 0
                for asset in porcent.keys(): 
                    if len(port.port[asset])>c+1:
                        count += port.port_porcent_init[asset][c] * porcent[asset]
                result.append(count)
            return result

        values, dates = [0], []
        for port, pesos in zip(self.port, self.taxas_assets):
            dates += port.dates_range

        for port, pesos in zip(self.port, self.taxas_assets):
            x = [ c+values[-1] for c in calculate_return_portfolio(pesos, port)]
            values += x
            
        values = values[1:]
        fig = go.Figure() 
        fig.add_trace(go.Scatter(x=dates, y=values, mode="lines", name='Portfolio'))

        annotations.append(dict(xref='paper', x=1.01, y=values[-1],
                            xanchor='left', yanchor='middle',
                            text=f'{round(values[-1],2)*100}%',
                            font=dict(family='Arial',
                                        size=16),
                            showarrow=False))


        for comp in self.port_comp.keys():
            values_comp = calculate_return_portfolio_unique(self.port_comp_taxa[comp+' TAXA'], self.port_comp[comp])  
            fig.add_trace(go.Scatter(x=dates, y=values_comp, mode="lines",  name=comp))

            annotations.append(dict(xref='paper', x=1.01, y=values_comp[-1],
                                        xanchor='left', yanchor='middle',
                                        text=f'{round(values_comp[-1],2)*100}%',
                                        font=dict(family='Arial',
                                                    size=16),
                                        showarrow=False))

        fig.layout.template = self.CHART_THEME
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
        port = self.port[n]
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