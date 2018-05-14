

"""

Allows you to visualize the average user rating based on year, genre, or movie from a SQL server
that has had the IMDB TSV file loaded into it.
Written During Computation and Mindfulness 2018 TESC
Derick Falk

Currently the layout of the gui could be improved.

"""
from MySQLdb import *
from matplotlib import pyplot as plt
import numpy as np
import tkinter as tk


# Method to show the matplotlib plot for sql query
def showplot(xinfo,mode,hyear,lyear,title,xlabel,ylabel,yinfo):
	passw = <password>
	user = <user>
	host = <host>
	database = <database>

	extra = ''
	top10 = 'AVG(rating)'

	if mode == 'title':
		extra = 'LIMIT 10'
		top10='rating'
		title = f'Top 10 movies and/or Television from {lyear} to {hyear} with more than {yinfo} votes'
		ylabel = 'Rating'
		xlabel = 'Movies'
	elif mode=='genre':
		extra = 'LIMIT 10'
		title = f'Top 10 genres from {lyear} to {hyear} with more than {yinfo} Votes'
		ylabel = 'Average rating'
		xlabel = 'Genre'

		
	cnx = connect(user=user, password=passw,host=host,database=database)
	cursor = cnx.cursor()
	# Sets up pyplot figure
	fig = plt.figure('Movie Plot')
	fig.subplots_adjust(bottom=0.36)
	fig.set_figwidth(1000)
	fig.set_figheight(15)
	ax = fig.add_subplot(111)
	
	# This is the sql query
	result = cursor.execute('SELECT {}, {} FROM movies WHERE year <= {} \
		AND year >= {} AND num_votes >= {} GROUP BY {} ORDER BY rating DESC  {} ;'.format(xinfo,top10,hyear,lyear,yinfo,mode,extra))
	
	# Compares ten years of total number of votes
	data = []
	xTickMarks = []
	# Makes data usuable for pyplot by iterating through cursor object
	for row in cursor:
		data.append(row[1])
		xTickMarks.append(str(row[0]))
	ind = np.arange(len(data)) # x locations for the groups
	width = 0.35 # width of bars
	# Settings for histogram bars
	rects1 = ax.bar(ind, data, width,
	               color='black',
	               error_kw=dict(elinewidth=3,ecolor='red'))
	# Limits of x and y axises
	ax.set_xlim(-width,len(ind)+width)
	ax.set_ylim(0,10)
	# Sets the figure for the subplot
	ax.set_ylabel(ylabel)
	ax.set_xlabel(xlabel)
	ax.set_title(title)
	ax.set_xticks(ind)
	xtickNames = ax.set_xticklabels(xTickMarks)
	plt.setp(xtickNames, rotation=75, fontsize=10)
	plt.show()



# Puts values from gui into options dict whereby its used to send a query to movie database
def doplot():
	options['lyear'] = str(yrs_l.get())
	options['hyear'] = str(yrs_h.get())
	options['xinfo'] = u.get()
	options['yinfo'] = v.get()
	options['mode'] = u.get()
	try:
	showplot(**options)
	except:
		pass
# Some default values
options = {'xinfo':'year','mode':'year','hyear':'2020','lyear':'1960',
'xlabel':'Year','ylabel':'Average Rating','title':f'Average rating','yinfo':'100'}

root = tk.Tk()
root.wm_title('IMDB Plot')

# Labels for start year, end year
years_lbls = tk.Frame(root);
yrs_l_label = tk.Label(years_lbls,text='Start Year', anchor='w')
yrs_l_label.pack(side='left')
yrs_h_label = tk.Label(years_lbls,text='End Year', anchor='e')
yrs_h_label.pack(side='right')
years_lbls.pack()

# Spin boxes for start year, end year
years = tk.Frame(root)
yrs_l = tk.Spinbox(years,from_=1878, to=2018)
yrs_l.pack(side='left')
years.pack()
yrs_h = tk.Spinbox(years,from_=1879, to=2018)
yrs_h.pack(side='right')
print(yrs_l.get())


#Labels for X and Y
xy_labels = tk.Frame(root)
xinfo = tk.Label(xy_labels,text='X info')
xinfo.pack(side='left')
yinfo = tk.Label(xy_labels,text='Y info')
yinfo.pack(side='right')
xy_labels.pack()

#X and Y info 
#Basically what information are we comparing to what
x_info = tk.Frame(root)

u = tk.StringVar()
u.set('year')
tk.Radiobutton(x_info, text='Year',variable=u, value='year').pack(anchor='w')
tk.Radiobutton(x_info, text='Genre',variable=u, value='genre').pack(anchor='w')
tk.Radiobutton(x_info, text='Top10!',variable=u, value='title').pack(anchor='w')
x_info.pack(side = 'left')

y_info = tk.Frame(root)
v = tk.StringVar()
v.set('10000') 
tk.Radiobutton(y_info, text='Num_Votes > 100',variable=v, value='100').pack(anchor='w')
tk.Radiobutton(y_info, text='Num_Votes > 1000',variable=v, value='1000').pack(anchor='w')
tk.Radiobutton(y_info, text='Num_Votes > 10,000',variable=v, value='10000').pack(anchor='w')
tk.Radiobutton(y_info, text='Num_Votes > 100,000',variable=v, value='100000').pack(anchor='w')
y_info.pack(side='right')

plt_frm = tk.Frame(root) 
plt_button = tk.Button(plt_frm,text='Plot',command =lambda: doplot())
plt_button.pack()
plt_frm.pack()


root.mainloop()
