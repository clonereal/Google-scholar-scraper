from bs4 import BeautifulSoup
import requests, lxml, os, json
import pandas as pd
import csv
from csv import writer

print("This code is modified by Yash. For usage, feel free to contact me")
for x in range(99):
  a = 'https://scholar.google.com/scholar?start='
  b = str(x)
  c = '0&q=political+radicalisation+of+youth+through+mass+media&hl=en&as_sdt=0,5'
#   a = 'https://scholar.google.com/scholar?start='
#   c = '0&q='
#   d = zz
#   e = '&hl=en&as_sdt=0,5'
  urrl = (a+b+c)
  headers = {
      'User-agent':
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
  }
  proxies = {
  'http': os.getenv('HTTP_PROXY') # or just type proxy here without os.getenv()
  }
  html = requests.get(urrl, headers=headers, proxies=proxies).text

  soup = BeautifulSoup(html, 'lxml')
  for pdf_link in soup.select('.gs_or_ggsm a'):
      pdf_file_link = pdf_link['href']
      print(pdf_file_link)

  data = []
  for result in soup.select('.gs_ri'):
      title = result.select_one('.gs_rt').text
      try:
          title_link = result.select_one('.gs_rt a')['href']
      except:
          pass
      publication_info = result.select_one('.gs_a').text
      snippet = result.select_one('.gs_rs').text
      cited_by = result.select_one('#gs_res_ccl_mid .gs_nph+ a')['href']
      related_articles = result.select_one('a:nth-child(4)')['href']
      try:
          all_article_versions = result.select_one('a~ a+ .gs_nph')['href']
      except:
          all_article_versions = None

      data.append(
          {
          'title': title,
          'title_link': title_link,
          'publication_info': publication_info,
          'snippet': snippet,
          'cited_by': f'https://scholar.google.com{cited_by}',
          'related_articles': f'https://scholar.google.com{related_articles}',
          'all_article_versions': f'https://scholar.google.com{all_article_versions}',
          })

  json_object = json.dumps(data,indent = 4)
  with open("sample.json", "a") as outfile:
      outfile.write(json_object)

  print(json.dumps(data, indent = 2, ensure_ascii = False))
