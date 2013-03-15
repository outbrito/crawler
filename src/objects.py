# -*- coding: UTF-8 -*-

'''
Created on 21/05/2011

@author: thiagop
'''
# Project imports
from DBManager import DBCursor
from ConfigParser import RawConfigParser
from traceback import format_exc
from MySQLdb import IntegrityError

    
#Função para mapear os campos da tabela em propriedades do objeto
def fieldMapper(cls, fields, values):
    result = []
    if values <> None:
        for row in values:
            
            obj = cls()
            
            for i in range(len(fields)):
                
                if row[i] == None:
                    continue
                elif row[i] == 'True':
                    v = True
                elif row[i] == 'False':
                    v = False
                elif type(obj.__getattribute__(fields[i][0])) == str:
                    v = str(row[i])
                    v = unicode(v, 'iso-8859-1')
                else:
                    v = row[i] 
                
                
                obj.__setattr__(fields[i][0], v)
            
            result.append(obj)
    
    return result


def getClassForTable(tableName): 
    lst = type.__subclasses__(Table)
    
    for cls in lst :
        if cls._Table__table == tableName :
            return cls
        
    return None

# Masterclass  
class Table(object):

    @classmethod
    def all(cls):
        query = "SELECT * FROM %s" %cls.__table
        cursor = DBCursor()
        cursor.execute(query)
        
        rs = cursor.fetchall()
        cols = cursor.description
        
        if rs <> None:
            objects = fieldMapper(cls, cols, rs)
            
        return objects
    
    @classmethod
    def get(cls, **kwargs):
        query = "SELECT * FROM %s" %cls.__table
        
        if kwargs <> {}:
            query += " WHERE "
        
        where = []
        for k,v in kwargs.items():
            where.append("%s = '%s'" %(k, v))
            
        query +=" " + " AND ".join(where)
        
        query = query.encode('iso-8859-1', 'xmlcharrefreplace')
        query = query.decode('iso-8859-1')
            
        cursor = DBCursor()
        cursor.execute(query)
        
        rs = cursor.fetchall()
        cols = cursor.description
        
        objects = fieldMapper(cls, cols, rs)
        
        return objects
    
    @classmethod
    def distinct(cls,*args, **kwargs):
        query = "SELECT DISTINCT" 
        
        query +=" " + ", ".join(args)
            
        query += " FROM %s" %cls.__table
        
        if kwargs <> {}:
            query += " WHERE"
        
        where = []
        for k,v in kwargs.items():
            where.append("%s = '%s'" %(k, v))
            
        query +=" " + " AND ".join(where)
        
        query = query.encode('iso-8859-1', 'xmlcharrefreplace')
        query = query.decode('iso-8859-1')
            
        cursor = DBCursor()
        cursor.execute(query)
        
        rs = cursor.fetchall()
        cols = cursor.description
        
        objects = fieldMapper(cls, cols, rs)
        
        return objects
    
    @classmethod
    def delete(cls, **kwargs):
        
        query = "DELETE FROM %s" %cls.__table
        
        if kwargs <> {}:
            query += " WHERE "
        
        param = ["%s = %s" %(k, v) for k,v in kwargs.items()]
        
        query += " AND ".join(param)
        
#        query = query.encode('iso-8859-1', 'xmlcharrefreplace')
#        query = query.decode('iso-8859-1')
        
        cursor = DBCursor()
        cursor.execute(query)
        
    
    def save(self, **kwargs):        
        if hasattr(self, "vac_ref") and self.vac_ref == 0:
            sql = "SELECT MAX(vac_ref) FROM " + self._Table__table
            
            cursor = DBCursor()
            cursor.execute(sql)
            res = cursor.fetchone()
            max_tab = res[0]
            
            if max_tab == None:
                max_tab = 0
                
            self.vac_ref = max_tab + 1
                
        table = self.__class__.__table
        dic = self.getVars()
        
        for k,v in dic.items():
            if v == None:
                dic.pop(k)
        
        if kwargs <> {}:
            fields = ", ".join(["%s='%s'" %(k,v) for k,v in dic.items()])
            
            params = " AND ".join(["%s='%s'" %(k,v) for k,v in kwargs.items()])
        
            query = "UPDATE %s SET %s WHERE %s" %(self._Table__table, fields, params)
               
        else:
            fields = "(" + ", ".join(["%s" %i for i in dic.keys()]) + ")"
            values = "(" + ", ".join(["'%s'" %i for i in dic.values()]) + ")"    
            
            query = """INSERT INTO %s %s VALUES %s""" %(table, fields, values)
            
            query = query.encode('iso-8859-1', 'xmlcharrefreplace')
            query = query.decode('iso-8859-1')
            
            tryies = 0
            while tryies < 5:
                try:
                    cursor = DBCursor()
                    cursor.execute(query)
                    break
                
                except IntegrityError:
                    # if it has some error, print the exception and try to save again
#                    log = open('sql.log', 'a')
#                    log.write(format_exc() + '\n\n')
#                    log.close()
                    
                    tryies += 1 
    
    
    def getVars(self):
        vars = self.__dict__.copy()
#        vars = self.__dict__
        
        for k,v in vars.items():
            if "__" in k:
                v = vars.pop(k)
                
                k = k[k.index("__"):]
                vars[k] = v
                
        return vars
            
    
class Advertiser(Table):
    '''
    advertiser
    '''
    
    _Table__table = "advertiser"


    def __init__(self):
        '''
        Constructor
        '''
        self.adv_ref = ''
        self.adv_code = 0
        self.adv_name = ""
        self.adv_add1 = ""
        self.adv_add2 = ""
        self.adv_add3 = ""
        self.adv_add4 = ""
        self.adv_pcode = ""
        self.adv_sman = ''
        self.adv_cont_1 = ""
        self.adv_cont_2 = ""
        self.adv_cont_3 = ""
        self.adv_cont_4 = ""
        self.adv_cont_5 = ""
        self.adv_cont_6 = ""
        self.adv_cont_7 = ""
        self.adv_cont_8 = ""
        self.adv_tel = ""
        self.adv_ddial = ""
        self.adv_fax_1 = ""
        self.adv_fax_2 = ""
        self.adv_rem = ""
        self.adv_letter_sent = ''
        self.adv_letter_date = "" #DATETIME
        self.adv_terr = 0
        self.adv_email = ""
        self.adv_type = ""
        self.adv_alt_name = ""
        self.adv_cont_type_1 = ""
        self.adv_cont_type_2 = ""
        self.adv_cont_type_3 = ""
        self.adv_cont_type_4 = ""
        self.adv_cont_type_5 = ""
        self.adv_cont_type_6 = ""
        self.adv_cont_type_7 = ""
        self.adv_cont_type_8 = ""
        self.adv_cont_ddial_1 = ""
        self.adv_cont_ddial_2 = ""
        self.adv_cont_ddial_3 = ""
        self.adv_cont_ddial_4 = ""
        self.adv_cont_ddial_5 = ""
        self.adv_cont_ddial_6 = ""
        self.adv_cont_ddial_7 = ""
        self.adv_cont_ddial_8 = ""
        self.adv_title = ""
        self.adv_added = "" #DATETIME
        self.adv_website = ""
        self.adv_check_url = "Y"
        self.adv_tot_vacancy = 0
        self.adv_tot_asn = 0
        self.adv_machine = ""
        self.adv_modified = "" #DATETIME
        self.adv_user = ""
        self.adv_reg_ip = ""
        self.adv_review_date = "" #DATE
        self.adv_bus_cat = 0
        self.adv_co_size = ""
        
        
    @classmethod
    def getFromConfig(cls, configFile):

        adref = configFile.get('Advertiser', 'ADREF')
        
        return cls.get(adv_ref=adref)
        
        
class Country(Table):
    '''
    Coutry
    '''
    
    _Table__table = "country"


    def __init__(self):
        '''
        Constructor
        '''
        self.cou_code = ''
        self.cou_desc = ""
        
        
class ScrapeVacancy(Table):
    '''
    Scrape_vacancies
    '''
    
    _Table__table = "scrape_vacancies"


    def __init__(self):
        '''
        Constructor
        '''        
        self.sv_script = ""
        self.sv_ref = ""
        self.sv_date = "" #DATE
        self.sv_our_ref = 0
        
        
class Vacancy(Table):
    '''
    Vacancies
    '''
    
    _Table__table = "vacancy"


    def __init__(self):
        '''
        Constructor
        '''        
        self.vac_ref = 0
        self.vac_cre_dte = "" #DATETIME
        self.vac_status = ''
        self.vac_job_title = ""
        self.vac_advertiser = ''
        self.vac_phone = ""
        self.vac_contact = ""
        self.vac_title = ""
        self.vac_needed = 0
        self.vac_date = "" #DATETIME
        self.vac_duration = 0
        self.vac_dur_type = ''
        self.vac_wk_hours = 0.0
        self.vac_sta_time = 0.0
        self.vac_end_time = 0.0
        self.vac_ot_wk = 0.0
        self.vac_ot_sat = 0.0
        self.vac_ot_sun = 0.0
        self.vac_pay_rate = 0.0
        self.vac_contract = 0
        self.vac_flex = ''
        self.vac_fax = ""
        self.vac_add1 = ""
        self.vac_add2 = ""
        self.vac_add3 = ""
        self.vac_add4 = ""
        self.vac_pcode = ""
        self.vac_machine = ""
        self.vac_modified = ""
        self.vac_user = ""
        self.vac_text = ""
        self.vac_locn = ""
        self.vac_type = ""
        self.vac_email_sent = ''
        self.vac_board = ""
        self.vac_salary = ""
        self.vac_advjob = ""
        self.vac_effective = "" #DATETIME
        self.vac_email = ""
        self.vac_url = ""
        self.vac_jd = ""
        self.vac_object = ""
        self.vac_lsource = ""
        self.vac_f_source = 0
        self.vac_f_sector = 0
        self.vac_f_sector2 = 0
        self.vac_f_sector3 = 0
        self.vac_f_region = 0
        self.vac_agencies = 0
        self.vac_job_category = 0
        self.vac_country = ""
        self.vac_county = 0
        
        
        
#        
#if __name__ == "__main__":
#    from DBManager import DBCursor
#    CONFIG_FILE = RawConfigParser()
#    CONFIG_FILE.read("./rulefinancial/Config.ini")
#    db = DBCursor(CONFIG_FILE)
#    print Advertiser.get()