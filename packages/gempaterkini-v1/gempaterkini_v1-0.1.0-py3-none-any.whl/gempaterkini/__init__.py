
import requests
from bs4 import BeautifulSoup


def data_extraction():

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        content = requests.get('https://bmkg.go.id', headers=headers)
    except Exception:
        return None

    if content.status_code == 200:
        soup =  BeautifulSoup(content.text, 'html.parser')
        result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        result = result.findAll('li')

        i = 0
        magnitudo = None
        kedalaman = None
        koordinat = None
        pusat = None
        dirasakan = None


        for res in result:


            if i == 0:
                waktu = res.text.split(', ')
                tanggal = waktu[0]
                jam = waktu[1]
            elif i == 1:
                magnitudo = res.text
            elif i == 2:
                kedalaman = res.text
            elif i == 3:
                koordinat = res.text

            elif i == 4:
                pusat = res.text
            elif i == 5:
                dirasakan = res. text
            i = i + 1

        hasil = dict()

        hasil['waktu'] = {'tanggal' : tanggal, 'jam' : jam}
        hasil['magnitudo'] = magnitudo
        hasil['kedalaman'] = kedalaman
        hasil['koordinat'] = koordinat
        hasil['pusat'] =  pusat
        hasil['dirasakan'] = dirasakan
        return hasil
    else:
        return None

def show_data(result):
  if result is None:
    print("======Cannot find data======")
    return

  print(f"waktu : {result['waktu']['tanggal']}, {result['waktu']['jam']}")
  print(f"magnitudo : {result['magnitudo']}")
  print(f"kedalaman : {result['kedalaman']}")
  print(f"koordinat : {result['koordinat']} ")
  print(f"pusat : {result['pusat']}")
  print(f"dirasakan : {result['dirasakan']}")


if __name__ == '__main__':
    print("================================")
    print("Earthquake Detection Application")
    print("================================")

    result = data_extraction()
    show_data(result)




