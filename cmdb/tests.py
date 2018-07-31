from django.test import TestCase
import requests
# Create your tests here.

token ="Oi4M_NEuP4-8NmcZt-pmokxjflAfpoZ_1P6hbQC-z2YFlYfnnshZYirGfsCgYwMKT09d4089DxnZ5Eu8T9ONaw"
group_list=[("family@roobo.com","hanyu"),]
url = "https://api.exmail.qq.com/cgi-bin/group/get?access_token="+ token + "&groupid=" + group_list[0][0]
print(url)
html = requests.get(url)
list = html.json()
print(list)