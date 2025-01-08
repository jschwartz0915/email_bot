import requests

# url = "http://localhost:8000/api/send-emails"
# files = {'file': ('sample_excel.csv', open('sample_excel.csv', 'rb'), 'text/csv')}
# headers = {'accept': 'application/json'}
#
# response = requests.post(url, headers=headers, files=files)
# print(response.status_code, response.text)

url = "http://localhost:8000/health"
response = requests.get(url)
print(response.status_code, response.text)


