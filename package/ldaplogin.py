#coding: utf-8
from ldap3 import Server, Connection, ALL
'''
实现LDAP用户登录验证，首先获取用户的dn，然后再验证用户名和密码
'''
class ldap_auth:

    ldapserver = "" #ldap服务器地址
    domain = ""#根目录
    #ldapuser = "";#ldap服务器用户名
    #domainUserName = domain + '\\'+ ldapuser
    #ldappass = "";#ldap服务器密码

    def ldap_login(self, ldapuser, ldappass,):
        domainUserName = self.domain + '\\' + ldapuser
        s = Server(self.ldapserver, get_info=ALL)  # define an unsecure LDAP server, requesting info on DSE and schema
        # define the connection
        c = Connection(s, user=domainUserName, password=ldappass)
        # perform the Bind operation
        r = c.bind()
        if r:
            return "True"
        else:
            return "False"


