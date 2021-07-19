import yfinance
import plotly.figure_factory as ff
def getfundamental(ticker):
    y=yfinance.Ticker(str(ticker).upper()+".NS")
    info=y.info
    print(info)
    try:
        info["website"]=f'<a href="{str(info["website"])}">Go to website</a>'
    except:
        pass
    try:
        info['logo_url']=f'<a href="{str(info["logo_url"])}">Go to website</a>'
    except:
        pass
    fig = ff.create_table(list(info.items()))
    return fig

