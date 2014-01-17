#!/bin/python

class MenuItem(object):
    
    """
    constructor
    @param {string} label
    @param {function} callback
    """
    def __init__(self, label, cbk):
        self.label = label #label
        self.cbk = cbk #callback
        self.value = None #state that can be set for prompt or toggle options

class Menu(object):
    
    """
    constructor
    @param {string} title
    """
    def __init__(self, title):
        
        """
        List that stores labels with callbacks as MenuItem(label, cbk)
        """
        self.items = list()
        
        """
        Menu navigation items
        """
        self.navItems = list()

        """
        menu title
        """
        self.title = title

        """
        tells whether someone has requested the closing of the menu
        """
        self._closeRequested = False
        
        """
        close value to be returned
        """
        self.returnValue = None

    """
    add an item to the menu
    @param {string} label
    @param {function} cbk
    """
    def addItem(self, label, cbk):
        self.items.append(MenuItem(label, cbk))
    
    """
    run the menu body, note that menu navigation options must retrun True or False,
    if False is returned the menu is closed
    @return value returned from the close event callback
    """
    def run(self):
        if self.title:
            print("#################### {0} ####################".format(self.title))
        self._closeRequested = False
        while not self._closeRequested:
            #print choices
            for i in range(0, len(self.items)):
                print("{0}) {1}".format(i, self.items[i].label))
            #print navigation choices
            for i in range(len(self.items), len(self.items) + len(self.navItems)):
                print("{0}) {1}".format(i, self.navItems[i - len(self.items)].label))
            try:
                idx = int(input(">"))
            except ValueError as ex:
                print("[-] Invalid value")
                continue
            
            #invoke callback passing the menu object and the selected menu item for 
            #state modifications
            if idx < len(self.items) and idx >= 0:
                #invoke item callback
                self.items[idx].cbk(self, self.items[idx])
            elif idx >= len(self.items) and idx < len(self.items) + len(self.navItems):
                #invoke navigation callback
                self.navItems[idx - len(self.items)].cbk(self, self.navItems[idx - len(self.items)])
            else:
                print("[-] Invalid selection")
        #return this value that can be set by item callbacks
        return self.returnValue
    
    def close(self):
        self._closeRequested = True

class ActionMenu(Menu):
    
    def __init__(self, title):
        super(ActionMenu, self).__init__(title)
        self.navItems.append(MenuItem('back', lambda menu,item: menu.close()))

class PromptMenu(Menu):

    def __init__(self, title, successCbk=None, failureCbk=None):
        super(PromptMenu, self).__init__(title)
        
        self.navItems.append(MenuItem('Ok', self.success))
        self.navItems.append(MenuItem('Cancel', self.cancel))

        #success or failure of selection callbacks, fired with menu instance as arg
        self.onSuccess = successCbk
        self.onFailure = failureCbk

    #callback
    def success(self, menu, item):
        self.returnValue = {}
        for item in self.items:
            self.returnValue[item.label] = item.value
        self.close()
        if self.onSuccess:
            self.onSuccess(self)

    #callback
    def cancel(self, menu, item):
        self.returnValue = {}
        self.close()
        if self.onFailure:
            self.onFailure(self)
    

## generic callbacks

def arrayParserCallback(menu, item):
    try:
        value = eval(input("{0}>".format(item.label)))
        if isinstance(value, list):
            item.value = value
        else:
            print("[-] invalid value")
    except ValueError:
        item.value = None
        print("[-] invalid value")
