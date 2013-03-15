# -*- coding: utf-8 -*-

'''
Created on 25/05/2010

@author: thiagop
'''

import MySQLdb as driver
from ConfigParser import RawConfigParser
from traceback import format_exc
import MySQLdb

class DBCursor(object):
    '''
    classdocs
    '''
    __instance = None
    __log = None
    __terminal = None
 
    
    def __init__(self, cfg=''):
        '''
        Constructor
        '''
        
        if cfg <> '':
            
            host = cfg.get('DBCreds', 'DBHost')
            user = cfg.get('DBCreds', 'DBUser')
            pwd = cfg.get('DBCreds', 'DBPass')
            base = cfg.get('DBCreds', 'DBName')
                
            if DBCursor.__instance == None:
                connection = driver.connect(host, user, pwd, base)
                
                # None = Autocommit
                connection.isolation_level = None
                
                DBCursor.__instance = connection.cursor()
            
    def execute(self, sql):         
        self.__instance.execute(sql)
    
    def __getattr__(self, name):
        if name == "execute":
            return self.__class__.execute
        else:
            return getattr(self.__instance, name)
        

        
        