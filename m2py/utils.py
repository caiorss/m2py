# -*- coding: utf-8 -*-
"""
file: utils.py

Compilation of useful python routines and classes.


    * printc(*args)
        Print colored texts in Unix Terminal emulators

    * run_example(code)
        Run each line of code example and print line and output.

    * run_block(code)
        Run code block and display its output

    * notify(message)
        Print user notification message (works only on Linux)

"""

import sys
import os
import inspect
from subprocess import Popen, PIPE
from io import StringIO
import re

joinpath = os.path.join
abspath  = os.path.abspath


platform = sys.platform


    
class Container(dict):
    """
    An improved doted dictionary class.

    Examples:
    ---------------------------------
    >>> cont = Container()
    >>> cont['a'] = 10.23
    >>> cont.a
    10.23
    >>>
    >>> cont.b = "hello world"
    >>>
    >>> cont.keys()
    ['a', 'b']
    >>>
    >>> cont.get('a')
    10.23
    >>> cont.get('b')
    'hello world'
    >>> cont.set('hello', 'world')
    >>> cont.hello
    'world'


    >>> c = Container(x=10, y=40)
    >>> c
    {'x': 10, 'y': 40}

    >>> c.x
    10
    >>> c.y
    40

    """

    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)

    def set(self, key, value):
        self[key] = value
#        self.__keys__.append(key)

    def save(self, filename):
        """
        Save dictionary content to a file
        """
        import shelve
        s = shelve.open(filename)
        s['container_data'] = list(self.items())
        s.close()

    @classmethod
    def load(cls, filename):
        """
        Load dictionary content from a file
        """
        import shelve
        s = shelve.open(filename)
        items = s['container_data']

        #print "items = ", items

        c = Container(**dict(items))
        return c
        #for k, v in items:
        #    self[k] = v
        s.close()

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value


# Colors ANSI format
# Works in Linux Only
Colors = Container(
    BLACK = "\033[0;30m",
    BLUE = "\033[0;34m",
    WHITE = "\033[0;37m",
    GREEN = "\033[0;32m",
    CYAN = "\033[0;36m",
    RED = "\033[0;31m",
    YELLOW = "\033[0;33m",
    MAGNETA = "\033[0;35m",
    BOLD = "\033[1m",
    # BACKGROUNDS,
    BG_BLACK = "\033[0;40m",
    BG_BLUE = "\033[0;44m",
    BG_WHITE = "\033[0;41m",
    BG_GREEN = "\033[0;42m",
    BG_CYAN = "\033[0;46m",
    BG_RED = "\033[0;41m",
    BG_YELLOW = "\033[0;43m",
    BG_MAGNETA = "\033[0;45m",
    BG_BOLD = "\033[4m",
)


def lookup_dict(dic, val):
    """
    Get key, ==> dic[key] = val

    :param dic:   Dictionary
    :param val:   Value to be looked up
    :return:      Dictionary key which value is val
    :type dic: dict
    """
    for k in list(dic.keys()):
        if val == dic[k]:
            return k

    return None


def sort_tuple_list(lst, col):
    """
    :param lst: List of tuples
    :param col: Column number of tuple

    Example:

    x = [
    ("Person 1",10),
    ("Person 2",8),
    ("Person 3",12),
    ("Person 4",20)]

    In [21]: sort_tuple_list(x, 1)
    Out[21]: [('Person 2', 8), ('Person 1', 10), ('Person 3', 12), ('Person 4', 20)]

    In [22]: sort_tuple_list(x, 0)
    Out[22]: [('Person 1', 10), ('Person 2', 8), ('Person 3', 12), ('Person 4', 20)]
    """
    import operator
    lst.sort(key=operator.itemgetter(col))
    return lst


def sort_columns_by_column(lst, colindex):
    sorted = sort_tuple_list(list(zip(*lst)), colindex)
    return list(zip(*sorted))

#------------------------------------#
#     STRING MANIPULATION            #
#------------------------------------#

def joinstr(seq, sep=" "):
  """ Join strings str.join() is annoying """
  return sep.join(str(x) for x in seq)

def schar(char, idx, string):
    """
    Substitute character of idx position
    by character char

    :param char: Character
    :param idx:  Character index
    :param string: String to be susbstituted.
    :type char: str
    :type idx:  int
    :type string: str
    :return: string[idx] = char
    :rtype: str
    """
    return string[:idx] + char + string[idx+1:]

def loadconfig(filename, separator="=", comment_symbol="#"):
    """
    :param filename:        Filename to be parsed
    :param separator:       Separtor between entry
    :param comment_symbol:  Comment symbol
    :return:                Dictionary containing the entries and values in config file.
    :type  filename:        str
    :type  separator:       str
    :type  comment_symbol:  str
    :type return: dict

    Parse a configuration file like:

            # Storage directory
            STORAGE  = ./storage
            DATABASE = zotero.sqlite
            PORT = 8080
            HOST = 0.0.0.0
            LOGFILE = /tmp/zotero.log

    and returns:

    {'LOGFILE ': ' /tmp/zotero.log', 'STORAGE  ': ' ./storage', 'DATABASE ...}


    """
    import re
    text = open(filename).read()

    entry_pattern = re.compile("(.*)%s(.*)" % separator)
    line_comment_pattern = re.compile("%s.*" % comment_symbol, re.M)

    _text= line_comment_pattern.sub("", text)
    _test = _text

    data = entry_pattern.findall(_text)
    #data = [(k.strip(), v.strip()) for k,v in data]
    Config = Container()

    for k, v in data:
        Config.set(k.strip(), v.strip())

    #return dict(data)
    return Config

def load_yaml_string(yamlstring):
    """
    Load Yaml string and return a dictionary.
    
    :param yamlstring:  String containing yaml configuration
    :return:            Dictionary of yaml string
    :rtype:             dict
    """
    import yaml
    import io
    output = io.StringIO()
    output.write(yamlstring)

    data= yaml.safe_load(output.getvalue())
    output.close()
    return data
    
def load_yaml_file(yamlfile):
    """"
     Load Yaml file and return a dictionary.
    
    :param yamlfile:    Filename containing yaml configuration
    :return:            Dictionary of yaml string
    :rtype:             dict
    """
    import yaml
    with  open(yamlfile, 'r') as f:
        data= yaml.load(f)
    return data

def load_json_file(jsonfile):
    """
     Load json file and return a dictionary.

    :param jsonfile:    Filename containing yaml configuration
    :return:            Dictionary of yaml string
    :rtype:             dict
    """
    import json
    with  open(jsonfile, 'r') as f:
        data= json.load(f)
    return data


#-----------------------------#
#  OPERATING SYSTEM FUNCTIONS #
#-----------------------------#


def run(cmd, stdin=None, p=False):

    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return "\n".join(p.communicate(stdin)).strip('\n')

def execute(commands, nowait=False):
    """
    Execute shell command and get output
    """
    from subprocess import Popen, PIPE


    if isinstance(commands, list):
        commands = " ".join(commands)

    p = Popen(commands, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    if not nowait:
        out, err = p.communicate()
        return out + '\n' + err
    else:
        return None



def mkdir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def get_hostname():
    import platform; 
    return platform.uname()[1]
    

def set_proc_name(newname):

    if not is_linux():
        return
    from ctypes import cdll, byref, create_string_buffer
    libc = cdll.LoadLibrary('libc.so.6')    #Loading a 3rd party library C
    buff = create_string_buffer(len(newname)+1) #Note: One larger than the name (man prctl says that)
    buff.value = newname                 #Null terminated string as it should be
    libc.prctl(15, byref(buff), 0, 0, 0) #Refer to "#define" of "/usr/include/linux/prctl.h" for the misterious value 16 & arg[3..5] are zero as the man page says.

        # from ctypes import cdll, byref, create_string_buffer
        # libc = cdll.LoadLibrary('libc.so.6')
        # buff = create_string_buffer(len(newname)+1)
        # buff.value = newname
        # libc.prctl(15, byref(buff), 0, 0, 0)

def get_proc_name():
    if not is_linux():
        return

    from ctypes import cdll, byref, create_string_buffer
    libc = cdll.LoadLibrary('libc.so.6')
    buff = create_string_buffer(128)
    # 16 == PR_GET_NAME from <linux/prctl.h>
    libc.prctl(16, byref(buff), 0, 0, 0)
    return buff.value

#---------------------------------------#
#       USER NOTIFICATION               #
#---------------------------------------#


def notify(summary, body='', app_name='', app_icon='',
     timeout=5000, actions=[], hints=[], replaces_id=0):
    import dbus
    """
    System notification message:

    Example:
    notify("Touchpad Disabled")
    """
    _bus_name = 'org.freedesktop.Notifications'
    _object_path = '/org/freedesktop/Notifications'
    _interface_name = _bus_name

    session_bus = dbus.SessionBus()
    obj = session_bus.get_object(_bus_name, _object_path)
    interface = dbus.Interface(obj, _interface_name)
    interface.Notify(app_name, replaces_id, app_icon,
            summary, body, actions, hints, timeout)


def msgbox_error(msg, title="gtkBuilder Selector"):
    import gtk

    dlg = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE)
    dlg.set_title(title)
    dlg.set_markup(msg)
    dlg.run()
    dlg.destroy()

def msgbox_ok(msg, title):
    import gtk

    dlg = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
    dlg.set_title(title)
    dlg.set_markup(msg)
    dlg.run()
    dlg.destroy()

def msgbox_info(msg, title="INFO"):
    import gtk

    parent = None
    md = gtk.MessageDialog(parent, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE,
                           "Download completed")
    md.set_title(title)
    md.run()
    md.destroy()

def msgbox_question(question, title="Question"):
    import gtk

    dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL,
                               gtk.MESSAGE_INFO, gtk.BUTTONS_YES_NO,
                               question)
    dialog.set_title(title)
    response = dialog.run()
    dialog.destroy()

    if response == gtk.RESPONSE_YES:
        return True
    else:
        return False



#----------------------------#
#  PATH FUNCTIONS            #
#----------------------------#

def this():
    """
    Returns the absolute path to the script that calls this function
    """
    return os.path.abspath(inspect.stack()[1][1])

def this_dir():
    """
    Returns the absolute path to script directory that calls this function
    """
    return os.path.dirname(os.path.abspath(inspect.stack()[1][1]))

def addrelpath(path="../"):
    thisdir  = os.path.dirname(os.path.abspath(inspect.stack()[1][1]))
    sys.path.append(os.path.join(this_dir(), path))


def resource_path(filename):
    """
    :param filename: (str)  Name of file in same directory of script
    Returns absolute path to file in same directory that this function
    is being called.
    """
    return os.path.join( os.path.dirname(os.path.abspath(inspect.stack()[1][1])), filename)

def get_globals():
    """ Gett global dictionary of __main__ module """

    import inspect
    #x = inspect.stack()[1]
    #print x
    #print dir(x[0])

    _globals = inspect.currentframe().f_back.f_globals
    print(_globals)
    return _globals
    #print "Called from module", caller.f_globals['__name__']
    #print "Called from module", _globals['__name__']


def get_resource_file(filen):
    """
    :param filen: (str) File name of resource file
    :return:

    Return content of file in same directory of the script calling
    this routine or inside the zip file if the script is imported
    from a zip file ( Python egg file).

    """
    import zipfile
    this_directory = os.path.dirname(os.path.abspath(inspect.stack()[1][1]))
    #logger.debug("Getting resource file %s" % filen)

    if zipfile.is_zipfile(this_directory):
       #logger.debug("ZIP FILE")
       zf = zipfile.ZipFile(this_directory)
       data = zf.read(filen)

    else:
       #logger.debug("NOT ZIP FILE")
       data = open(os.path.join(this_directory, filen)).read()

    return data

def get_home():
    return os.path.expanduser('~')

def expandpath(path):
    """
    Expand path variables to absolute path
    """
    plist = []
    
    for p in path.split(os.sep):
        p_ = os.path.expanduser(p)
        p_ = os.path.expandvars(p_)
        plist.append(p_)
      
    return os.path.abspath(os.path.join(*plist))


def is_main():
    fname=  os.path.abspath(inspect.stack()[1][1])
    print(fname)




#-------------------------------#
#  OPERATING SYSTEM DETECTION   #
#-------------------------------#

def is_unix():

    return sys.platform.startswith('linux') or \
           sys.platform.startswith('bsd') or \
           sys.platform.startswith('darwin')

def is_linux():
    """
    :return: Return True if OS is Linux, False otherwise
    :rtype: bool
    """
    return sys.platform.startswith('linux')

def is_windows():
    """
    :return: Return True if OS is Windows, False otherwise
    :rtype: bool
    """
    return sys.platform.startswith('win')

def is_darwin():
    """
    :return: Return True if OS is OSX, False otherwise
    :rtype: bool
    """
    return sys.platform.startswith('darwin')

def is_bsd():
    """
    :return: Return True if OS is BSD, False otherwise
    :rtype: bool
    """
    return sys.platform.startswith('bsd')

def xclip():
    """
    Run clipboard command
    :return:
    """
    if platform.startswith("linux"):
        output = execute("xclip -selection clipboard -o")
    else:
        raise Exception("Not implemented yet to this platform")

    return output

def get_external_ip():
    import urllib.request, urllib.parse, urllib.error
    import re
    site = urllib.request.urlopen("http://checkip.dyndns.org/").read()
    grab = re.findall('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', site)
    address = grab[0]
    return address

def get_tinyurl(url):
    """
    Get Compressed URL
    """
    import urllib.request, urllib.parse, urllib.error
    
    tpl = "http://tinyurl.com/api-create.php?url={url}"
    url_ = tpl.format(url=url)
    tinyurl = urllib.request.urlopen(url_).read()
    return tinyurl

#-----------------------------#
#  COLORED PRINT              #
#-----------------------------#

def printc(*args):
    """
    Print text in colored format

    Color tags:
    {r} - red
    {y} - yellow
    {g} - green
    {0} - black
    {m} - magneta
    {w} - white
    {b} - Blue

    {b0} - background black
    {br} - background white
    {by} - background yello

    {bold} - Bold text
    {line} - Underline

    """
    import re
    txt = "".join(args) + "{w}"

    txt = re.sub(r'{\0}', r"\033[0;30m", txt)  # BLACK
    txt = re.sub(r'{b}', r"\033[0;34m", txt)  # BLUE
    txt = re.sub(r'{w}', r"\033[0;37m", txt)  # WHITE
    txt = re.sub(r'{g}', r"\033[0;32m", txt) # GREEN
    txt = re.sub(r'{c}', r"\033[0;36m", txt)  # CYAN
    txt = re.sub(r'{r}', r"\033[0;31m", txt)  # RED
    txt = re.sub(r'{y}', r"\033[0;33m", txt)  # YELLOW
    txt = re.sub(r'{m}', r"\033[0;35m", txt)  # MAGNETA

    # BACKGROUNDS
    txt = re.sub(r'{b0}', r"\033[0;40m", txt)  # BLACK
    txt = re.sub(r'{bb}', r"\033[0;44m", txt)  # BLUE
    txt = re.sub(r'{bw}', r"\033[0;41m", txt)  # WHITE
    txt = re.sub(r'{bg}', r"\033[0;42m", txt)  # GREEN
    txt = re.sub(r'{bc}', r"\033[0;46m", txt)  # CYAN
    txt = re.sub(r'{br}', r"\033[0;41m", txt)  # RED
    txt = re.sub(r'{by}', r"\033[0;43m", txt)  # YELLOW
    txt = re.sub(r'{bm}', r"\033[0;45m", txt)  # MAGNETA

    txt = re.sub(r'{bold}', r"\033[1m", txt)    # Bold
    txt = re.sub(r'{line}', r"\033[4m", txt)    # Bold

    print(txt)


def exec_output(code, namespace={}):
    """
    Execute code in __main__
    global dictionary (namespace)
    and return output.

    """

    buffer = StringIO()
    sys.stdout = buffer
    exec(code, namespace)
    sys.stdout = sys.__stdout__

    return buffer.getvalue()


def run_example(code):

    import inspect
    _globals = inspect.currentframe().f_back.f_globals

    lines = code.splitlines()
    #_code = joinstr(lines, '\n>>> ')
    #print _code

    for line in lines:
        if line.startswith('#'):
            print('\n' + line[1:])
        else:
            printc("{g}>>> ", line)
            #if EXECUTE_STEP: raw_input(">> Enter to RETURN to continue")

            output = exec_output(line, _globals)
            if output:
                printc("{r}", output)


def run_block(code):

    import inspect
    _globals = inspect.currentframe().f_back.f_globals
    _code = joinstr(code.splitlines(), '\n>>> ')

    printc("{g}", _code)
    output = exec_output(code, _globals)
    printc("{r}", output)


def paste_run():
    #import re
    #from utils import xclip
    txt = xclip()
    txt = txt.strip('\n').strip('\r')



    # Replace bad character
    txt = txt.replace(r'’', "'").replace(r'‘', "'").replace(r'′', "'").replace(r'−', '-')

    # Remove lines non starting with >>>
    lines = [x for x in txt.splitlines() if x.startswith(">>>")]

    # Remove >>> from beginning of lines
    lines = [x.split(">>>")[1].strip() for x in lines]


    #print "\n".join(lines)

    #nextxt = "\n".join(lines)
    #exec(nextxt)

    #print "----------------"

    for line in lines:

        print(">>> ", line)

        if not line:
            continue

        if re.match(".*=.*", line) or re.match("^from.*import", line) or re.match("^import", line):
            exec(line)
        else:
            print(eval(line))


#-----------------------------#
#           MATH              #
#-----------------------------#

def cmpflt(x, y, error=0.01):
    """
    Compare to float numbers
    """
    return abs(x-y) < error

def cmpfltp(x, y, error=0.01):
    """
    Compare the percentual error between two
    float point numbers.
    """
    return abs((x-y)/x) < error


def shape_list(lst, N):
    """
    Transforms a list into a matrix, for instance:

    :param N: Number of elements per row
    :return:  Reshaped list

    [a0, b0, c0, a1, b1, c1, a2, b2, c2] into

    [
    [a0 b0 c0],
    [a1 b1 c1],
    [a2 b2 c2],
    ]

    Examples:
    In [20]: lst = range(9)
    In [22]: lst
    Out[22]: [0, 1, 2, 3, 4, 5, 6, 7, 8]

    In [24]: shape_list(lst, 3)
    Out[24]: [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

    In [25]: shape_list(lst, 4)
    Out[25]: [[0, 1, 2, 3], [4, 5, 6, 7]]

    In [28]: shape_list(lst, 1)
    Out[28]: [[0], [1], [2], [3], [4]]
    """
    ls = lst[:]
    return [[ls.pop(0) for i in range(N)] for r in ls]



#---------------------------------------------#
#       WINDOWS FUNCTIONS                     #
#---------------------------------------------#

import time

try:
    import win32api
    import win32con
    import ctypes

    OpenClipboard = ctypes.windll.user32.OpenClipboard
    EmptyClipboard = ctypes.windll.user32.EmptyClipboard
    GetClipboardData = ctypes.windll.user32.GetClipboardData
    SetClipboardData = ctypes.windll.user32.SetClipboardData
    CloseClipboard = ctypes.windll.user32.CloseClipboard
    GlobalLock = ctypes.windll.kernel32.GlobalLock
    GlobalAlloc = ctypes.windll.kernel32.GlobalAlloc
    GlobalUnlock = ctypes.windll.kernel32.GlobalUnlock
    memcpy = ctypes.cdll.msvcrt.memcpy
except:
    pass

""" Abbreviations for readability """

""" Windows Clipboard utilities """
def GetClipboardText():
    text = ""
    if OpenClipboard(0):
        hClipMem = GetClipboardData(win32con.CF_TEXT)
        GlobalLock.restype = ctypes.c_char_p
        text = GlobalLock(hClipMem)
        GlobalUnlock(hClipMem)
        CloseClipboard()
    return text

def SetClipboardText(text):
    buffer = ctypes.c_buffer(text)
    bufferSize = ctypes.sizeof(buffer)
    hGlobalMem = GlobalAlloc(win32con.GHND, bufferSize)
    GlobalLock.restype = ctypes.c_void_p
    lpGlobalMem = GlobalLock(hGlobalMem)
    memcpy(lpGlobalMem, ctypes.addressof(buffer), bufferSize)
    GlobalUnlock(hGlobalMem)
    if OpenClipboard(0):
        EmptyClipboard()
        SetClipboardData(win32con.CF_TEXT, hGlobalMem)
        CloseClipboard()

""" Windows Registry utilities """
def OpenRegistryKey(hiveKey, key):
    keyHandle = None
    try:
        curKey = ""
        keyItems = key.split('\\')
        for keyItem in keyItems:
            if curKey:
                curKey = curKey + "\\" + keyItem
            else:
                curKey = keyItem
            keyHandle = win32api.RegCreateKey(hiveKey, curKey)
    except Exception as e:
        keyHandle = None
        print("OpenRegistryKey failed:", e)
    return keyHandle

def ReadRegistryValue(hiveKey, key, name):
    """ Simple api to read one value from Windows registry.
    If 'name' is empty string, reads default value."""
    data = typeId = None
    try:
        hKey = win32api.RegOpenKeyEx(hiveKey, key, 0, win32con.KEY_ALL_ACCESS)
        data, typeId = win32api.RegQueryValueEx(hKey, name)
        win32api.RegCloseKey(hKey)
    except Exception as e:
        print("ReadRegistryValue failed:", e)
    return data, typeId

def WriteRegistryValue(hiveKey, key, name, typeId, data):
    """ Simple api to write one value to Windows registry.
    If 'name' is empty string, writes to default value."""
    try:
        keyHandle = OpenRegistryKey(hiveKey, key)
        win32api.RegSetValueEx(keyHandle, name, 0, typeId, data)
        win32api.RegCloseKey(keyHandle)
    except Exception as e:
        print("WriteRegistry failed:", e)

""" misc utilities """
def GetPythonwExePath():
    """ Get path to current version of pythonw.exe """
    pythonExePath = ""
    try:
        pythonwExeName = "pythonw.exe"
        pythonInstallHiveKey = win32con.HKEY_LOCAL_MACHINE
        pythonInstallKey = r"Software\Python\PythonCore\%s\InstallPath" % sys.winver
        pythonInstallDir, typeId = ReadRegistryValue(pythonInstallHiveKey, pythonInstallKey, "")
        pythonwExePath = os.path.join(pythonInstallDir, pythonwExeName)
    except Exception as e:
        print("GetPythonExePath failed:", e)
    return pythonwExePath


def get_desktop_path():
    """
    Returns the desktop directory.

    ------------------
    It could be used the environement variables,
    however it is not compatibel with locales
    differents from English.
    """
    from win32com.shell import shell, shellcon
    return shell.SHGetFolderPath (0, shellcon.CSIDL_DESKTOP, None, 0)

def get_appdata_path():
    from win32com.shell import shell, shellcon
    return shell.SHGetFolderPath (0, shellcon.CSIDL_APPDATA, None, 0)

def get_facvorites_path():
    from win32com.shell import shell, shellcon
    print(shell.SHGetFolderPath (0, shellcon.CSIDL_FAVORITES, None, 0))


def get_drivers():
    """
    Return Windows drivers:

    >>> get_drivers()
    ['C:\\', 'D:\\', 'Z:\\']
    """
    import win32api
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    return drives

def create_link(orig, dest, descripion = ""):
    """
    Create Linking to File:
        orig: Origin File or directory
        dest: Destination directory
    """

    import os, sys
    import pythoncom
    from win32com.shell import shell, shellcon

    fpath, fname = os.path.split(orig)
    linkname = fname.split('.')[0] + ".lnk"

    shortcut = pythoncom.CoCreateInstance (
      shell.CLSID_ShellLink,
      None,
      pythoncom.CLSCTX_INPROC_SERVER,
      shell.IID_IShellLink
    )
    shortcut.SetPath (orig)
    shortcut.SetDescription ( descripion)
    shortcut.SetIconLocation (orig, 0)

    desktop_path = shell.SHGetFolderPath (0, shellcon.CSIDL_DESKTOP, 0, 0)
    persist_file = shortcut.QueryInterface (pythoncom.IID_IPersistFile)
    persist_file.Save (os.path.join (dest, linkname), 0)


def get_shares():
    """ Get Windows Share Directories """

    import win32net
    import win32netcon

    COMPUTER_NAME = "" # look at this machine
    INFO_LEVEL = 2


    shares_ = []

    resume = 0
    while True:
      (shares, total, resume) = \
        win32net.NetShareEnum (
          COMPUTER_NAME,
          INFO_LEVEL,
          resume,
          win32netcon.MAX_PREFERRED_LENGTH
        )
      for share in shares:
        shares_.append(share)
        #print share

      if not resume:
        break

    return shares_


def elevate_privilege(python_script):
    import win32api
    win32api.ShellExecute( 0, # parent window
        "runas", # need this to force UAC to act
        "C:\\python27\\python.exe",
        python_script,
        "C:\\python27", # base dir
        1 ) # window visibility - 1: visible, 0: backgroun


if __name__ == "__main__":

    print("is_windows() ", is_windows())
    print("is_unix() ", is_unix())

    if is_windows():
        print(get_appdata_path())

        print(GetClipboardText())

        print("get_drivers() ", get_drivers())


        #create_link("C:\Python27", get_desktop_path(), "Python directory")
