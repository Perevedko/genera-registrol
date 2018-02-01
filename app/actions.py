import os, re, csv, zipfile

prezzi = [
    {'id': '144', 'price': 10, 'name': 'foobar'},
    {'id': '202', 'price': 10},
    {'id': '212', 'price': 10},
    {'id': '229', 'price': 10},
    {'id': '207', 'price': 10},
    {'id': '141', 'price': 10},
    {'id': '211', 'price': 10},
    {'id': '208', 'price': 10},
    {'id': '228', 'price': 10},
    {'id': '149', 'price': 10},
    {'id': '227', 'price': 10},
    {'id': '128', 'price': 10},
    {'id': '75',  'price': 10},
    {'id': '109', 'price': 10},
    {'id': '111', 'price': 10},
    {'id': '239', 'price': 10},
    {'id': '113', 'price': 10},
    {'id': '112', 'price': 10},
    {'id': '102', 'price': 10},
    {'id': '129', 'price': 10},
    {'id': '237', 'price': 10},
    {'id': '230', 'price': 10},
    {'id': '222', 'price': 10},
    {'id': '162', 'price': 10},
    {'id': '233', 'price': 10},
    {'id': '234', 'price': 10},
    {'id': '156', 'price': 10},
    {'id': '108', 'price': 10},
    {'id': '226', 'price': 10},
    {'id': '231', 'price': 10},
    {'id': '182', 'price': 10},
    {'id': '232', 'price': 10},
    {'id': '206', 'price': 10},
    {'id': '238', 'price': 10},
    {'id': '240', 'price': 10}
]

csv_file = os.path.join(os.getcwd(), 'csv.csv')

def process_folder_to_csv(folder, csv_file=csv_file):
    csvfile = csv.writer(open(csv_file, 'wb'), delimiter='$', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvfile.writerow(['Anno','Mese','Prod_ID','Prodotto','Qta','Reso','Abb','Copertina','Imponibile','IVA dovuta'])

    for root, subFolders, files in os.walk(folder):
        # print root
        for file in files:
            if file.endswith(".st"):
                # print file
                with open(os.path.join(root, file)) as fp:
                    da_a = re.findall('Dal\s(\d+/\d+/\d+)\sal\s(\d+/\d+/\d+)',fp.read())
                    # print da_a
                    fp.seek(0)

                    prodotto = re.findall('Prodotto:\s(\d+)\s[-]\s(.*)\r\n',fp.read())
                    # print prodotto
                    fp.seek(0)

                    correzione = re.findall('Nota di [accredito|variazione].*[-](\d+)\r',fp.read())
                    correzione = [int(i) for i in correzione]
                    #correzione = map(int, correzione)
                    # print sum(correzione)
                    #print correzione
                    fp.seek(0)

                    totale = re.findall('Totale venduto\s*(\d+)\r',fp.read())
                    copie = int(totale[0])+int(sum(correzione))
                    # print int(totale[0]), copie
                    fp.seek(0)
                    id = prodotto[0][0]
                    prezzi_elem = {}
                    for elem in prezzi:
                        if elem.get('id') == id:
                            prezzi_elem = elem
                    csvfile.writerow([
                        da_a[0][0][6:10],
                        da_a[0][0][3:5],
                        prodotto[0][0],
                        prodotto[0][1],
                        copie,
                        copie*0.7,
                        copie*0.3,
                        prezzi_elem.get('price', 0),
                        copie * 0.3 * prezzi_elem.get('price', 0),
                        copie * 0.3 * prezzi_elem.get('price', 0) * 0.04
                    ])


unzip_folder = os.path.join(os.getcwd(), 'unzipped')

def clear_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def unzip_file(zip_file_path):
    clear_folder(unzip_folder)
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(unzip_folder)
