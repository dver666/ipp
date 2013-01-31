#!/usr/bin/env python

import pygtk
pygtk.require("2.0")
import gtk,gobject

def progress_timeout(pbobj):
    if pbobj.activity_check.get_active():
        pbobj.pbar.pulse()
    else:
        new_val=pbobj.pbar.get_fraction()+0.01
        if new_val>1.0:
            new_val=0.0
        pbobj.pbar.set_fraction(new_val)

    return True

class ProgressBar:
    def toggle_show_text(self,widget,data=None):
        if widget.get_active():
            self.pbar.set_text("some text")
        else:
            self.pbar.set_text("")

    def toggle_activity_mode(self,widget,data=None):
        if widget.get_active():
            self.pbar.pulse()
        else:
            self.pbar.set_fraction(0.0)

    def toggle_orientation(self,widget,data=None):
        if self.pbar.get_orientation()==gtk.PROGRESS_LEFT_TO_RIGHT:
            self.pbar.set_orientation(gtk.PROGRESS_RIGHT_TO_LEFT)
        elif self.pbar.get_orientation()==gtk.PROGRESS_RIGHT_TO_LEFT:
            self.pbar.set_orientation(gtk.PROGRESS_LEFT_TO_RIGHT)

    def destroy_progress(self,widget,data=None):
        gobject.source_remove(self.timer)
        self.timer=0
        gtk.main_quit()

    def __init__(self):
        self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_resizable(True)

        self.window.connect("destroy",\
                            self.destroy_progress)
        
        self.window.set_title("ProgressBar")
        self.window.set_border_width(0)

        vbox=gtk.VBox(False,5)
        vbox.set_border_width(10)
        self.window.add(vbox)
        vbox.show()

        align=gtk.Alignment(0.5,\
                            0.5,\
                            0,\
                            0)
        vbox.pack_start(align,\
                        False,\
                        False,\
                        5)
        align.show()

        self.pbar=gtk.ProgressBar()

        align.add(self.pbar)
        self.pbar.show()

        self.timer=gobject.timeout_add(100,\
                                       progress_timeout,\
                                       self)

        separator=gtk.HSeparator()
        vbox.pack_start(separator,\
                        False,\
                        False,\
                        0)
        separator.show()

        table=gtk.Table(2,\
                        2,\
                        False)
        vbox.pack_start(table,\
                        False,\
                        True,\
                        0)
        table.show()

        check=gtk.CheckButton("Show text")
        table.attach(check,\
                     0,\
                     1,\
                     0,\
                     1,\
                     gtk.EXPAND|gtk.FILL,\
                     gtk.EXPAND|gtk.FILL,\
                     5,\
                     5)
        check.connect("clicked",\
                      self.toggle_show_text)
        check.show()

        self.activity_check=check=gtk.CheckButton("Activity mode")
        table.attach(check,\
                     0,\
                     1,\
                     1,\
                     2,\
                     gtk.EXPAND|gtk.FILL,\
                     gtk.EXPAND|gtk.FILL,\
                     5,\
                     5)
        check.connect("clicked",\
                      self.toggle_activity_mode)
        check.show()

        check=gtk.CheckButton("Right to Left")
        table.attach(check,\
                     0,\
                     1,\
                     2,\
                     3,\
                     gtk.EXPAND|gtk.FILL,\
                     gtk.EXPAND|gtk.FILL,\
                     5,\
                     5)
        check.connect("clicked",\
                      self.toggle_orientation)
        check.show()

        button=gtk.Button("close",\
                          gtk.STOCK_CLOSE)
        button.connect("clicked",\
                       self.destroy_progress)
        vbox.pack_start(button,\
                        False,\
                        False,\
                        0)

        button.set_flags(gtk.CAN_DEFAULT)
        
        button.grab_default()
        button.show()
        
        self.window.show()

    def main(self):
        # this still hangs until force quit gets to the decorator
        gtk.main()
        return 0

if __name__=="__main__":
    progressbar=ProgressBar()
    progressbar.main()
