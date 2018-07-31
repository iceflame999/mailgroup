#!/usr/bin/env python
# coding=utf-8
import requests
import json

'''
调用腾讯API
'''

class mailapi:

    corpid = ""
    corpsecret = ""
    url = "https://api.exmail.qq.com/cgi-bin/gettoken"
    url = url + "?corpid=" + corpid + "&corpsecret=" + corpsecret


    def gettoken(self):
        html = requests.get(self.url)
        list = html.json()
        token = list["access_token"]
        return token

    def increase_group(self, groupid, groupname, username, token):
        userlist = []
        username = username + "这里加邮箱域名"
        userlist.append(username)
        val = {
            "groupid": "",
            "groupname": "",
            "userlist": [],
            "grouplist": [],
            "department": [],
            "allow_type": 0,
            "allow_userlist": []
        }
        url = "https://api.exmail.qq.com/cgi-bin/group/create?access_token=" + token
        val["groupid"] = groupid
        val["groupname"] = groupname
        val["userlist"] = userlist
        result = requests.post(url, data=json.dumps(val))
        return result.text

    def del_group(self, groupid, token):
        url = "https://api.exmail.qq.com/cgi-bin/group/delete?access_token=" + token + "&groupid=" + groupid
        result = requests.get(url)
        return result.text

    def get_group(self, groupid, token):
        url = "https://api.exmail.qq.com/cgi-bin/group/get?access_token=" + token + "&groupid=" + groupid
        html = requests.get(url)
        list = html.json()
        userlist = list["userlist"]
        groupname = list["groupname"]
        return userlist, groupname

    def add_group(self, groupid, username, token):
        userlist, groupname = self.get_group(groupid, token)
        url = "https://api.exmail.qq.com/cgi-bin/group/update?access_token=" + token
        userlist.append(username)
        val = {
            "groupid": "",
            "groupname": "",
            "userlist": [],
            "grouplist": [],
            "department": [],
            "allow_type": 0,
            "allow_userlist": []
        }
        val["groupid"] = groupid
        val["groupname"] = groupname
        val["userlist"] = userlist
        result = requests.post(url, data=json.dumps(val))
        return result.text

    def remove_group(self, groupid, username, token):
        userlist, groupname = self.get_group(groupid, token)
        url = "https://api.exmail.qq.com/cgi-bin/group/update?access_token=" + token
        try:
            userlist.remove(username)
        except:
            return '''{"errmsg":"无法移除，请确认移除邮箱。"}'''
        val = {
            "groupid": "",
            "groupname": "",
            "userlist": [],
            "grouplist": [],
            "department": [],
            "allow_type": 0,
            "allow_userlist": []
        }
        val["groupid"] = groupid
        val["groupname"] = groupname
        val["userlist"] = userlist
        result = requests.post(url, data=json.dumps(val))
        return result.text
