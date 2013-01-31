#!/usr/bin/env python

import gtk
import gtkmozembed

class TinyGecko:
    def __init__(self):
        self.moz=gtkmozembed.MozEmbed()

        win=gtk.Window()
        win.add(self.moz)
        win.show_all()
        self.moz.load_url('http://www.pygtk.org')

if __name__=='__main__':
    TinyGecko()
    gtk.main()
