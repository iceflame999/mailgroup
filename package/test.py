
from package import getdata
from package import gettoken
import time

group_list = getdata.getgroup()
api = gettoken.mailapi()
token = api.token
value = []

for groupid in group_list:
    userlist, groupname = api.get_group(groupid[0], token)
    for user in userlist:
        getdata.addadmin(groupid[0],user)
        time.sleep(2)


