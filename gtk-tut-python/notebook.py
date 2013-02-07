#!/usr/bin/env python

#toolbar

import pygtk
pygtk.require("2.0")
import gtk

class NotebookExample:
    def rotate_book(self,button,notebook):
        notebook.set_tab_pos((notebook.get_tab_pos()+1)%4)

    def tabsborder_book(self,button,notebook):
        tval=False
        bval=False
        if self.show_tabs==False:
            tval=True
        if self.show_border==False:
            bval=True

        notebook.set_show_tabs(tval)
        self.show_tabs=tval
        notebook.set_show_border(bval)
        self.show_border=bval

    def remove_book(self,button,notebook):
        page=notebook.get_current_page()
        notebook.remove_page(page)
        notebook.queue_draw_area(0,\
                                 0,\
                                 -1,\
                                 -1)

    def delete(self,widget,event=None):
        gtk.main_quit()
        return False
    
    def __init__(self):
        window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.connect("delete-event",\
                       self.delete)
        window.set_border_width(10)
        
        table=gtk.Table(3,\
                        6,\
                        False)
        window.add(table)
        notebook=gtk.Notebook()
        notebook.set_tab_pos(gtk.POS_TOP)
        table.attach(notebook,\
                     0,\
                     6,\
                     0,\
                     1)
        notebook.show()
        self.show_tabs=True
        self.show_border=True

        for i in range(5):
            buff="Append Frame %d"%(i+1)
            bufl="Page %d"%(i+1)
            frame=gtk.Frame(buff)
            frame.set_border_width(10)
            frame.set_size_request(100,\
                                  75)
            frame.show()
            label=gtk.Label(buff)
            frame.add(label)
            label.show()
            label=gtk.Label(bufl)
            notebook.append_page(frame,\
                                 label)

        checkbutton=gtk.CheckButton("Check her please!")
        checkbutton.set_size_request(100,\
                                     75)
        checkbutton.show()
        label=gtk.Label("Add page")
        notebook.insert_page(checkbutton,\
                             label,\
                             2)

        for i in range(5):
            buff="Prepend Frame %d"%(i+1)
            bufl="PPage %d"%(i+1)

            frame=gtk.Frame(buff)
            frame.set_border_width(10)
            frame.set_size_request(100,\
                                  75)
            frame.show()
            label=gtk.Label(buff)
            frame.add(label)
            label.show()
            label=gtk.Label(bufl)
            notebook.append_page(frame,\
                                 label)

        notebook.set_current_page(3)
        
        button=gtk.Button("close")
        button.connect("clicked",\
                       self.delete)
        table.attach(button,\
                     0,\
                     1,\
                     1,\
                     2)
        button.show()
        
        button=gtk.Button("next page")
        button.connect("clicked",\
                       lambda w: notebook.next_page())
        table.attach(button,\
                     1,\
                     2,\
                     1,\
                     2)
        button.show()
        
        button=gtk.Button("prev page")
        button.connect("clicked",\
                       lambda w: notebook.prev_page())
        table.attach(button,\
                     2,\
                     3,\
                     1,\
                     2)
        button.show()
        
        button=gtk.Button("tab position")
        button.connect("clicked",\
                       self.rotate_book,\
                       notebook)
        table.attach(button,\
                     3,\
                     4,\
                     1,\
                     2)
        button.show()
        
        button=gtk.Button("tab/border on/off")
        button.connect("clicked",\
                       self.tabsborder_book,\
                       notebook)
        table.attach(button,\
                     4,\
                     5,\
                     1,\
                     2)
        button.show()
        
        button=gtk.Button("remove page")
        button.connect("clicked",\
                       self.remove_book,\
                       notebook)
        table.attach(button,\
                     5,\
                     6,\
                     1,\
                     2)
        button.show()
        
        table.show()
        window.show()

def main():
    gtk.main()
    return 0

if __name__=='__main__':
    NotebookExample()
    main()
