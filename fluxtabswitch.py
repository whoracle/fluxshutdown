import commands
import os
import gtk
"""
	wmctrl:
    Each window is 4-tuple: (id, desktop number, host, window title)
    
    Also: For fucks sake, document this ASAP
"""

def switchToWindow(widget, event, winID, buttons, windowArray, targetLabel):
	keyname = gtk.gdk.keyval_name(event.keyval)
	if "Alt" in keyname:
		print "mod"
		os.popen("wmctrl -i -a "+winID)
		gtk.main_quit()
	elif "Tab" in keyname:
		print "name"
		arraymax = len(buttons) - 1
		for i in range(0, len(buttons)):
			print "i: "+str(i)
			if widget == buttons[i]:
				if i < arraymax:
					print "set"
					target = buttons[i+1]
					targetLabel.set_text(windowArray[i+1][3])
					break
				elif i == arraymax:
					print "fin"
					target = buttons[0]
					targetLabel.set_text(windowArray[0][3])	
		target.grab_focus()

lines = commands.getoutput("wmctrl -d").split("\n")
desktops = []
for line in lines:
    line = line.replace("  ", " ")
    desktop = tuple(line.split(" ", 3))
    desktops.append(desktop)

lines = commands.getoutput("wmctrl -l").split("\n")
windows = []
for line in lines:
    line = line.replace("  ", " ")
    win = tuple(line.split(" ", 3))
    windows.append(win)

isPopulated = dict()
for desktop in desktops:
	isPopulated[desktop[0]] = False
	for win in windows:
		if win[1] == desktop[0]:
			isPopulated[desktop[0]] = True

tabWin = gtk.Window()
tabWin.set_decorated(False)
tabWin.set_skip_taskbar_hint(True)
tabWin.set_skip_pager_hint(True)

cols = 0
for desktop in isPopulated:
	if isPopulated[desktop] == True:
		cols = cols + 1
	else:
		desktops.remove(desktops[int(desktop)])

buttons = []
table = gtk.Table(3,cols,False)
table.set_col_spacings(10)
windowName = gtk.Label(windows[0][3])

for i in range(0, len(desktops)):
	table.attach(gtk.Label(desktops[i][3].split(" ")[6]),i,i+1,0,1,xpadding=5,ypadding=5)
	hbox = gtk.HBox()
	for win in windows:
		if win[1] == desktops[i][0]:
			button = gtk.Button("\n            \n")
			button.connect("key_release_event", switchToWindow, win[0], buttons, windows, windowName)
			button.set_relief(gtk.RELIEF_HALF)
			buttons.append(button)
	
	for button in buttons:
		hbox.pack_start(button)
	table.attach(hbox,i,i+1,1,2,xpadding=5,ypadding=5)

table.attach(windowName,0,cols,2,3,xpadding=5,ypadding=5)
tabWin.add(table)
tabWin.set_position(gtk.WIN_POS_CENTER)
tabWin.show_all()
gtk.main()
