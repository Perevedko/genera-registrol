import os, re, csv, zipfile

prezzi = { "75" : 10, "102" : 10, "108" : 10, "109" : 10, "111" : 10, "112" : 10, "113" : 10, "128" : 10, "129" : 10, "141" : 10, "144" :10, "149" : 10, "156" : 10, "162" : 10, "182" : 10, "202" : 10, "206" : 10, "207" : 10, "208" : 10, "211" : 10, "212" : 10, "222" : 10, "226" : 10, "227" : 10, "228" : 10, "229" : 10, "230" : 10, "231" : 10, "232" : 10, "233" : 10, "234" : 10, "237" : 10, "238" : 10, "239" : 10, "240" : 10 }
# what is prezzi?

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

                    csvfile.writerow([
                        da_a[0][0][6:10],
                        da_a[0][0][3:5],
                        prodotto[0][0],
                        prodotto[0][1],
                        copie,
                        copie*0.7,
                        copie*0.3,
                        prezzi.get(prodotto[0][0], 0),
                        copie*0.3*prezzi.get(prodotto[0][0], 0),
                        copie*0.3*prezzi.get(prodotto[0][0], 0)*0.04
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
