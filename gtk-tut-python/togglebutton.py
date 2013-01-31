#!/usr/bin/env python

import pygtk
pygtk.require("2.0")
import gtk

class ToggleButton:
    def callback(self,widget,data=None):
        print "%s was toggled %s"%(data,\
                                   ("OFF","ON")\
                                   [widget.get_active()])

    def delete_event(self,widget,event,data=None):
        gtk.main_quit()
        return False

    def __init__(self):
        self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Toggle Button")

        self.window.connect("delete_event",\
                            self.delete_event)

        self.window.set_border_width(20)
        vbox=gtk.VBox(True,2)
        self.window.add(vbox)
        
        button=gtk.ToggleButton("toggle button 1")

        button.connect("toggled",\
                       self.callback,\
                       "toggle button 1")
        
        vbox.pack_start(button,\
                        True,\
                        True,\
                        2)
        button.show()
        
        button=gtk.ToggleButton("toggle button 2")

        button.connect("toggled",\
                       self.callback,\
                       "toggle button 2")
        
        vbox.pack_start(button,\
                        True,\
                        True,\
                        2)
        button.show()
        
        button=gtk.Button("Quit",\
                          gtk.STOCK_QUIT)

        button.connect("clicked",\
                       lambda w: gtk.main_quit())

        vbox.pack_start(button,\
                        True,\
                        True,\
                        2)
        button.show()
        
        vbox.show()
        self.window.show()

def main():
    gtk.main()
    return 0

if __name__=="__main__":
    ToggleButton()
    main()
