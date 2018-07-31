from django.shortcuts import render,redirect
from package import ldaplogin
from package import gettoken
from package import getdata
import requests

# Create your views here.

def index(request):
    user_status = []
    if request.method == "POST":

        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        if username=="" or password=="":
            temp = {"user": username, "pwd": password, "statu": "False", "label": "用户名或密码错误，请重新输入！"}
            #user_status.append(temp)
            return render(request, "index.html", temp)
        ld = ldaplogin.ldap_auth()
        login = ld.ldap_login(username, password)
        if login=="True":
            #temp = {"user": username, "pwd": password, "statu": login, "label": ""}
            #user_status.append(temp)

            resp = redirect('/group/')# 设置登录成功后跳转页面
            resp.set_cookie('user', username,expires=3600)# 添加cookies，设置生存时间
            return resp
            #return render(request, "group.html", {"data":user_status})
            #return redirect("/group/", {"data":user_status})
        else:
            temp = {"user": username, "pwd": password, "statu": login, "label": "用户名或密码错误，请重新输入！"}
            user_status.append(temp)
            return render(request, "index.html", temp)
    if request.method == "GET":
        temp = {"user":"", "pwd":"", "statu":"","label":""}
        return render(request, "index.html", temp)
    #return HttpResponse("Hello World!")


def group(request):
    temp = {}
    if request.method == "GET":# 处理登录后跳转
        try:#cookies失效后返回登录页面
            username = request.COOKIES['user']
            # 连接数据库，获取群组列表
            group_list = getdata.getgroup()
            temp["user"] = username
            temp["group_list"] = group_list
            # 显示可管理权限
            admin_list = getdata.getadmin(username)
            temp["adminlist"] = admin_list
            return render(request, "group.html", temp)
        except:
            return redirect("/index/")
    if request.method == "POST":
        group_list = getdata.getgroup()
        temp["group_list"] = group_list
        username = request.COOKIES['user']
        temp["user"] = username
        #print(request.POST["id"])
        groupid = request.POST.get("id",None)
        if not groupid:
            try:
                groupid = request.COOKIES['groupid']
            except:
                groupid = ""
        #实例化gettoken类,获取腾讯邮箱连接信息
        api = gettoken.mailapi()
        token = api.gettoken()
        #连接数据库，获取权限列表
        #admin_list = getdata.getadmin(username)

        #response.set_cookie('userlist', userlist, expires=3600)
        if request.POST.get("increase",None):#创建邮件组
            act_groupid = request.POST.get("groupid","")#文本框里填写的groupid
            act_groupname = request.POST.get("groupname", "")
            result = eval(api.increase_group(act_groupid, act_groupname, username, token))
            if result["errmsg"]=="ok":
                temp["increase_label"]="创建成功！"
                try:
                    getdata.addgroup(act_groupname, act_groupid)
                except:
                    temp["increase_label"]="创建成功，本地数据库更新异常！请立即通知管理员！"
                group_list = getdata.getgroup()
                act_username = username + "@roobo.com"
                getdata.addadmin(act_groupid,act_username)
                temp["group_list"] = group_list
                groupid = ""
            else:
                temp["increase_label"]="创建失败：" + result["errmsg"]
                temp["userlist"]=""
            #新增按钮
        elif request.POST.get("delete",None):
            act_groupid = request.POST.get("groupid", "")
            admin_list = getdata.getadmin(username)
            if act_groupid in admin_list:
                result = eval(api.del_group(act_groupid, token))
            else:
                result = {"errmsg":"无权删除"}
            if result["errmsg"] == "ok":
                temp["increase_label"] = "删除成功！"
                try:
                    getdata.delgroup(act_groupid)
                except:
                    temp["increase_label"] = "删除成功，本地数据库更新异常！请立即通知管理员！"
                group_list = getdata.getgroup()
                temp["group_list"] = group_list
                groupid = ""
            else:
                temp["increase_label"] = "删除失败：" + result["errmsg"]
            #删除按钮
        elif request.POST.get("add",None):
            act_userid = request.POST.get("userid","")
            admin_list = getdata.getadmin(username)
            if groupid in admin_list:
                result = eval(api.add_group(groupid, act_userid, token))
            else:
                result = {"errmsg":"无权添加"}
            if result["errmsg"] == "ok":
                temp["increase_labe2"] = "添加成功！"
            else:
                temp["increase_labe2"] = "添加失败：" + result["errmsg"]
            #添加按钮
        elif request.POST.get("remove",None):
            act_userid = request.POST.get("userid", "")
            admin_list = getdata.getadmin(username)
            if groupid in admin_list:
                result = eval(api.remove_group(groupid, act_userid, token))
            else:
                result = {"errmsg": "无权移除"}
            if result["errmsg"] == "ok":
                temp["increase_labe2"] = "移除成功！"
            else:
                temp["increase_labe2"] = "移除失败：" + result["errmsg"]
            #移除按钮
        elif request.POST.get("poweron",None):
            act_groupid = request.POST.get("admin_groupid", "")
            act_username = request.POST.get("admin_user", "")
            admin_list = getdata.getadmin(username)
            if act_groupid in admin_list:
                getdata.addadmin(act_groupid, act_username)
                temp["label3"]="已授权"
            else:
                temp["label3"]="无权授权"
            #授权按钮
        elif request.POST.get("poweroff",None):
            act_groupid = request.POST.get("admin_groupid", "")
            act_username = request.POST.get("admin_user", "")
            admin_list = getdata.getadmin(username)
            if act_groupid in admin_list:
                getdata.deladmin(act_groupid, act_username)
                temp["label3"] = "已除权"
            else:
                temp["label3"] = "无权除权"
            #除权按钮
        else:
            1
            # 返回页面
            # 通过token获取群组信息
        #显示可管理权限
        admin_list = getdata.getadmin(username)
        temp["adminlist"] = admin_list
        #userlist的默认显示
        if groupid:
            userlist, groupname = api.get_group(groupid, token)
            temp["userlist"] = userlist
        response = render(request, "group.html", temp)
        response.set_cookie('groupid', groupid, expires=3600)
        return response
