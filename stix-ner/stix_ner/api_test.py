import requests
url = "http://127.0.0.1:8000/ctiner"
data = {"text": "A cybercriminal group known as Ember Fox launched a campaign against an energy sector company by exploiting an unpatched Apache Struts vulnerability (CVE-2017-5638) in a public-facing web server. They deployed Metasploit to gain a reverse shell, then installed NanoCore RAT for persistence and surveillance. Analysts detected the intrusion through unusual outbound traffic to dynamic DNS domains and new registry run keys"}
print(data)
response = requests.post(url, json=data)
print(response.text)