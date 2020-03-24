import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "FJw16pNs2The3H4GyM1iEQ",
	"isbns": "9781632168146"})
print(res.json())