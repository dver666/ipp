"""
python-gmenu an implementation of the
freedesktop menu specification for GNOME
http://www.freedesktop.org/Standards/menu-spec
http://standards.freedesktop.org/menu-spec/menu-spec-1.0.html
xdg-utils-1.0.2-1.tgz with testcode
xdg-utils under /usr/bin
xdg-desktop-icon
xdg-desktop-menu
xdg-email
xdg-icon-resource
xdg-mime
xdg-open
xdg-screensaver

Python has GMenuSimpleEditor
gmenu-simple-editor
/usr/share/applications/gmenu-simple-editor.desktop references
gnome-main-menu
gnome-main-menu.svg and
gnome-main-menu.png exist in /<theme>/places/<size>#

/usr/share/icons/HighContrastLargePrintInverse/48x48/places/gnome-main-menu.png
/usr/share/icons/Humanity/places/16/gnome-main-menu.svg
/usr/share/icons/Humanity/places/22/gnome-main-menu.svg
/usr/share/icons/Humanity/places/24/gnome-main-menu.svg
/usr/share/icons/Humanity/places/48/gnome-main-menu.svg
/usr/share/icons/Humanity/places/64/gnome-main-menu.svg
/usr/share/icons/Humanity-Dark/places/16/gnome-main-menu.svg
/usr/share/icons/Humanity-Dark/places/22/gnome-main-menu.svg
/usr/share/icons/Humanity-Dark/places/24/gnome-main-menu.svg
/usr/share/icons/Humanity-Dark/places/48/gnome-main-menu.svg
/usr/share/icons/Humanity-Dark/places/64/gnome-main-menu.svg
/usr/share/icons/gnome/16x16/places/gnome-main-menu.png
/usr/share/icons/gnome/22x22/places/gnome-main-menu.png
/usr/share/icons/gnome/24x24/places/gnome-main-menu.png
/usr/share/icons/gnome/32x32/places/gnome-main-menu.png
/usr/share/icons/gnome/scalable/places/gnome-main-menu.svg

except

/usr/share/icons/Humanity/places/32/
/usr/share/icons/Humanity-Dark/places/32/

some icons have corresponding .icon files but the following icon

/usr/share/icons/Humanity/places/48/neat.icon
does not have  corresponding .svg

/usr/share/icons/Humanity/places/22&24/start-here.svg is gray

"""

import optparse
import sys

import gmenu

def print_entry(entry,path):
    if entry.get_is_excluded():
        excluded=' <excluded>'
    else:
        excluded=''

    print '%s\t%s\t%s%s'%(path,\
                          entry.get_desktop_file_id(),\
                          entry.get_desktop_file_path(),\
                          excluded)

def print_directory(dir,parent_path=None):
    if not parent_path:
        path='/'
    else:
        path='%s%s/'%(parent_path,dir.get_name())

    for item in dir.get_contents():
        type=item.get_type()
        if type==gmenu.TYPE_ENTRY:
            print_entry(item,path)
        elif type==gmenu.TYPE_DIRECTORY:
            print_directory(item,path)
        elif type==gmenu.TYPE_ALIAS:
            aliased=item.get_item()
            if aliased.get_type()==gmenu.TYPE_ENTRY:
                print_entry(aliased,path)
        elif type in [gmenu.TYPE_HEADER,gmenu.TYPE_SEPARATOR]:
            pass
        else:
            print >> sys.stderr,'Unsupported item type: %s'%type

def main(args):
    parser=optparse.OptionParser()
    parser.add_option('-f',\
                      '--file',\
                      dest='file',\
                      help='Menu file')
    parser.add_option('-i',\
                      '--include-excluded',\
                      dest='exclude',\
                      action='store_true',\
                      default=False,\
                      help='Include <Exclude>d entries')
    parser.add_option('-n',\
                      '--include-nodisplay',\
                      dest='nodisplay',\
                      action='store_true',\
                      default=False,\
                      help='Include NoDisplay=true entries')

    (options,args)=parser.parse_args()

    if options.file:
        menu_file=options.file
    else:
        menu_file='applications.menu'

    flags=gmenu.FLAGS_NONE
    if options.exclude:
        flags |= gmenu.FLAGS_INCLUDE_EXCLUDED
    if options.nodisplay:
        flags |= gmenu.FLAGS_INCLUDE_NODISPLAY

    tree=gmenu.lookup_tree(menu_file,\
                           flags)
    root=tree.get_root_directory()

    if not root:
        print 'Menu tree is empty'
    else:
        print_directory(root)

if __name__ == '__main__':
    try:
      main(sys.argv)
    except KeyboardInterrupt:
      pass
