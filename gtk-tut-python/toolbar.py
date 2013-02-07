#!/usr/bin/env python

import pygtk
pygtk.require("2.0")
import gtk

"""
Warning (from warnings module):
  File "/home/diver/Desktop/gtk-tut-python/toolbar.py", line 52
    self.delete_event)
DeprecationWarning: 

Warning (from warnings module):
  File "/home/diver/Desktop/gtk-tut-python/toolbar.py", line 53
    toolbar.append_space()
DeprecationWarning: 

Warning (from warnings module):
  File "/home/diver/Desktop/gtk-tut-python/toolbar.py", line 64
    toolbar)
DeprecationWarning: 

Warning (from warnings module):
  File "/home/diver/Desktop/gtk-tut-python/toolbar.py", line 65
    toolbar.append_space()
DeprecationWarning: 

Warning (from warnings module):
  File "/home/diver/Desktop/gtk-tut-python/toolbar.py", line 77
    toolbar)
DeprecationWarning: 

Warning (from warnings module):
  File "/home/diver/Desktop/gtk-tut-python/toolbar.py", line 78
    toolbar.append_space()
DeprecationWarning: 

Warning (from warnings module):
  File "/home/diver/Desktop/gtk-tut-python/toolbar.py", line 90
    toolbar)
DeprecationWarning: 

Warning (from warnings module):
  File "/home/diver/Desktop/gtk-tut-python/toolbar.py", line 91
    toolbar.append_space()
DeprecationWarning: 

Warning (from warnings module):
  File "/home/diver/Desktop/gtk-tut-python/toolbar.py", line 104
    toolbar)
DeprecationWarning: 

Warning (from warnings module):
  File "/home/diver/Desktop/gtk-tut-python/toolbar.py", line 105
    toolbar.append_space()
DeprecationWarning: 

Warning (from warnings module):
  File "/home/diver/Desktop/gtk-tut-python/toolbar.py", line 112
    "Private")
DeprecationWarning: 
"""

class ToolbarExample:
    def delete_event(self,widget,event=None):
        gtk.main_quit()
        return False

    def radio_event(self,widget,toolbar):
        if self.text_button.get_active():
            toolbar.set_style(gtk.TOOLBAR_TEXT)
        elif self.icon_button.get_active():
            toolbar.set_style(gtk.TOOLBAR_ICONS)
        elif self.both_button.get_active():
            toolbar.set_style(gtk.TOOLBAR_BOTH)

    def toggle_event(self,widget,toolbar):
        toolbar.set_tooltips(widget.get_active())
    
    def __init__(self):
        dialog=gtk.Dialog()
        dialog.set_title("GTK Toolbar Tutorial")
        dialog.set_size_request(650,\
                                250)
        dialog.set_resizable(True)

        dialog.connect("delete-event",\
                       self.delete_event)

        handlebox=gtk.HandleBox()
        dialog.vbox.pack_start(handlebox,\
                               False,\
                               False,\
                               5)

        toolbar=gtk.Toolbar()
        toolbar.set_orientation(gtk.ORIENTATION_HORIZONTAL)
        toolbar.set_style(gtk.TOOLBAR_BOTH)
        toolbar.set_border_width(5)
        handlebox.add(toolbar)

        iconw=gtk.Image()
        iconw.set_from_file("/usr/share/app-install/icons/gtkhash.xpm")
        close_button=toolbar.append_item("Close",\
                                         "Closes this app",\
                                         "Private",\
                                         iconw,\
                                         self.delete_event)
        toolbar.append_space()
        
        iconw=gtk.Image()
        iconw.set_from_file("/usr/share/app-install/icons/gtkhash.xpm")
        icon_button=toolbar.append_element(gtk.TOOLBAR_CHILD_RADIOBUTTON,\
                                           None,\
                                           "Icon",\
                                           "Only icons in toolbar",\
                                           "Private",\
                                           iconw,\
                                           self.radio_event,\
                                           toolbar)
        toolbar.append_space()
        self.icon_button=icon_button

        iconw=gtk.Image()
        iconw.set_from_file("/usr/share/app-install/icons/gtkhash.xpm")
        text_button=toolbar.append_element(gtk.TOOLBAR_CHILD_RADIOBUTTON,\
                                           icon_button,\
                                           "Text",\
                                           "Only texts in toolbar",\
                                           "Private",\
                                           iconw,\
                                           self.radio_event,\
                                           toolbar)
        toolbar.append_space()
        self.text_button=text_button

        iconw=gtk.Image()
        iconw.set_from_file("/usr/share/app-install/icons/gtkhash.xpm")
        both_button=toolbar.append_element(gtk.TOOLBAR_CHILD_RADIOBUTTON,\
                                           text_button,\
                                           "Both",\
                                           "Icon and text in toolbar",\
                                           "Private",\
                                           iconw,\
                                           self.radio_event,\
                                           toolbar)
        toolbar.append_space()
        self.both_button=both_button
        both_button.set_active(True)

        iconw=gtk.Image()
        iconw.set_from_file("/usr/share/app-install/icons/gtkhash.xpm")
        tooltip_button=toolbar.append_element(gtk.TOOLBAR_CHILD_TOGGLEBUTTON,\
                                              None,\
                                              "Tooltips",\
                                              "Toolbar with or without tooltips",\
                                              "Private",\
                                              iconw,\
                                              self.toggle_event,\
                                              toolbar)
        toolbar.append_space()
        self.tooltip_button=tooltip_button
        tooltip_button.set_active(True)

        entry=gtk.Entry()
        toolbar.append_widget(entry,\
                              "This is just an entry",\
                              "Private")
        entry.show()
        toolbar.show()
        handlebox.show()
        dialog.show()

def main():
    gtk.main()
    return 0

if __name__=="__main__":
    ToolbarExample()
    main()
