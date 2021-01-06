import tkinter as tk
#from autobw import showTraffic, urlid
from time import gmtime, strftime, localtime
import os

import requests
import sys
import xml.etree.cElementTree as ET
import re
from time import gmtime, strftime, localtime

#url's
prtgurl = 'http://mrtg.equitel.com.bd'
xmlurl = 'http://mrtg.equitel.com.bd/api/table.xml?&content=values&sortby=-datetime&display=extendedheaders&varexpand=tabletitle&tabletitle=Sensor%20Data&graphid=0&columns=datetime%2Cvalue_%2Ccoverage%2Cobjid%2Cbaselink&id='
urlid = [
{'id':'7563', 'name': 'IIG T'},
{'id':'7564', 'name': 'F@H P'},
{'id':'7566', 'name': 'F@H S'},
{'id':'7558', 'name': 'BSCCL'},
{'id':'7760', 'name': 'IDS P'},
{'id':'7762', 'name': 'IDS S'},
{'id':'7747', 'name': 'BT ISP T'},
{'id':'3923', 'name': 'BT-MGMT'},
{'id':'8041', 'name': 'Novo DCS'},
{'id':'8037', 'name': 'NOVO Nix'},
{'id':'8236', 'name': 'IDS FB'},
{'id':'8221', 'name': 'BDIX'}]


#{'id':'4328', 'name': 'BT ISP DCS'},]

#get time
datetime = strftime('%d-%m-%y : %I:%M %p',localtime())


def showTraffic (urlid):
	login_data = dict(username='!!!!!', password='!!!!!!')
	session = requests.session()
	session.post(prtgurl, data=login_data)
	#print('Login Successful')


	super_string =[]
	bw =''
	#Fetch the raw xml data
	for i in urlid:
		xmldata = session.get(xmlurl + i['id'])
		f = open('table.xml','w')
		f.write(xmldata.text)
		#print('Acquired raw xml data')
		f.close();
		session.close()


        #XML Manipulation

		tree = ET.parse('table.xml')
		root = tree.getroot()
		inelements = []
		outelements = []

		for elemin in root.iter('value'): 
			if elemin.attrib['channel']=='Traffic In (speed)':
				str1=elemin.text.replace(',','')
				if str1 == 'Error':
					numin=[0]
				else:
					if str1.find('.')==-1:
						numin = re.findall("\d+", str1)
						numin = list(map(int,numin))
					else:
						numin = re.findall("\d+\.\d+", str1)
						numin = list(map(float,numin))
						 
				inelements.append(numin)



		for elemout in root.iter('value'):
			if elemout.attrib['channel']=='Traffic Out (speed)':
				str2=elemout.text.replace(',','')
				if str2 == 'Error':
					numout = [0]
				else:
					if str2.find('.')==-1:
						numout = re.findall("\d+", str2)
						numout = list(map(int,numout))
					else:
						numout = re.findall("\d+\.\d+", str2)
						numout = list(map(float,numout))
						 
				outelements.append(numout)

 
		maxin =  max(inelements[:60])
		maxout = max(outelements[:60])
		  
		avin = maxin[0]; 
		avout = maxout[0] ;
		naame = i['name']

		# if naame == 'BT-MGMT':
		# bw = "Gi 0/50  (OH by Tips) : " + str(v1.get()) +"\n" + "Gi 0/52  (OH-Aknet) : " + str(v2.get())
		# super_string.append(bw)

		bw = '\n'+naame+' - '+str(avin)+'/'+str(avout)+' Mbps'
		super_string.append(bw)

		if naame == 'BT-MGMT':
			bw = '\n'+ "Gi 0/50  (OH by Tips) : " + str(v1.get()) +"\n" + "Gi 0/52  (OH-Aknet) : " + str(v2.get())
		super_string.append(bw)
		#print(bw) 
		#print (i['name'],':',avin,'/',avout,'Mbps')


 

		return super_string

def refresh():
#super_string=''

	box.delete(1.0,tk.END)

def bandw():
	refresh()
	super_string = showTraffic(urlid)
 
	datetime = strftime('%d-%m-%y : %I:%M %p',localtime())
	box.insert(1.0,datetime)
	for i in super_string:
		box.insert(tk.END,i)

		box.insert(tk.END,"\n")
# box.insert(tk.END,press1())
# box.insert(tk.END,press2())

		box.insert(tk.END,"\n")
		box.insert(tk.END,"\n")
		box.insert(tk.END,"BR/")
		box.insert(tk.END,"\n")
		box.insert(tk.END,get_text())


 
 
 

 
 

def copy():
	window.clipboard_clear()
	window.clipboard_append(box.get("1.0","end-1c"))



def press1():
	c1 = "Gi 0/50  (OH by Tips) : " + str(v1.get()) +"\n"
	return c1

def press2():
	c2 = "Gi 0/52  (OH-Aknet) : " + str(v2.get())
	return c2

def get_text():
	b = l.get()
	return b

#define window
window = tk.Tk()
window.configure(background = "#444444")
window.geometry('900x700')
window.title('BANDWIDTH GENERATOR')
window.resizable(0,0)



label = tk.Label(text="Bandwidth Report Generator",
foreground = "darkorange",
background= "#444444",
width= 70,
height = 5)
label.config(font=("Subway",20))
label.pack(fill = tk.X)

ll = u"\u00a9" + "2020 Tanzil Bin Hassan"

g = tk.Label(text = ll,font=("Courier", 6), background = '#f4d47c').pack()

#defining Frames
frame_left = tk.Frame(window)
frame_left.configure(background = '#444444')
frame_left.pack(side = tk.LEFT)

frame_right = tk.Frame(window)
frame_right.configure(background = '#444444')
frame_right.pack(side = tk.RIGHT)

frame_bottom = tk.Frame(window)
frame_bottom.pack(side=tk.BOTTOM)

#creating form:
v1 = tk.StringVar()
v1.set("Up")

v2 = tk.StringVar()
v2.set("Up")

# image1 = tk.PhotoImage(file='generate.png')
# image2 = tk.PhotoImage(file='refresh.png')
# image3 = tk.PhotoImage(file='copy.png')


k = tk.Label(frame_left, text = "Engineer Name:", fg = "darkorange", bg= '#444444')
k.config(font=("Courier", 15))
k.pack(pady =5,padx = 10)
l = tk.Entry(frame_left,width =15, font= ("Courier", 20), background= '#f4d47c', justify= "center" )
l.pack(pady =5, padx= 20)




a = tk.Label(frame_left, text = "Gi 0/50(OH by Tips)[UP/DOWN]",font=("Courier", 15), fg = "darkorange", bg= '#444444')

a.pack(pady= 5)
R1 = tk.Radiobutton(frame_left, text="Up", variable=v1,value="Up", command = press1,font=("Courier", 15), background = '#444444' , fg= "darkorange" ).pack()
R2 = tk.Radiobutton(frame_left, text="Down", variable=v1,value="Down" , command = press1,font=("Courier", 15),background = '#444444' , fg= "darkorange").pack()


b = tk.Label(frame_left, text = "Gi 0/52(OH-Aknet)[UP/DOWN]",font=("Courier", 15),fg = "darkorange", bg= '#444444').pack()
R3 = tk.Radiobutton(frame_left, text="Up", variable=v2,value="Up", command = press2,font=("Courier", 15),background = '#444444' , fg= "darkorange" ).pack()
R4 = tk.Radiobutton(frame_left, text="Down", variable=v2,value="Down" , command = press2,font=("Courier", 15),background = '#444444' , fg= "darkorange").pack()



box = tk.Text(frame_right, font=("Courier", 15))
box.config(height=20, width=65, bg="#f4d47c")
box.pack(padx = (0,20), pady = 2)

#Gen Button
button = tk.Button(frame_left,
    text="Generate",
    width=10,
    height=5,
    bg="green",
    fg="yellow",
    borderwidth=0,
    font = ("Courier", 12, 'bold'),
    #image = image1, 
    command = bandw)
button.pack(side = tk.LEFT, padx = 20, pady = 100)


btn = tk.Button(frame_left,
	text = "Refresh",
	width = 10,
	height = 5,
	bg = "maroon",
	fg = "white",
	borderwidth=0,
	font = ("Courier", 12, 'bold'),
	#image = image2,
	command = refresh)

btn.pack(side = tk.LEFT, padx = 20, pady =100)

btn1 = tk.Button(frame_left,
	text = "Copy",
	width = 10,
	height = 5,
	bg = "#223280",
	borderwidth=0,
	font = ("Courier", 12, 'bold'),
	#image = image3,
	command = copy)
btn1.pack(side = tk.LEFT, padx = 20, pady = 100)





window.update()




window.mainloop()