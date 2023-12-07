"""
Name : gm_login_utils.py
Author  : 池泽琴
Contact : 邮箱地址
Time    : 2023-10-07 14:36
Desc:
"""
import hashlib
import json
import time

import requests
from gmmysql.mysqlexe import OperateMysql
from enum import Enum
from urllib3.exceptions import InsecureRequestWarning
import urllib3

urllib3.disable_warnings(InsecureRequestWarning)

class LoginDomain(Enum):
	"""登录域名设置枚举"""
	login_uri = 'djc-gateway/authing/login'
	user_uri = 'gateway/v1/user?requireAvatar=true'
	# test1配置
	test1_djc = "https://www.djctest1.gm/"
	test1_zcj = 'https://www.cqzcjtest1.gm/'
	test1_xcj = 'https://www.xcjtest1.gm/'
	test1_zdb = 'https://zdb.xcjtest1.gm/'
	# show配置
	show_djc = "https://www.djcshow.gm/"
	show_zcj = 'https://www.gpwbeta.com/'
	show_xcj = 'https://www.cqzcjshow.com/'
	show_zdb = 'https://zdb.cqzcjshow.com/'
	# test2配置
	test2_djc = "https://www.djctest2.gm/"
	test2_zcj = 'https://www.cqzcjtest2.gm/'
	test2_xcj = 'https://www.xcjtest2.gm/'



class LoginData(Enum):
	"""登录头、登录URI等枚举"""
	form_headers = {'content-type': 'application/x-www-form-urlencoded'}
	login_uri = 'djc-gateway/authing/login'
	application_headers = {'Content-type': 'application/json'}

	# 登录时传递form表单的数据定义如下，请根据各环境配置
	zcj_test1_login_data_dict = {
		'origin': 'https://www.cqzcjtest1.gm',
		'password': '402522cea3acc6228192fec58a7b8a79',
		'client_id': 'plat@ZCJ',
		'scope': 'www.cqzcjtest1.gm',
		'options': '',
		'response_type': 'code',
		'redirect_uri': 'https://www.cqzcjtest1.gm/gateway/v1/login',
		'certLoginProvider': 'ezca',
		'success_uri': 'https://www.cqzcjtest1.gm/login-app/login-success/index.html',
		'state': '{"client_id": "plat@ZCJ", "scope": "www.cqzcjtest1.gm", "redirect_uri": "https://www.cqzcjtest1.gm/gateway/v1/login"}'
	}

	xcj_test1_login_data_dict = {
		'origin': 'https://www.cqzcjtest1.gm',
		'password': '402522cea3acc6228192fec58a7b8a79',
		'client_id': 'plat@ZCJ',
		'scope': 'www.cqzcjtest1.gm',
		'options': '',
		'response_type': 'code',
		'redirect_uri': 'https://www.cqzcjtest1.gm/gateway/v1/login',
		'certLoginProvider': 'ezca',
		'success_uri': 'https://www.cqzcjtest1.gm/login-app/login-success/index.html',
		'state': '{"client_id": "plat@ZCJ", "scope": "www.cqzcjtest1.gm", "redirect_uri": "https://www.cqzcjtest1.gm/gateway/v1/login"}'
	}

	zcj_show_login_data_dict = {
		'origin': 'https://www.gpwbeta.com',
		'password': '402522cea3acc6228192fec58a7b8a79',
		'client_id': 'plat@ZCJ',
		'scope': 'www.gpwbeta.com',
		'options': '',
		'response_type': 'code',
		'redirect_uri': 'https://www.gpwbeta.com/gateway/v1/login',
		'certLoginProvider': 'ezca',
		'success_uri': 'https://www.gpwbeta.com/login-app/login-success/index.html',
		'state': '{"client_id": "plat@ZCJ", "scope": "www.gpwbeta.com", "redirect_uri": "https://www.gpwbeta.com/gateway/v1/login"}'
	}

	xcj_show_login_data_dict = {
		'origin': 'https://www.cqzcjshow.com',
		'password': '402522cea3acc6228192fec58a7b8a79',
		'client_id': 'plat@XCJ',
		'scope': 'www.cqzcjshow.com',
		'options': '',
		'response_type': 'code',
		'redirect_uri': 'https://www.cqzcjshow.com/gateway/v1/login',
		'certLoginProvider': 'ezca',
		'success_uri': 'https://www.cqzcjshow.com/login-app/login-success/index.html',
		'state': '{"client_id": "plat@XCJ", "scope": "www.cqzcjtest1.gm", "redirect_uri": "https://www.cqzcjshow.com/gateway/v1/login"}'
	}

def _second_verify(resp, login_org):
	"""第一次验证不通过时获取返回值，并传入待登录的单位名称，返回EMPLOEE"""
	try:
		identities = json.loads(resp.text).get('identities')
		identities_id = [x['id'] for x in identities if x['name'] == str(login_org)][0]
		return identities_id
	except IndexError as e:
		print(f"二次验证未获取到单位名称,请传入单位名称。当前单位名称：{login_org}")

def login_zcj(session, env, user_name, org_name=None):
	"""政采机房登录，需传入session，环境名称env，登录用户账号user_name，登录单位org_name且默认为空"""
	env = env.strip().lower()
	login_data_dict_name = f'zcj_{env}_login_data_dict'  # 根据env参数替换登录data字典
	login_domain = f'{env}_zcj'   # 根据env参数替换环境
	try:
		login_data_dict_copy = getattr(LoginData, login_data_dict_name).value.copy()   # 封装登录data字典
		get_token_url = getattr(LoginDomain, login_domain).value + LoginDomain.login_uri.value  # 组装登录url
		user_info_url = getattr(LoginDomain, login_domain).value + LoginDomain.user_uri.value
		login_data_dict_copy['username'] = user_name  # 根据账号，在data字典中添加username的键值对
		# 登录
		res = session.post(get_token_url, headers=LoginData.form_headers.value, data=login_data_dict_copy, verify=False)
		# 获取登录人基本信息--user接口
		user_info = session.get(user_info_url, verify=False)
		# 账号如有多单位时，无法确定登录身份，需再次选择登录单位
		if res.status_code == 400 or '无法确定登陆身份' in res.text:  # 新登录机制，当返回400或返回有无法确定登陆身份的文本，则走二次验证
			print(f"二次登录机制--当返回400或返回有无法确定登陆身份的文本时，需要指定登录单位。\n"
			      f"当前登录单位是：{org_name}")
			login_data_dict_copy['identityId'] = _second_verify(res, org_name)  # 传入org_name可登录
			res = session.post(get_token_url, headers=LoginData.form_headers.value, data=login_data_dict_copy, verify=False)
			user_info = session.get(user_info_url, verify=False)
			return session  # 返回请求session
		elif res.status == 106 or '极验证' in res.text:
			print(f"本次登录触发极验证机制")
			get_token_url = get_token_url + "?geetest_challenge=111111&geetest_seccode=111111&geetest_validate=111111"
			res = session.post(get_token_url, headers=LoginData.form_headers.value, data=login_data_dict_copy, verify=False)
			return session
		else:
			return session
	except AttributeError:
		raise ValueError(f'Invalid environment: {env}')

def login_xcj(session, env, user_name, org_name=None):
	"""行采机房登录，需传入session，环境名称env，登录用户账号user_name，登录单位org_name且默认为空"""
	env = env.strip().lower()
	login_data_dict_name = f'xcj_{env}_login_data_dict'
	login_domain = f'{env}_xcj'
	try:
		login_data_dict_copy = getattr(LoginData, login_data_dict_name).value.copy()  # 封装登录data字典
		get_token_url = getattr(LoginDomain, login_domain).value + LoginDomain.login_uri.value  # 组装登录url
		user_info_url = getattr(LoginDomain, login_domain).value + LoginDomain.user_uri.value  # 组装用户信息url
		login_data_dict_copy['username'] = user_name
		# 登录
		res = session.post(get_token_url, headers=LoginData.form_headers.value, data=login_data_dict_copy, verify=False)
		# 获取登录人基本信息--user接口
		user_info = session.get(user_info_url, verify=False)
		# 账号如有多单位时，无法确定登录身份，需再次选择登录单位
		if res.status_code == 400 or '无法确定登陆身份' in res.text:  # 新登录机制，当返回400或返回有无法确定登陆身份的文本，则走二次验证
			print(f"二次登录机制--当返回400或返回有无法确定登陆身份的文本时，需要指定登录单位。\n"
			      f"当前登录单位是：{org_name}")
			login_data_dict_copy['identityId'] = _second_verify(res, org_name)  # 传入org_name可登录
			res = session.post(get_token_url, headers=LoginData.form_headers.value, data=login_data_dict_copy, verify=False)
			user_info = session.get(user_info_url, verify=False)
			return session  # 返回请求session
		elif res.status_code == 106 or '极验证' in res.text:
			print(f"本次登录触发极验证机制")
			get_token_url = get_token_url + "?geetest_challenge=111111&geetest_seccode=111111&geetest_validate=111111"
			res = session.post(get_token_url, headers=LoginData.form_headers.value, data=login_data_dict_copy, verify=False)
			return session
		else:
			return session
	except AttributeError:
		raise ValueError(f'Invalid environment: {env}')


if __name__ == '__main__':
	session = requests.session()
	req = login_zcj(session, 'test1', '18502120689', '远大空调有限公司')  # 如果账号属于多个单位，请传入待登录单位；
	req1 = login_xcj(session, 'test1', '13760187099', '大江大河')
	print(LoginData.__doc__)


