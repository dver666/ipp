#!/usr/bin/env python

# file selector

"""
No LazyNamespace...

Warning (from warnings module):
  File "/home/diver/Desktop/gtk-tut-python/interactivefilesel.py", line 77
    self.filew=gtk.FileSelection("File Selection")
DeprecationWarning: use gtk.FileChooserDialog

Warning (from warnings module):
  File "/home/diver/Desktop/gtk-tut-python/interactivefilesel.py", line 85
    self.filew.set_filename("penguin.png")
DeprecationWarning: use gtk.FileChooserDialog
"""

import pygtk
pygtk.require("2.0")
import gtk
gtk.set_interactive(True)

if hasattr('_gtk','_lazyutils'):
    ns=LazyNamespace(gtk,locals())
    ns.add_submodule('glade','_glade')
    ns.add_submodule('_gtk','gtk._gtk')
    sys.modules['gtk']=ns
    sys.modules['gtk.glade']=LazyModule('_glade',{})
else:
    print("No LazyNamespace...")
    # gtk.set_interactive(True)

class FileSelectionExample:
    #  delete event message
    def delete_event(self,widget,event,data=None):
        print "delete event occured"
        return False

    # Close down and exit handler
    def destroy(self,widget,data=None):
        gtk.main_quit()

    # emitted when the user selects a file
    def file_set_cb(self,w):
        self.fcb.get_focus_on_click()
        print "selected: %s"%self.fcb.get_filename()
        return True

    # 
    # def selection_changed_cb(self,w):
    #    self.fcb.get_focus_on_click()
    #    print "selection changed to: "%self.fcw.select_file()
    #    return True

    # event handler
    def area_event(self,widget,event):
        handled=False

        # File Choooser Widget
        self.fcw=gtk.FileChooserWidget()
        self.fcw.set_local_only(True)
        self.fcw.set_preview_widget_active(True)
        self.fcw.connect("event",\
                         self.area_event)

    # Close down and exit handler
    def destroy_window(self,widget,event):
        gtk.main_quit()
        return True

    def __init__(self):
        window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("File Selection")
        window.set_resizable(True)
        window.connect("delete_event",\
                       self.destroy_window)
        window.connect("destroy",\
                       self.destroy)
        self.vbox=gtk.VBox(False,0)
        window.add(self.vbox)
        self.vbox.show()

        # Area with File Chooser button
        self.fcb=gtk.FileChooserButton('Select a File')
        self.fcb.set_width_chars(len(self.fcb.get_title())*2)
        self.fcb.connect("file-set",\
                         self.file_set_cb)
        self.vbox.pack_start(self.fcb,\
                             True,\
                             True,\
                             0)
        self.hbox=gtk.HBox(False,0)
        self.vbox.add(self.hbox)
        self.hbox.show()
        self.fcb.show()

        # Quit button
        self.button=gtk.Button(stock=gtk.STOCK_QUIT)
        self.button.connect_object("clicked",\
                                   gtk.Widget.destroy,\
                                   window)
        self.vbox.pack_start(self.button,\
                             True,\
                             True,\
                             0)
        self.hbox=gtk.HBox(False,0)
        self.vbox.add(self.hbox)
        self.hbox.show()
        self.button.show()
        window.show()

    def main(self):
        gtk.main()

if __name__=="__main__":
    fc=FileSelectionExample()
    fc.main()
