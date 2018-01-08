import numpy as np
import pandas as pd
import os.path
from datetime import datetime, timedelta
import plotly.graph_objs as go
import plotly.plotly as py
import colorlover as cl
import cufflinks as cf
import xlrd, openpyxl
import plotly

# periodDate = datetime(2017, 11, 19, 0, 0)
# beginningDate = datetime(2017, 6, 4, 0, 0)
# thisPeriod = '2018 - 07'
# NinetyDayEnd = '2018 - 10'
# yearBegin = '2018 - 01'
# yearEnd = '2018 - 13'

staticPath= "./static/"



def summaryTable(df, dt):
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
		temp = df[(df['Created'] >= dt["periodDate"]) & (df['line'] == SL)]
		result[0] = temp['TR'].sum()
		result[1] = temp['TR'].count()
		ytdTemp = df[(df['Created'] > dt["beginningDate"]) & (df['line'] == SL)]
		result[2] = ytdTemp['TR'].sum()
		result[3] = ytdTemp['TR'].count()
		return result

	def printIt(SL, rows):
		with open(staticPath+'tableOut.csv','a') as file:
			file.write(SL+',')
			for row in rows:
				for cell in row:
					file.write(str(cell)+',')
			file.write('\n')
	try:
		os.remove(staticPath+'tableOut.csv')
	except:
		pass

	slines = df['line'].unique()
	slines = [x for x in slines if str(x) != 'nan']
	print(slines)
	for line in np.sort(slines):
		a = computeNewOp(df, line)
		b = computeRow(df, line, 6, dt["thisPeriod"])
		c = computeRow(df, line, -1, dt["thisPeriod"])
		d = computeRow(df, line, -2, dt["thisPeriod"])
		printIt(line,[a,b,c,d])

	temp = df[df['Close Period'] <= dt["thisPeriod"]]
	print('outputted to file')

def pipePlots(df, dt):
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

	resultFY = (result[result.index <= dt["yearEnd"]])
	# resultFY.to_csv('1.pipeline.csv')

	target = pd.read_csv("uploads/target.csv").set_index('date')
	targetLocal = (target[target.index <= dt["yearEnd"]])

	# color_scale_blues = reversed(cl.scales['7']['seq']['Greens'])
	# color_scale_blues =['#103834','#195953','#207068', '#629a95', '#bcd4d1', '#d2e2e0']
	color_scale_blues =['#060622','#1e6370','#589992',  '#7FB6B4', '#BCD4D1','#add8c3', '#e4faef']

	targetFig = targetLocal.iplot(kind='scatter', mode='lines', asFigure=True, dash=['dash'], width=[4], name = ["forecast"])
	for i, trace in enumerate(targetFig['data']):
		trace['line']['shape'] = 'spline'
		trace['name'] = 'FY18 NSR target'

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
	py.image.save_as(figure, filename=staticPath+'allTech.png')

	# SECOND GRAPH
	result = (result[result.index <= dt["NinetyDayEnd"]])
	targetHere = (target[target.index <= dt["NinetyDayEnd"]])
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
		width=1000,
	)


	targetFig = targetHere.iplot(kind='scatter', mode='markers', asFigure=True, dash=['dash'], width=[4], name = ["forecast"])
	for i, trace in enumerate(targetFig['data']):
		trace['line']['shape'] = 'spline'
		trace['name'] = 'FY18 NSR target'

	fig = go.Figure(data=data, layout=layout)
	fig['data'].extend(targetFig['data'])
	py.image.save_as(fig, filename=staticPath+'90DayAll.png')


def keyDeals(dfTech , dt):
	# TABLE
	keyDealsRead = pd.read_csv("uploads/keydeals.csv").set_index('Id')
	keyDeals = keyDealsRead.join(FY)
	keyDeals['90DayWindow?'] = np.where(keyDeals['Close Period']<= dt["NinetyDayEnd"], 'TRUE', '' )
	# keyDeals.dropna(inplace=True)
	keyDealsClean = keyDeals[['Rational', 'Selected By','stage', 'Account', 'Opportunity', 'TR', 'line', 'Close Date', 'Category','90DayWindow?']].sort_values(by='Selected By')
	# keyDealsClean = keyDeals[['Selected By','Rational', 'Category']].sort_values(by='Selected By')
	# keyDealsClean.to_csv(staticPath+'keydealsoutput.csv')

	keyDealsGroup = keyDeals.groupby('Category').count()['TR']
	data1 = [
    	go.Bar(
	        x=keyDealsGroup.index,
	        y=keyDealsGroup.values,
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
	    font=dict(size=15)
	)

	fig1 = go.Figure(data=data1, layout=layout)
	py.image.save_as(fig1, filename=staticPath+'keyDealsRational.png')

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

	resultHere = (result[result.index <= dt["NinetyDayEnd"]])

	result = (result[result.index <= dt["NinetyDayEnd"]])
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

	fig = go.Figure(data=data, layout=layout)
	py.image.save_as(fig, filename=staticPath+'90DayKeyDeals.png')


def slPlot(df, dt):
	SLTotal = df[(df['stage'] != [-2]) & (df['stage'] != [-1]) &(df['Close Period'] <= dt["NinetyDayEnd"])].groupby('line').sum()['TR']
	# SLTotal.to_csv('2.sls.csv')

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
		font=dict(size=18),
	)
	fig = go.Figure(data=data, layout=layout)
	py.image.save_as(fig, filename=staticPath+'SlsPlot.png')

def dealSizePlot(df, dt):
	#DEAL SIZE
	tiers = ['0M-1M', '1M-5M', '5M-10M', '10M+']

	sizeTier = df[(df['stage'] != [-2]) & (df['stage'] != [-1]) & (df['Close Period'] <= dt["NinetyDayEnd"])].copy()
	sizeTier['size'] = np.where(sizeTier['TR']<=1000000, tiers[0],
								np.where(sizeTier['TR']<=5000000, tiers[1],
										np.where(sizeTier['TR']<=10000000, tiers[2], tiers[3])))

	sizetierGroup = sizeTier.groupby('size').sum()['TR']
	sizetierGroup = sizetierGroup.reindex([tiers[0], tiers[1], tiers[2], tiers[3]])
	# sizetierGroup.to_csv('3.sizeTiers.csv')

	labels = sizetierGroup.index
	values = sizetierGroup.values
	colors = cl.scales['4']['qual']['Pastel2']

	data = [go.Pie(labels=labels, values=values,pull=.05, hole=.05, marker=dict(colors=colors, line=dict(width=2)))]
	layout = go.Layout(
		legend=dict(traceorder="normal"),
		font=dict(size=15),
	)
	fig = go.Figure(data=data, layout=layout)
	py.image.save_as(fig, filename=staticPath+'dealSizePlot.png')

def closeReasonPlot(df, dt):
	closeTier = df[(df["stage"]==-2) | (df["stage"]==-1) | (df["stage"]==6)].copy()
	closeTier = closeTier[closeTier['Close Period'] <= dt["NinetyDayEnd"]]
	closeTier.replace({"stage": {6.0:'Sold', -2:'Abandoned' , -1:'Lost'}}, inplace= True)
	closeTierGroup = closeTier.groupby('stage').sum()['TR']
	# closeTierGroup.to_csv('4.closeReason.csv')

	labels = closeTierGroup.index
	values = closeTierGroup.values
	colors = cl.scales['3']['qual']['Pastel2']
	data = [go.Pie(labels=labels, values=values,pull=.05, hole=.05, marker=dict(colors=colors, line=dict(width=2)))]
	layout = go.Layout(
		font=dict(size=15),
	)
	fig = go.Figure(data=data, layout=layout)
	py.image.save_as(fig, filename=staticPath+'closeReasonPlot.png')


def averageAgePlot(df, dt):
	#AVERAGE AGE
	averageAge = (df[(df["stage"]!= -2) & (df["stage"]!= -1) & (df["stage"]!=6)]).copy()
	averageAge = averageAge[averageAge['Close Period'] <= dt["NinetyDayEnd"]]

	now = datetime.now()
	averageAge['age'] = (now - averageAge['Created'])/np.timedelta64(1, 'D')
	averageAge.replace({"stage": {0.0:'Identifying', 1:'Contacting' , 2:'Qualifying',3:'Developing' , 4:'Proposed', 5:'Verbal Commit'}}, inplace= True)
	averageAgeGroup = averageAge.groupby('stage').mean()['age']
	# averageAgeGroup.to_csv('5.averageAge.csv')

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
		font=dict(size=18),	
		yaxis=dict(
		title='Days',
		)
	)
	fig = go.Figure(data=data, layout=layout)
	py.image.save_as(fig, filename=staticPath+'averageAgePlot.png')

	#AGE TIER
	ageTier = averageAge

	tiers = ["0 - 3 Weeks", "3 - 6 Weeks", "6 weeks - 3 months", "3 months +"]
	ageTier['ageTier'] = np.where(ageTier['Number of Days since Last Updated']<22, tiers[0],
								np.where(ageTier['Number of Days since Last Updated']<43, tiers[1],
										np.where(ageTier['Number of Days since Last Updated']<93, tiers[2], tiers[3])))

	ageTierGroup = ageTier.groupby('ageTier').sum()['TR']
	ageTierGroup = ageTierGroup.reindex([tiers[0], tiers[1], tiers[2], tiers[3]])
	# ageTierGroup.to_csv('6.ageTier.csv')
	
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
		font=dict(size=15),	
	)
	fig = go.Figure(data=data, layout=layout)
	py.image.save_as(fig, filename=staticPath+'ageTierPlot.png')

def initiateDf():
	# plotly.tools.set_credentials_file(username='kasrazahir', api_key='hvEWprL4cY9DDtgkhp3U')
	plotly.tools.set_credentials_file(username='kasra.zahir', api_key='p04mrpvEHUM1994TQbbP')
	global FY
	FY = pd.read_excel("./uploads/data.xlsx").set_index('Id#')

	columns = [
		'Service',
		'Service Line Group',
		'Service Line',
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
	FY.rename(columns={'Total Estimated Revenue': 'TR', 'Sales Stage':'stage'}, inplace=True)

	# FY['TR'] = FY['TR'].str.replace(r'[$,]', '').astype('float')
	FY['stage'] = FY['stage'].map(lambda x: str(x)[:2])
	FY['stage'] = FY['stage'].astype(float)
	FY['stage'] = FY['stage'].replace(8, -2)
	FY['stage'] = FY['stage'].replace(7, -1)
	FY['Created'] = pd.to_datetime(FY['Created'])
	FY['Last Updated'] = pd.to_datetime(FY['Last Updated'])
	FY.loc[FY['Service Line']=='Oracle', 'line']='Oracle'
	FY.loc[FY['Service Line']=='SAP', 'line']='SAP'
	FY.loc[FY['Service Line']=='Digital Customer', 'line']='DC'
	FY.loc[FY['Service Line']=='Analytics & Information Mgmt', 'line']='AIM'
	FY.loc[FY['Service Line']=='Digital Integration', 'line']='DI'
	FY.loc[FY['Service Line']=='Application ManagementServices', 'line']='AMS'
	FY.loc[FY['Service Line'].str.split('-').str[0] =='TSA ', 'line']='TS&A'

	return FY

def initiateTech(FY, dt):
	global FYTech
	FYTech = (FY[FY['Service Line Group'] == 'Technology'][FY['Close Period'] >= dt["yearBegin"]]).copy()
	return FYTech

plots = [
 {"type":"pipe", "function": pipePlots, "category": "area", "desc": "Full Pipeline"},
 {"type":"sl", "function": slPlot, "category": "bar", "desc": "Service Lines"},
 {"type":"dealSize", "function": dealSizePlot, "category" : "pie", "desc": "Deal Size Tiers"},
 {"type":"closeReason", "function": closeReasonPlot, "category": "pie", "desc": "Persuit Outcomes"},
 {"type":"averageAge", "function": averageAgePlot,  "category": "bar",  "desc": "Entry Age"},
 {"type":"summary", "function": summaryTable, "category": "table", "desc": "Summary Table" },
 {"type":"keyDeals", "function": keyDeals,  "category": "table", "desc": "Key Deals"}
]

plots4 = [
 # {"type":"summary", "function": pipePlots, "category": "table", "desc": "Summary Table" },
 # {"type":"averageAge", "function": averageAgePlot,  "category": "bar",  "desc": "Entry Age"},

 # {"type":"averageAge", "function": averageAgePlot,  "category": "bar",  "desc": "Entry Age"},
 {"type":"summary", "function": summaryTable, "category": "table", "desc": "Full Pipeline" },
#  {"type":"summary2", "function": summaryTable, "category": "pie", "desc": "Persuit Outcomes" },
#  {"type":"summary3", "function": summaryTable, "category": "area" , "desc": "Summary Table" },
#  {"type":"ageTier", "function": averageAgePlot, "category": "area", "desc": "Key Deals"},
]

def plotIt(type):
	# db.csv has the year and month of this period
	dateDf = pd.read_csv(staticPath+"db.csv",index_col=[0])
	yearValue = dateDf['thisPeriodYear'].values[0]
	monthValue = dateDf['thisPeriodMonth'].values[0]
	yearBegin = str(yearValue)+" - 01"
	yearEnd = str(yearValue)+" - 13"
	if( monthValue > 9 ):
		thisPeriod = str(yearValue)+" - "+str(monthValue)
	else:
		thisPeriod = str(yearValue)+" - 0"+str(monthValue)

	if (monthValue > 6):
		NinetyDayEnd = str(yearValue)+" - "+str(monthValue+3)
	else:
		NinetyDayEnd = str(yearValue)+" - 0"+str(monthValue+3)
	beginningDate = datetime(2017, 6, 4, 0, 0)+timedelta(days=int(364*(yearValue-2018)))
	periodDate = beginningDate + timedelta(days=int(28*(monthValue-1)))

	dt = {"yearBegin":yearBegin, "yearEnd":yearEnd,"thisPeriod":thisPeriod,"NinetyDayEnd":NinetyDayEnd,"beginningDate":beginningDate,"periodDate":periodDate}
	print("Setting Dates:", dt)

	global FY
	FY = initiateDf()
	global FYTech
	FYTech = initiateTech(FY, dt)
	list(filter(lambda x : x['type'] == type, plots))[0]['function'](FYTech, dt)

plotIt("summary")
