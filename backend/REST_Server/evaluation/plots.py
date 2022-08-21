import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.colors import n_colors
import datetime

def plotMetrics(df: pd.DataFrame):
    categories = df.pixelAccuracy[0].keys()

    for cat in categories:
        df[cat + ": Pixel Accuracy"] = [d.get(cat) for d in df.pixelAccuracy]
        df[cat + ": IoU"] = [d.get(cat) for d in df.IoU]
        df[cat + ": Dice Coefficient"] = [d.get(cat) for d in df.diceCoefficient]
    
    df.drop('pixelAccuracy', inplace=True, axis=1)
    df.drop('IoU', inplace=True, axis=1)
    df.drop('diceCoefficient', inplace=True, axis=1)

    df = df.set_index('tsCorrectionReceived')
    df.index = pd.to_datetime(df.index)

    dfhour = df.resample('H').mean().dropna(thresh=1)
    dfday = df.resample('D').mean()
    dfweek = df.resample('W-MON').mean()

    df.index.names = ['Date']
    df.reset_index(inplace= True)

    dfhour.index.names = ['Date']
    dfhour.reset_index(inplace= True)

    dfday.index.names = ['Date']
    dfday.reset_index(inplace= True)

    dfweek.index.names = ['Date']
    dfweek.reset_index(inplace= True)

    fig = go.Figure()
    dfs = {'none':df, 'hourly': dfhour, 'daily' :dfday, 'weekly':dfweek}

    # specify visibility for traces accross dataframes
    frames = len(dfs) # number of dataframes organized in  dict
    columns = len(dfs['none'].columns) - 1 # number of columns i df, minus 1 for Date
    scenarios = [list(s) for s in [e==1 for e in np.eye(frames)]]
    visibility = [list(np.repeat(e, columns)) for e in scenarios] 

    buttons = []

    # - i is used to reference visibility attributes
    # - k is the name for each dataframe
    # - v is the dataframe itself
    for i, (k, v) in enumerate(dfs.items()):
        for c, column in enumerate(v.columns[1:]):
            fig.add_scatter(name = column,
                            x = v['Date'],
                            y = v[column], 
                            visible=True if k=='none' else False # 'all' values are shown from the start
                        )
                    
        # one button per dataframe to trigger the visibility of all columns / traces for each dataframe
        button =  dict(label=k,
                    method = 'restyle',
                    args = ['visible',visibility[i]])
        buttons.append(button)

    # include dropdown updatemenu in layout
    fig.update_layout(updatemenus=[dict(type="dropdown",
                                        direction="down",
                                        buttons = buttons,
                                        y=1.15,
                                        x=1.),])
    
    fig.update_layout(
    title="Metrics for received Corrections",
    xaxis_title="Date",
    yaxis_title="Value",
    legend_title="Metrics",
    )

    figHtml = fig.to_html(full_html=False, include_plotlyjs='cdn')
    return figHtml

def plotModels(df: pd.DataFrame):
    modelVersions = df.modelVersion.unique()

    iouDict = {}
    for model in modelVersions:
        iouDf = df.loc[df['modelVersion'] == model]
        iouDict[model] = [sum(d.values())/(len(d.values())) for d in iouDf.IoU]

    if len(modelVersions) > 1:
        colors = n_colors('rgb(5, 200, 200)', 'rgb(200, 10, 10)', len(modelVersions), colortype='rgb')
    else:
        colors = ['rgb(5, 200, 200)']

    fig = go.Figure()

    for i, (model, value) in enumerate(iouDict.items()):
        fig.add_trace(go.Box(y=value,boxpoints='suspectedoutliers', jitter=0.2, name=model, marker_color =colors[i]))
        #fig.add_trace(go.Violin(x=value, line_color=colors[i], name=model))

    #fig.update_traces(orientation='h', side='positive', width=3, points=False)
    fig.update_layout(xaxis_showgrid=False, xaxis_zeroline=False,showlegend=False,)

    fig.update_layout(
    title="Model Versions",
    yaxis_title="mIoU",
    xaxis_title="Model Version",
    )

    config = {
    'toImageButtonOptions': {
        'format': 'png', # one of png, svg, jpeg, webp
        'filename': 'custom_image',
        'height': 500,
        'width': 700,
        'scale':6 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    figHtml = fig.to_html(full_html=False, config= config, include_plotlyjs='cdn')
    return figHtml

def plotApiUsage(df: pd.DataFrame):
    fig = go.Figure()

    fig.add_trace(go.Histogram(x=df.tsStartSegmentation,
                    xbins=dict(
                      start=df.tsStartSegmentation.min().hour,
                      end=df.tsStartSegmentation.max(),
                      size='3600000'),
                      autobinx=False))
    
    fig.update_layout(xaxis_range=[datetime.datetime.now() - datetime.timedelta(hours=24)
                                   ,datetime.datetime.now() ])

    fig.update_layout(
    title="API Usage",
    xaxis_title="Date",
    yaxis_title="Segmentation Uploads",
    height=400,
    )

    figHtml = fig.to_html(full_html=False, include_plotlyjs='cdn')
    return figHtml

def plotSegmentationTime(df: pd.DataFrame):
    fig = go.Figure()

    deltaTime = df.tsEndSegmentation-df.tsStartSegmentation
    deltaMs = [d.total_seconds() * 1000 for d in deltaTime] 

    fig.add_trace(go.Box(y=deltaMs,
            boxpoints='suspectedoutliers', # can also be all, outliers, or suspectedoutliers, or False
            jitter=0.2, # add some jitter for a better separation between points
            name="",
            quartilemethod="inclusive"))

    upperfence = np.percentile(deltaMs, 75) + (1.5*(np.percentile(deltaMs, 75)-np.percentile(deltaMs, 25)))
    lowerfence = np.percentile(deltaMs, 25) - (1.5*(np.percentile(deltaMs, 75)-np.percentile(deltaMs, 25)))
    
    fig.update_layout(yaxis_range=[lowerfence*0.8 ,upperfence*1.2])
        
    fig.update_layout(
    title="Time for Segmentation",
    yaxis_title="Time [ms]",
    )

    figHtml = fig.to_html(full_html=False, include_plotlyjs='cdn')
    return figHtml

def plotModelLoss(df: pd.DataFrame):
    fig = go.Figure()

    loss = [x for xs in df['loss'] for x in xs]
    val_loss = [x for xs in df['val_loss'] for x in xs]
    epoche = [ind+1 for ind, x in enumerate(loss)]

    fig.add_trace(go.Scatter(x=epoche, y=loss, mode='lines', name='loss'))
    fig.add_trace(go.Scatter(x=epoche, y=val_loss, mode='lines', name='val_loss'))

    fig.update_layout(
    title="Loss",
    xaxis_title="Epoch",
    height=250,
    )

    figHtml = fig.to_html(full_html=False, include_plotlyjs='cdn')
    return figHtml

def plotModelAccuracy(df:pd.DataFrame):
    fig = go.Figure()

    accuracy = [x for xs in df['accuracy'] for x in xs]
    val_accuracy = [x for xs in df['val_accuracy'] for x in xs]
    epoche = [ind+1 for ind, x in enumerate(accuracy)]

    fig.add_trace(go.Scatter(x=epoche, y=accuracy, mode='lines', name='accuracy'))
    fig.add_trace(go.Scatter(x=epoche, y=val_accuracy, mode='lines', name='val_accuracy'))

    fig.update_layout(
    title="Accuracy",
    xaxis_title="Epoch",
    height=250,
    )

    figHtml = fig.to_html(full_html=False, include_plotlyjs='cdn')
    return figHtml

def plotSegToCorPie(seg:int, cor:int):
    fig = go.Figure()

    fig.add_trace(go.Pie(labels=["Segmentations", "Corrections"], values=[seg,cor]))

    fig.update_layout(
    title="Received tasks",
    height=400,
    )

    figHtml = fig.to_html(full_html=False, include_plotlyjs='cdn')
    return figHtml