
import os, sys, random
import xml.etree.ElementTree as ET
from glob import glob
import pandas as pd
from shutil import copyfile
#os, sys, random: utilitas umum. xml.etree.ElementTree: untuk parsing file .xml. glob: mencari semua file dengan pola tertentu (*.xml). pandas: menyimpan data ke DataFrame/CSV. shutil.copyfile: 
# (tidak digunakan di kode ini, bisa dihapus).
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
annotations = glob('BCCD/Annotations/*.xml')
#Ambil semua file XML dalam folder BCCD/Annotations.
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
df = []
cnt = 0
#df: list kosong untuk menampung data bounding box. cnt: counter (tidak wajib, hanya untuk referensi).
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
for file in annotations:
    #filename = file.split('/')[-1].split('.')[0] + '.jpg'
    #filename = str(cnt) + '.jpg'
    filename = file.split('\\')[-1]
    filename =filename.split('.')[0] + '.jpg'
    #Ambil nama file .xml, ubah ke nama file .jpg. Gunakan \\ agar cocok di Windows (untuk Linux/macOS ganti /).
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    row = []
    parsedXML = ET.parse(file)
    for node in parsedXML.getroot().iter('object'):
        blood_cells = node.find('name').text
        xmin = int(node.find('bndbox/xmin').text)
        xmax = int(node.find('bndbox/xmax').text)
        ymin = int(node.find('bndbox/ymin').text)
        ymax = int(node.find('bndbox/ymax').text)

        row = [filename, blood_cells, xmin, xmax, ymin, ymax]
        df.append(row)
        cnt += 1
    #Loop semua objek <object> dalam file XML. Ambil: name: jenis sel darah (RBC, WBC, Platelets). xmin, xmax, ymin, ymax: koordinat bounding box. Tambahkan ke list df.
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

data = pd.DataFrame(df, columns=['filename', 'cell_type', 'xmin', 'xmax', 'ymin', 'ymax'])

data[['filename', 'cell_type', 'xmin', 'xmax', 'ymin', 'ymax']].to_csv('Bounding_Box.csv', index=False)
#Konversi list df ke pandas DataFrame. Simpan ke file CSV bernama test.csv tanpa menyimpan indeks.
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
