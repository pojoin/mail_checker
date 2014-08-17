#!/usr/bin/python
#coding=UTF-8
# Filename : check_mail.py
'''
Created on Apr 5, 2013

@author: pojoin
'''
import sys
import gtk
import appindicator
import os
import imaplib
import re
import pynotify

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
PING_FREQUENCY = 30 # seconds

class CheckGMail:
    def __init__(self):
        self.red_icon_path = self.icon_directory() + '02.png'
        self.green_icon_path = self.icon_directory() + '01.png'
        self.ind = appindicator.Indicator("new-gmail-indicator",
                                           self.green_icon_path,
                                           appindicator.CATEGORY_COMMUNICATIONS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.ind.set_attention_icon(self.red_icon_path)
        
        #self.ind.set_icon(icon_path + '01.png')
                                             
        #print icon_path
        self.menu_setup()
        self.ind.set_menu(self.menu)
        
    def icon_directory(self):
        return os.path.dirname(os.path.realpath(__file__)) + os.path.sep
     
    def menu_setup(self):
        self.menu = gtk.Menu()
        
        self.quit_item = gtk.MenuItem("Quit")
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()
        self.menu.append(self.quit_item)
        

    def main(self):
        #self.check_mail()
        gtk.timeout_add(PING_FREQUENCY * 1000, self.check_mail)
        gtk.main()
    
    def openThunderbird(self,widget):
    	subprocess.Popen('thunderbird', shell=True, stdin=subprocess.PIPE)

    def quit(self, widget):
        sys.exit(0)
    
    #利用系统的通知
    def notify(self,title='Test',content='test'):
    	pynotify.init("DCY-Title")
    	n = pynotify.Notification(title, content,self.green_icon_path)
    	n.show()

    def check_mail(self):
        print 'check'
        try:
            m139_unread = self.m139_checker('mobilePhoneNumber@139.com','mypasswd')
            
            if m139_unread > 0 :
                self.ind.set_status(appindicator.STATUS_ATTENTION)
                self.ind.set_label(str(m139_unread))
                self.notify('提示','您有新邮件，请注意查收！')
            else:
                self.ind.set_status(appindicator.STATUS_ACTIVE)
                self.ind.set_label(None)
			                
        except Exception,e:
            print e.message
            self.notify('erro',e)
            fileHandle = open(self.icon_directory()+'err.log','w+')
            fileHandle.write(e +'\n')
            fileHandle.close()
        return True
    
    def m139_checker(self,username,password):
        i = imaplib.IMAP4('imap.10086.cn')
        try:
            i.login(username, password)
            x, y = i.status('INBOX', '(MESSAGES UNSEEN)')
            #messages = int(re.search('MESSAGES\s+(\d+)', y[0]).group(1))
            unseen = int(re.search('UNSEEN\s+(\d+)', y[0]).group(1))
            return unseen
        except Exception,e:
            print e.message
            return False, 0

if __name__ == "__main__":
    indicator = CheckGMail()
    indicator.main()
