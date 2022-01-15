from utils.setPortfolio2 import *
import plotly.graph_objects as go
from utils.variaveis import CHART_THEME


class SetPara:
    def __init__(self) -> None:
        self.GrapPor = []
        self.dataset = []
        self.risco = 0
        self.retur = 0
        self.sharpe = 0

    def refresh(self, assets, interval, start, end, atualization, dates_to_calculate, tipo):
        GrapPor, risco, retur, sharpe, dataset = createPortfolio(assets, interval, start, end, atualization, dates_to_calculate, tipo)
        if GrapPor!=False:
            self.GrapPor = GrapPor
            self.risco = risco
            self.retur = retur
            self.sharpe = sharpe
            self.dataset = dataset
    
    def returnAvoid(self):
        fig = go.Figure() 
        fig.layout.template = CHART_THEME
        return fig
    
    def figPie(self, n=0):
        if type(self.GrapPor)==list:
            return self.returnAvoid()
        return self.GrapPor.circle_chart_portifolio(n)

    def graphAssets(self):
        if type(self.GrapPor)==list:
            return self.returnAvoid()
        return self.GrapPor.graphAssets()

    def indicatorPeriod(self):
        if type(self.GrapPor)==list:
            return self.returnAvoid()
        return self.GrapPor.indicatorPeriod()

    def returnPeriod(self):
        if type(self.GrapPor)==list:
            return self.returnAvoid()
        return self.GrapPor.returnPeriod()

    def returnPortfolio(self):
        if type(self.GrapPor)==list:
            return self.returnAvoid()
        return self.GrapPor.returnPortfolio()

    def fronteiraEficiente(self, n=0):
        if type(self.GrapPor)==list:
            return self.returnAvoid()
        return self.GrapPor.fronteiraEficiente(n)


    

Figs = SetPara()

#OBSERVAÇÕES
# Botar uma seta pra atualizar as configurações do portifólio no gráfico de pizza
# avisar qual ativo ta dando erro
# Fazer um comparativo da queda dos portifólios nos anos de 2008 e 2020