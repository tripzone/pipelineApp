import numpy as np
import pandas as pd
import os.path
from datetime import datetime
import plotly.graph_objs as go
import plotly.plotly as py
import colorlover as cl
import cufflinks as cf
import xlwt
import plotly

periodDate = datetime(2017, 7, 30, 0, 0)
beginningDate = datetime(2017, 6, 4, 0, 0)
thisPeriod = '2018 - 03'
NinetyDayEnd = '2018 - 08'
yearBegin = '2018 - 01'
yearEnd = '2018 - 13'
dateTarget = '2017-12-01'

def generateTable(df):
	def computeRow(df, SL, stage, period):
		result = np.zeros(4)
		temp = df[(df['Close Period'] == period) & (df['line'] == SL) & (df['stage'] == stage)]
		result[0] = temp['TR'].sum()
		result[1] = temp['TR'].count()
		ytdTemp = df[(df['Close Period'] <= period) & (df['line'] == SL) & (df['stage'] == stage)]
		result[2] = ytdTemp['TR'].sum()
		result[3] = ytdTemp['TR'].count()
		return result

	def computeNewOp(df, SL):
		result = np.zeros(4)
		temp = df[(df['Created'] > periodDate) & (df['line'] == SL)]
		result[0] = temp['TR'].sum()
		result[1] = temp['TR'].count()
		ytdTemp = df[(df['Created'] > beginningDate) & (df['line'] == SL)]
		result[2] = ytdTemp['TR'].sum()
		result[3] = ytdTemp['TR'].count()
		return result

	def printIt(SL, rows):
		with open('./output/tableOut.csv','a') as file:
			file.write(SL+',')
			for row in rows:
				for cell in row:
					file.write(str(cell)+',')
			file.write('\n')
	try:
		os.remove('./output/tableOut.csv')
	except:
		pass

	for line in df['line'].unique():
		a = computeNewOp(df, line)
		b = computeRow(df, line, 6.0, thisPeriod)
		c = computeRow(df, line, -1.0, thisPeriod)
		d = computeRow(df, line, -2.0, thisPeriod)
		printIt(line,[a,b,c,d])

	temp = df[df['Close Period'] <= thisPeriod]
	print('outputted to file')
def pipePlots(df):

	# FIRST GRAPH
	dfGroup = df.groupby(['Close Period','stage'])['TR'].sum().reset_index()
	xVal=dfGroup['Close Period'].values
	yVal=dfGroup['stage'].values
	stages = dfGroup['stage'].unique()

	result = pd.DataFrame()
	for x in (y for y in stages if (y >= 0)):
		df = dfGroup[dfGroup['stage']==x].set_index('Close Period')
		df = df[['TR']]
		df = df.rename(columns={'TR': x})
		result = pd.concat([result, df], axis=1)
	result = result.reindex_axis(sorted(result.columns, reverse=True), axis=1)

	resultFY = (result[result.index <= yearEnd])

	target = pd.read_csv("uploads/target.csv").set_index('date')
	targetLocal = (target[target.index <= yearEnd])

	# color_scale_blues = reversed(cl.scales['7']['seq']['Greens'])
	# color_scale_blues =['#103834','#195953','#207068', '#629a95', '#bcd4d1', '#d2e2e0']
	color_scale_blues =['#060622','#1e6370','#589992',  '#7FB6B4', '#BCD4D1','#add8c3', '#e4faef']

	targetFig = targetLocal.iplot(kind='scatter', mode='lines', asFigure=True, dash=['dash'], width=[4], name = ["forecast"])
	for i, trace in enumerate(targetFig['data']):
		trace['line']['shape'] = 'spline'
		trace['name'] = 'FY18 NR targer'

	figure = resultFY.iplot(kind='area', fill=True, filename='stacked-area', colors=color_scale_blues,asFigure=True, opacity=0.8)
	figure['layout']['paper_bgcolor']='rgba(0,0,0,0)',
	figure['layout']['plot_bgcolor']='rgba(0,0,0,0)',
	figure['layout']['width']=1600

	legends = ['6 - Sold', '5 - Verbal Commit', '4 - Proposed', '3 - Developing', '2 - Qualifying', '1 - contacting', '0 - Identifying']

	for i, trace in enumerate(figure['data']):
		trace['line']['shape'] = 'spline'
		trace['mode']= 'lines'
		trace['name']= legends[i]

	figure['data'].extend(targetFig['data'])
	py.image.save_as(figure, filename='./output/allTech.png')

	from IPython.display import Image
	Image('./output/allTech.png')

	# SECOND GRAPH
	result = (result[result.index < NinetyDayEnd])
	targetHere = (target[target.index < NinetyDayEnd])
	opacityParam = 0.8

	total = result.fillna(0)[3.0]+result.fillna(0)[4.0]+result.fillna(0)[5.0]+result.fillna(0)[6.0]
	annotations = []

	for i, period in enumerate(list(result.index)):
		a = {
			'x': period,
			'y': total[i],
			'xanchor': 'center',
			'yanchor': 'bottom',
			'showarrow': False,
			'text': '${:,.0f}'.format(total[i])
			}
		annotations.append(a)

	data = [
	   go.Bar(
			x=list(result.index),
			y=result[6.0],
			marker=dict(
				color='#09211e'
			),
			name = "6 - Sold",
			opacity=opacityParam
		),
		go.Bar(
			x=list(result.index),
			y=result[5.0],
			marker=dict(
				color='#196059'
			),
			name = "5 - Verbal Commit",
			opacity=opacityParam

		),
		go.Bar(
			x=list(result.index),
			y=result[4.0],
			marker=dict(
				color='#629a95'
			),
			name = "4 - Proposed",
			opacity=opacityParam
		),
		 go.Bar(
			x=list(result.index),
			y=result[3.0],
			marker=dict(
				color='#bcd4d1'
			),
			name = "3 - Developing",
			opacity=opacityParam,
			text = ['a','b','c','d'],
		)
	]

	layout = go.Layout(
		barmode='stack',
		annotations= annotations,
		xaxis=dict(nticks=13),
		width=900,
	)


	targetFig = targetHere.iplot(kind='scatter', mode='markers', asFigure=True, dash=['dash'], width=[4], name = ["forecast"])
	for i, trace in enumerate(targetFig['data']):
		trace['line']['shape'] = 'spline'
		trace['name'] = 'FY18 NR targer'

	fig = go.Figure(data=data, layout=layout)
	fig['data'].extend(targetFig['data'])
	py.image.save_as(fig, filename='./output/90DayAll.png')
	from IPython.display import Image
	Image('./output/90DayAll.png')

def keyDeals(df, dfTech ):
	# TABLE
	keyDealsRead = pd.read_csv("uploads/keydeals.csv").set_index('Id')
	keyDeals = keyDealsRead.join(df)
	keyDeals['90DayWindow?'] = np.where(keyDeals['Close Period']< NinetyDayEnd, 'TRUE', '' )
	# output90Day = output[output['Close Period'] < NinetyDayEnd]
	# keyDeals.dropna(inplace=True)
	keyDealsGroup = keyDeals.groupby('Category').sum()
	keyDealsClean = keyDeals[['Rational', 'Selected By','stage', 'Account', 'Opportunity', 'TR', 'line', 'Close Date', 'Category','90DayWindow?']].sort_values(by='Selected By')
	# keyDealsClean = keyDeals[['Selected By','Rational', 'Category']].sort_values(by='Selected By')

	keyDealsClean.to_csv('./output/keydealsoutput.csv')

	#PLOT
	ed = keyDealsRead.join(dfTech)
	group = ed.groupby(['Close Period','stage'])['TR'].sum()
	ed = group.reset_index()
	result = pd.DataFrame()
	stages = dfTech['stage'].unique()

	for x in (y for y in stages if (y >= 0)):
		df = ed[ed['stage']==x].set_index('Close Period')
		df = df[['TR']]
		df = df.rename(columns={'TR': x})
		result = pd.concat([result, df], axis=1)
	result = result.reindex_axis(sorted(result.columns, reverse=True), axis=1)

	resultHere = (result[result.index < NinetyDayEnd])

	result = (result[result.index < NinetyDayEnd])
	opacityParam = 0.8

	total = result.fillna(0)[3.0]+result.fillna(0)[4.0]+result.fillna(0)[5.0]
	annotations = []

	for i, period in enumerate(list(result.index)):
		a = {
			'x': period,
			'y': total[i],
			'xanchor': 'center',
			'yanchor': 'bottom',
			'showarrow': False,
			'text': '${:,.0f}'.format(total[i])
			}
		annotations.append(a)


	data = [
		go.Bar(
			x=list(result.index),
			y=result[5.0],
			marker=dict(
				color='#196059'
			),
			name = "5 - Verbal Commit",
			opacity=opacityParam

		),
		go.Bar(
			x=list(result.index),
			y=result[4.0],
			marker=dict(
				color='#629a95'
			),
			name = "4 - Proposed",
			opacity=opacityParam
		),
		 go.Bar(
			x=list(result.index),
			y=result[3.0],
			marker=dict(
				color='#bcd4d1'
			),
			name = "3 - Developing",
			opacity=opacityParam,
			text = ['a','b','c','d'],
		)
	]

	layout = go.Layout(
		barmode='stack',
		annotations= annotations,
		xaxis=dict(nticks=13),
		width=900,
	)

	# fig = go.Figure(data=data, layout=layout)
	# py.image.save_as(fig, filename='./output/90DaySelected.png')

	from IPython.display import Image
	Image('./output/keyDeals.png')
	# py.iplot(fig, filename='grouped-bar')

def slPlot(df):
	SLTotal = df[(df['stage'] != [-2]) & (df['stage'] != [-1]) &(df['Close Period'] < NinetyDayEnd)].groupby('line').sum()['TR']
	# SLTotal = SLTotal.iloc[::-1]
	data = [
		go.Bar(
			x=SLTotal.index, # assign x as the dataframe column 'x'
			y=SLTotal.values,
			width = 0.5,
			marker=dict(
				color='#bcd4d1',
				line=dict(
					color='#629a95',
					width=2,
			)
			),
		)
	]

	layout = go.Layout(
		width=700,
	)

	fig = go.Figure(data=data, layout=layout)
	py.image.save_as(fig, filename='./output/SlsPlot.png')
	from IPython.display import Image
def dealSizePlot(df):
	#DEAL SIZE

	tiers = ['0M-1M', '1M-5M', '5M-10M', '10M+']

	sizeTier = df[df['Close Period'] < NinetyDayEnd].copy()
	sizeTier['size'] = np.where(sizeTier['TR']<1000000, tiers[0],
								np.where(sizeTier['TR']<5000000, tiers[1],
										np.where(sizeTier['TR']<10000000, tiers[2], tiers[3])))

	sizetierGroup = sizeTier.groupby('size').sum()['TR']
	sizetierGroup = sizetierGroup.reindex([tiers[0], tiers[1], tiers[2], tiers[3]])
	labels = sizetierGroup.index
	values = sizetierGroup.values
	colors = cl.scales['4']['qual']['Pastel2']
	data = [go.Pie(labels=labels, values=values,pull=.05, hole=.05, marker=dict(colors=colors, line=dict(width=2)))]

	layout = go.Layout(
		legend=dict(traceorder="normal")
	)
	fig = go.Figure(data=data, layout=layout)
	py.image.save_as(fig, filename='./output/dealSizePlot.png')
	from IPython.display import Image
def closeReasonPlot(df):
	closeTier = df[(df["stage"]==-2) | (df["stage"]==-1) | (df["stage"]==6)].copy()
	closeTier = closeTier[closeTier['Close Period'] < NinetyDayEnd]
	closeTier.replace({"stage": {6.0:'Sold', -2:'Abandoned' , -1:'Lost'}}, inplace= True)
	closeTierGroup = closeTier.groupby('stage').sum()['TR']
	labels = closeTierGroup.index
	values = closeTierGroup.values
	colors = cl.scales['3']['qual']['Pastel2']
	data = [go.Pie(labels=labels, values=values,pull=.05, hole=.05, marker=dict(colors=colors, line=dict(width=2)))]
	fig = go.Figure(data=data)
	py.image.save_as(fig, filename='./output/closeReasonPlot.png')
	from IPython.display import Image
def averageAgePlot(df):
	#AVERAGE AGE
	averageAge = (df[(df["stage"]!= -2) & (df["stage"]!= -1) & (df["stage"]!=6)]).copy()
	averageAge = averageAge[averageAge['Close Period'] < NinetyDayEnd]

	now = datetime.now()
	averageAge['age'] = (now - averageAge['Created'])/np.timedelta64(1, 'D')
	averageAge.replace({"stage": {0.0:'Identifying', 1:'Contacting' , 2:'Qualifying',3:'Developing' , 4:'Proposed', 5:'Verbal Commit'}}, inplace= True)

	averageAgeGroup = averageAge.groupby('stage').mean()['age']
	data = [
		go.Bar(
			x=averageAgeGroup.index, # assign x as the dataframe column 'x'
			y=averageAgeGroup.values,
			width = 0.5,
			marker=dict(
				color='#bcd4d1',
				line=dict(
					color='#629a95',
					width=2,
			)
			),
		)
	]

	layout = go.Layout(
		width=700,
		yaxis=dict(
		title='Days',
		)
	)

	fig = go.Figure(data=data, layout=layout)
	py.image.save_as(fig, filename='./output/averageAgePlot.png')

	#AGE TIER
	ageTier = averageAge

	tiers = ["0 - 3 Weeks", "3 - 6 Weeks", "6 weeks - 3 months", "3 months +"]
	ageTier['ageTier'] = np.where(ageTier['Number of Days since Last Updated']<21, tiers[0],
								np.where(ageTier['Number of Days since Last Updated']<42, tiers[1],
										np.where(ageTier['Number of Days since Last Updated']<91, tiers[2], tiers[3])))

	ageTierGroup = ageTier.groupby('ageTier').sum()['TR']
	ageTierGroup = ageTierGroup.reindex([tiers[0], tiers[1], tiers[2], tiers[3]])
	data = [
		go.Bar(
			x=ageTierGroup.index, # assign x as the dataframe column 'x'
			y=ageTierGroup.values,
			width = 0.5,
			marker=dict(
				color='#bcd4d1',
				line=dict(
					color='#629a95',
					width=2,
			)
			),
		)
	]

	layout = go.Layout(
		width=700,
		yaxis=dict(
		title='Days',
		)
	)

	fig = go.Figure(data=data, layout=layout)
	fig = go.Figure(data=data, layout=layout)
	py.image.save_as(fig, filename='./output/ageTierPlot.png')
def initiateDf():
	plotly.tools.set_credentials_file(username='kasra.zahir', api_key='p04mrpvEHUM1994TQbbP')

	FY = pd.read_csv("./uploads/data.csv").set_index('Id#')

	columns = [
		'Tech Service Line',
		'90 day',
		'Service',
		'Service Line Group',
		'Sales Stage',
		'Close Date',
		'Close Period',
		'Total Estimated Revenue',
		'Created',
		'Account',
		'Opportunity',
		'Last Updated',
		'Number of Days since Last Updated'
	   ]


	FY = FY[columns]
	# ed = FYTechAll[['Close Date','Close Period', 'Tech Service Line','Sales Stage', 'Total Estimated Revenue','Created', 'Last Updated', 'Number of Days since Last Updated']].copy()
	FY.rename(columns={'Total Estimated Revenue': 'TR', 'Tech Service Line':'line', 'Sales Stage':'stage'}, inplace=True)

	FY['TR'] = FY['TR'].str.replace(r'[$,]', '').astype('float')
	FY['stage'] = FY['stage'].map(lambda x: str(x)[:2])
	FY['stage'] = FY['stage'].astype(float)
	FY['stage'] = FY['stage'].replace(8, -2)
	FY['stage'] = FY['stage'].replace(7, -1)
	FY['Created'] = pd.to_datetime(FY['Created'])
	FY['Last Updated'] = pd.to_datetime(FY['Last Updated'])
	return FY

def initiateTech(FY):
	# FY = initiateDf()
	FYTechAll = FY[FY['Service Line Group'] == 'Technology'][FY['Close Period'] >= yearBegin].copy()
	return FYTechAll

def plotIt(type, data):
	if (type == 'pipe'):
		pipePlots(data)
	elif (type == 'sl'):
		slPlot(data)
	elif (type == 'dealsize'):
		dealSizePlot(data)
	elif (type == 'closeReason'):
		closeReasonPlot(data)
	elif (type == 'averageAge'):
		averageAgePlot(data)
	return({succes:False, error:'invalid plot type'})

def tableOut(type, data, FY):
	if (type == 'newOpp'):
		generateTable(data)
	elif (type == 'keyDeals'):
		keyDeals(FY, data)
		return({succes:False, error:'invalid plot type'})
