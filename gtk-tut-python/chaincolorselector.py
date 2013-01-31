#!/usr/bin/env python

# chain of responsiblity

import pygtk
pygtk.require("2.0")
import gtk

class Event:
    def __init__(self,name):
        self.name=name

class Widget:
    def __init__(self,parent=None):
        self.__parent=parent

    def Handle(self,event):
        handler='Handle_'+event.name
        if hasattr(self,handler):
            method=getattr(self,handler)
            method(event)
        elif self.__parent:
            self.__parent.Handle(event)
        elif hasattr(self,'HandleDefault'):
            self.HandleDefault(event)

class MainWindow(Widget):
    def Handle_close(self,event):
        print('MainWindow: '+event.name)

    def HandleDefault(self,event):
        print('SendDialog:'+event.name)

class SendDialog(Widget):
    def Handle_paint(self,event):
        print('SendDialog: '+event.name)

class MsgText(Widget):
    def Handle_down(self,event):
        print('MsgText: '+event.name)

class ChainColorSelector(Widget):
    """
        chaincolorselector.py demonstrates the use of the ColorSelectionDialog.
        The program displays a window containing a drawing area. Clicking on
        it opens a color selection dialog and changing the color in the color
        selection dialog changes the background color

        I need a tab in IDLE options configDialog that will set the
        IDLE frame color and menu font color.
        I can inherit from tklib tkColorChooser.py class which inherits from
        tk-libs DialogBox. Next I will extend configDialog.py so it shows the
        new tab.
    """

    #  delete event message
    def delete_event(self,widget,event,data=None):
        print "delete event occured"
        return False

    # Close down and exit handler
    def destroy(self,widget,data=None):
        gtk.main_quit()

    # connect handler for clicked event
    def show_help_cb(self,widget):
        # print "show-help signal"
        gtk.gtk_tooltips_data_get()
        return True
    
    # Color changed handler
    def color_changed_cb(self,widget):
        # Get drawingarea colormap
        colormap=self.drawingarea.get_colormap()
        # Get current color
        color=self.ccdial.colorsel.get_current_color()
        # Set window background color
        self.drawingarea.modify_bg(gtk.STATE_NORMAL,\
                                   color)

    # Drawingarea event handler
    def area_event(self,widget,event):
        handled=False

        # Check we received event
        if event.type==gtk.gdk.BUTTON_PRESS:
            handled=True

            # Create color selection dialog
            if self.ccdial==None:
                # color selection dialog constructor
                self.ccdial=gtk.ColorSelectionDialog("Select Background Color")
                
            # Get the ColorSelection widget
            colorsel=self.ccdial.colorsel
            
            colorsel.set_has_opacity_control(True)
            colorsel.set_previous_color(self.color)
            colorsel.set_current_color(self.color)
            colorsel.set_has_palette(True)

            # Connect to the color_changed signal
            colorsel.connect("color_changed",\
                             self.color_changed_cb)

            # get help_button property
            help_button=self.ccdial.help_button
            # connect help_button to callback
            help_button.connect("clicked",\
                                self.show_help_cb)
            help_button.set_flags(gtk.CAN_DEFAULT)
            help_button.grab_default()
            # show button
            help_button.show()

            # Show the dialog
            response=self.ccdial.run()

            if response==gtk.RESPONSE_OK:
                #print "It is RESPONSE_OK"
                self.color=colorsel.get_current_color()
            elif response==gtk.RESPONSE_CANCEL:
                #print "It is RESPONSE_CANCEL"
                self.drawingarea.modify_bg(gtk.STATE_NORMAL,\
                                           self.color)
            elif response==gtk.RESPONSE_HELP:
                print "It is RESPONSE_HELP"
                self.drawingarea.modify_bg(gtk.STATE_NORMAL,\
                                           self.color)
            else:
                print response
                self.drawingarea.modify_bg(gtk.STATE_NORMAL,\
                                           self.color)

            self.ccdial.hide()

        return handled

    # Close down and exit handler
    def destroy_window(self,widget,event):
        gtk.main_quit()
        return True

    def __init__(self):
        self.ccdial=None
        window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Color Selection Test Widget")
        window.set_resizable(True)
        
        window.connect("delete_event",\
                       self.destroy_window)
        window.connect("destroy",\
                       self.destroy)

        self.vbox=gtk.VBox(False,0)
        window.add(self.vbox)
        self.vbox.show()

        # Drawing Area
        self.drawingarea=gtk.DrawingArea()
        self.color=self.drawingarea.get_colormap().alloc_color(0,\
                                                               65535,\
                                                               0)
        self.drawingarea.set_size_request(200,200)
        self.drawingarea.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.drawingarea.connect("event",\
                                 self.area_event)
        self.vbox.pack_start(self.drawingarea,\
                             True,\
                             True,\
                             0)
        self.hbox=gtk.HBox(False,0)
        self.vbox.add(self.hbox)
        self.hbox.show()
        self.drawingarea.show()
        
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
        
        self.button.set_flags(gtk.CAN_DEFAULT)
        self.button.grab_default()
        self.button.show()
        window.show()

    def main(self):
        gtk.main()

if __name__=="__main__":
    ccs=ChainColorSelector()
    ccs.main()
