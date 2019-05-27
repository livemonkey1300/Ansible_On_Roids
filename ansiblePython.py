#!/usr/bin/python3
import sqlite3
from sqlite3 import Error
import os
import socket

class DataB:
 def __init__(self, db_file):
  self.db_file = db_file
  self.conn = ''
  self.c = ''
  self.table = ''
  self.table_structure = ''
  self.sql = ''
  self.table_value = ''
 def connecting(self):
  try:
   self.conn = sqlite3.connect(self.db_file)
   self.c = self.conn.cursor()
  except Error as e:
   print(e)
 def start(self):
     self.connecting()
 def init_table(self , table ):
     self.table = 'CREATE TABLE IF NOT EXISTS %s ' % ( table )
 def init_table_structure(self , structure ):
     charlist = ['[',']','\'']
     table_structure = ' %s ' % ( structure )
     for char in charlist:
         table_structure = table_structure.replace(char,'')
     self.table_structure = '( %s );' % (table_structure)
 def create_in_table(self, table, structure):
     self.init_table(table)
     self.init_table_structure(structure)
     self.proc_table_l2()


 def proc_table_l3(self):
       self.sql = '%s%s%s' % ( self.table , self.table_structure , self.table_value )
       self.c.execute(self.sql)
       self.conn.commit()
 def proc_table_l2(self):
       self.sql = '%s%s' % ( self.table , self.table_structure )
       self.c.execute(self.sql)
       self.conn.commit()

 def UPDATE_table(self, table, structure , map , value , mapvalue ):
       self.table = 'UPDATE %s SET %s = ? WHERE %s = ? ' % ( table , structure , map)
       self.sql = '%s' % ( self.table )
       self.c.execute(self.sql , ( value , mapvalue ))
       self.conn.commit()

 def UPDATE_To_table(self, table):
       self.table = 'SELECT * FROM %s' % ( table )
       self.sql = '%s' % ( self.table )
       options = []
       for row in self.c.execute(self.sql).description:
           options.append(row[0])
       return options

 def SELECT_CHECK_table(self, table, structure , value ):
       conditions = structure
       conditionv = value
       self.table = 'SELECT * FROM %s WHERE %s LIKE ? ' % ( table , conditions )
       self.sql = '%s' % ( self.table )
       self.c.execute(self.sql , [conditionv] )
       data = self.c.fetchall()
       if len(data)==0:
        #print('Creating %s %s' % (conditionv , self.table ))
        return True
       else:
        #print('%s already exists' % conditionv )
        return False

 def SELECT_in_table(self, table, structure , value ):
       conditions = structure
       conditionv = value
       self.table = 'SELECT * FROM %s WHERE %s LIKE ? ' % ( table , conditions )
       self.sql = '%s' % ( self.table )
       self.c.execute(self.sql , [conditionv] )
       data = self.c.fetchall()
       if len(data)==0:
        # print('%s dont exists' % conditionv )
        return []
       else:
        return data

 def SELECT_table(self , table ):
       self.table = 'SELECT * FROM %s' % ( table )
       self.sql = '%s' % ( self.table )
       self.c.execute(self.sql)
       return self.c.fetchall()

 def DELETE_table(self , table , condition ):
       self.table = 'DELETE FROM %s WHERE %s' % ( table , condition )
       self.c.execute(self.table)
       self.conn.commit()


 def INSERT_table(self , table ):
      self.table = 'INSERT INTO %s' % ( table )
 def INSERT_table_structure(self , structure ):
      charlist = ['[',']','\'']
      table_structure = ' %s ' % ( structure )
      for char in charlist:
          table_structure = table_structure.replace(char,'')
      self.table_structure = '(%s)' % (table_structure)
 def INSERT_table_value(self , value ):
       charlist = ['[',']']
       table_value = ' %s ' % ( value )
       for char in charlist:
           table_value = table_value.replace(char,'')
       self.table_value = ' VALUES(%s)' % (table_value)
 def INSERT_in_table(self, table, structure , value ):
      if self.SELECT_CHECK_table(table, structure[0] , value[0] ):
       self.INSERT_table(table)
       self.INSERT_table_structure(structure)
       self.INSERT_table_value(value)
       self.proc_table_l3()

class PrettyPrint:
    def __init__(self):
        self.head = ''
        self.spacing = 0
    def set_head(self, head):
        self.head = head
    def strip_header(self , head):
        space = ( (len(head) * 5) + 2 )
        self.options_head( head , space )
    def header(self , head):
        space = ( (len(head) * 5) + 2 )
        print (space * '-')
        print (" " + " ".join(head) + "")
        print (space * '-')
        self.options_head( head , space )
    def options_head(self,  option , space ):
        nhead = '-[ ' + option + ' ]'
        spacing = '%s%s' % ( nhead , ( space - len(nhead)) * '-')
        self.spacing = len(spacing)
        print(spacing)
    def print_options( self , arg1 , arg2):
        args = '| %s : %s' % ( arg1 , arg2 )
        largs = len(args)
        lspace = (self.spacing - largs) - 2
        print ( '%s%s |' % ( args , lspace * ' ' ))
    def print_lineBreak( self ):
        print (self.spacing * '-')

     # def set_optionshead(self , op):
     #  self.ophead = '-[ ' + op + ' ]'
     #  self.spacing = len(op)
     #
     # def optionshead(self):
     #  toprint = '%s%s' % ( self.ophead , ( self.spacing  * '-'))
     #  self.spacingtotal = len(toprint)
     #  print ( toprint )
     #
     # def optionsfoot(self):
     #  print ( self.spacingtotal * '-' )
     #
     # def printop( self , arg1 , arg2):
     #  print ( '| %s : %s%s  |' % ( arg1 , arg2 , ( (self.spacingtotal - (9 + len(arg2))) * ' ') ))




class MenuB:
    def __init__(self ):
        self.db = DataB('an.db')
        self.menusitem = { "New host" : self.new_host , "Check Host" : self.check_host , "Check Group" : self.check_group , "Check Groupvar" : self.check_groupvar , "Print Host" : self.print_hostfiles , "Run Ansible" : self.run_hostfiles  , "Edit Host" : self.edit_in_host , "Delete Host" : self.delete_host  , "Exit" : exit }
        self.submenusitem = {}
        self.option = []
        self.query = []
        self.pretty = PrettyPrint()
        self.init_DB()
        self.gid = 0
    def init_DB(self):
        self.db.start()
        self.db.create_in_table( 'Hosts' , ['Id INTEGER PRIMARY KEY AUTOINCREMENT' , 'Name Varchar' , 'Ip Varchar', 'GroupId INTEGER'] )
        self.db.create_in_table( 'Groups' , ['Id INTEGER PRIMARY KEY AUTOINCREMENT' , 'Name Varchar'] )
        self.db.create_in_table( 'GroupVars' , ['Id INTEGER PRIMARY KEY AUTOINCREMENT' , 'Name Varchar' , 'Var Varchar' , 'GroupId INTEGER'] )
        self.db.INSERT_in_table( 'Groups' , ['Name'] , [ 'windows' ] )
        self.db.INSERT_in_table( 'GroupVars' , ['Name' , 'Var' , 'GroupId'] , [ 'ansible_ssh_user' , 'Administrator' , 1 ])
        self.db.INSERT_in_table( 'GroupVars' , ['Name' , 'Var' , 'GroupId'] , [ 'ansible_ssh_pass' , 'Supp0rtt34m' , 1 ])
        self.db.INSERT_in_table( 'GroupVars' , ['Name' , 'Var' , 'GroupId'] , [ 'ansible_ssh_port' , '5986' , 1 ])
        self.db.INSERT_in_table( 'GroupVars' , ['Name' , 'Var' , 'GroupId'] , [ 'ansible_connection' , 'winrm' , 1 ])
        self.db.INSERT_in_table( 'GroupVars' , ['Name' , 'Var' , 'GroupId'] , [ 'ansible_winrm_server_cert_validation' , 'ignore' , 1 ])

    def print_hostfiles(self , pause=0):
        options = []
        f= open("./hosts","w+")
        for Id , Name in self.db.SELECT_table('Groups'):
            print('[%s]' % (Name))
            f.write('[%s]\n' % (Name))
            n = self.db.SELECT_in_table( 'Hosts' , 'GroupId' , Id)
            for Idh , Nameh , Iph , GroupIdh  in n:
             print('%s hname="%s"' % (Iph , Nameh ))
             f.write('%s hname="%s"\n' % (Iph , Nameh ))
            f.write('\n\n')
            print('\n')
            f.write('[%s:vars]\n' % (Name))
            print('[%s:vars]' % (Name))
            n = self.db.SELECT_in_table( 'GroupVars' , 'GroupId' , Id)
            for Idv , Namev , Varv , GroupIdv  in n:
             print('%s=%s' % (Namev,Varv))
             f.write('%s=%s\n' % (Namev,Varv))
        if pause == 0:
         input('[Press Enter To Continue]')
        f.close()
        return options

    def run_hostfiles(self):
        os.system('./run.sh')
        input('[Press Enter To Continue]')

    def check_groupvar(self , pause=0):
        options = []
        for Id , Name , Var , GroupId  in self.db.SELECT_table('GroupVars'):
            self.pretty.print_options(Id , '%s %s %s' % ( Name , Var , GroupId ) )
            options.append(Id)
        self.pretty.print_lineBreak()
        if pause == 0:
         input('[Press Enter To Continue]')
        return options

    def check_group(self , pause=0):
        options = []
        self.pretty.print_lineBreak()
        for Id , Name in self.db.SELECT_table('Groups'):
            self.pretty.print_options(Id , Name)
            options.append(Id)
        self.pretty.print_lineBreak()
        if pause == 0:
         input('[Press Enter To Continue]')
        return options

    def select_host(self , pause=0 , enter='get_check_host'):
        options = self.check_host( pause )
        while True:
         my_input = input('| Enter  %s : ' % (enter) )
         try:
          if int(my_input) in options:
             return my_input
          else:
             print('Wrong %s ' % (enter))
         except (ValueError, IndexError):
          print('Wrong %s ' % (enter))
          pass

    def check_is_IP(self , enter):
        while True:
            my_input = input('| Enter %s : ' % (enter) )
            try:
             socket.inet_pton(socket.AF_INET, my_input)
             return my_input
            except AttributeError:  # no inet_pton here, sorry
              try:
               socket.inet_aton(my_input)
               return my_input
              except socket.error:
               print('Wrong %s ' % (enter))
               pass
            except socket.error:
                print('Wrong %s ' % (enter))
                pass


    def select_group(self , enter):
        options = self.check_group( 1 )
        while True:
         my_input = input('| Enter  %s : ' % (enter) )
         try:
          if int(my_input) in options:
             return my_input
          else:
             print('Wrong %s ' % (enter))
         except (ValueError, IndexError):
          print('Wrong %s ' % (enter))
          pass

    def edit_host(self):
        self.pretty.print_lineBreak()
        self.query = []
        for i in self.db.UPDATE_To_table('Hosts'):
            self.query.append(i)
            if 'Id' not in i:
             self.submenusitem[i] = self.update_in_host
            if 'GroupId' in i:
             self.submenusitem[i] = self.update_in_host
        self.submenusitem['Return'] = self.printMenu
        self.printMenu( 'submenusitem' , 'Updating host %s  ' % ( self.gid ) , 1 )
        self.check_host()

    def update_in_host(self , up):
        n = self.db.SELECT_in_table( 'Hosts' , 'Id' , self.gid)
        print(n[0][self.query.index(up)])
        if 'Ip' in up:
         value = self.check_is_IP( 'IP >' )
        elif 'GroupId' in up:
         value = self.select_group( 'GroupID >')
        else:
         value = input('| Enter an new %s >> ' % (up) )
        self.db.UPDATE_table( 'Hosts' , up , 'Id' , value , self.gid )
        input('[Press Enter To Continue]')

    def edit_in_host(self ):
        self.gid = self.select_host( 1 , 'Select Host')
        self.edit_host()
        input('[Press Enter To Continue]')

    def new_host(self):
        self.pretty.print_lineBreak()
        IP_host_input = self.check_is_IP( 'IP >' )
        Name_host_input = input('| Enter an new Name >> ')
        GroupId_host_input = self.select_group( 'GroupID >' )
        self.db.INSERT_in_table( 'Hosts' , ['Name' , 'Ip' , 'GroupId' ] , [ Name_host_input  , IP_host_input , int(GroupId_host_input) ] )
        self.check_host()

    def check_host(self , pause=0 ):
        options = []
        for i in self.db.SELECT_table('Hosts'):
            options.append(i[0])
            tmp = ''
            for i2 in range( 1 , len(i) - 1):
                tmp = '%s %s' % ( tmp , i[i2])
            n = self.db.SELECT_in_table( 'Groups' , 'Id' , i[len(i) - 1])
            tmp = '%s %s' % ( tmp , n[0][1])
            self.pretty.print_options( i[0] , tmp )
        self.pretty.print_lineBreak()
        if pause == 0:
         input('[Press Enter To Continue]')
        return options
        # os.system('clear')

    def delete_host(self):
        self.gid = self.select_host( 1 , 'Host To DELETE')
        self.db.DELETE_table( 'Hosts' , '%s%s' % ('Id=', self.gid ))

    def printMenu(self , menu='menusitem' , menuprint='Main Menu' , menucall=0):
        menu = self.__dict__[ menu ]
        while True:
         os.system('clear')
         lines = []
         self.pretty.strip_header(menuprint)
         for item in menu:
          lines.append( item )
         for item , key in enumerate(lines):
          self.pretty.print_options( item , key )
         self.pretty.print_lineBreak()
         choice = input('| Enter an option >> ')
         try:
          if int(choice) >= 0 :
           self.pretty.strip_header(lines[int(choice)])
           functionToCall = menu[lines[int(choice)]]
           if menucall == 0:
            functionToCall()
           if menucall != 0 and 'Return' not in lines[int(choice)] :
            functionToCall( lines[int(choice)] )
           if 'Return' in lines[int(choice)] :
            functionToCall()

         except (ValueError, IndexError):
          pass


m = MenuB()
m.printMenu()

# connection = ''
#
#
# def create_connection(db_file):
#     try:
#         conn = sqlite3.connect(db_file)
#         return conn
#     except Error as e:
#         print(e)
#     return None
#
# def create_table(conn, create_table_sql):
#     try:
#         c = conn.cursor()
#         c.execute(create_table_sql)
#     except Error as e:
#         print(e)
#
#
# def create_allTable(conn):
#     tables = ''
#     for i in range(1,3):
#      tables = "%s%s%s" % ( "CREATE TABLE IF NOT EXISTS projects_" , i , " ( id integer PRIMARY KEY, name text NOT NULL); " )
#      create_table (conn , tables )
#
# def main():
#     database = "ansible.db"
#     conn = create_connection(database)
#     if conn is not None:
#         print("To create")
#         with conn:
#          create_allTable(conn)
#          new_host(conn)
#          select_all_host(conn)
#          delete_host(conn)
#     else:
#         print("Error! cannot create the database connection.")
#
#
# def menu(conn):
#
#
#
# def select_all_host(conn):
#     cur = conn.cursor()
#     for id , name in cur.execute("SELECT id , name FROM projects_1"):
#         print( '[%s] %s' % ( id , name))
#
#
# def new_host(conn):
#      New_Host = input('| Enter an New Host  >> ')
#      sql = ''' INSERT INTO projects_1(name)
#                VALUES(?) '''
#      cur = conn.cursor()
#      cur.execute(sql, [New_Host] )
#      return cur.lastrowid
#
# def delete_host(conn):
#      New_Host = input('| Delete Host  >> ')
#      sql = '''  DELETE FROM projects_1 WHERE id=?; '''
#      cur = conn.cursor()
#      cur.execute(sql, New_Host )
#      return cur.lastrowid
#
#
#
#
# if __name__ == '__main__':
#     main()
