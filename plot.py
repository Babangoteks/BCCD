
# importing required libraries
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import patches
import os

def filterFiles(directoryPath, extension):
    """
        This function filters the format files with the selected extension in the directory
        
        Args:
            directoryPath (str): relative path of the directory that contains text files
            extension (str): extension file

        Returns:
            The list of filtered files with the selected extension
    """    
    relevant_path = directoryPath
    included_extensions = [extension]
    file_names = [file1 for file1 in os.listdir(relevant_path) if any(file1.endswith(ext) for ext in included_extensions)]
    numberOfFiles = len(file_names)
    listParams = [file_names, numberOfFiles]
    return listParams
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
[image_names, numberOfFiles] = filterFiles("BCCD/JPEGImages", "jpg")    

trainRCNN = pd.read_csv('test.csv', sep=",", header=None)
trainRCNN.columns = ['filename', 'cell_type', 'xmin', 'xmax', 'ymin', 'ymax']
trainRCNN.head() 
#Ambil semua gambar .jpg di folder BCCD/JPEGImages. Baca CSV bounding box tanpa header. Tetapkan nama kolom sesuai urutan data.
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

for imageFileName in image_names:    
    fig = plt.figure()
    #add axes to the image
    ax = fig.add_axes([0,0,1,1]) #adding X and Y axes from 0 to 1 for each direction 
    plt.axis('off') #Untuk setiap file gambar: Buat figure dan axes tanpa sumbu. Baca dan tampilkan gambar.
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # read and plot the image
    image = plt.imread('BCCD/JPEGImages/' + imageFileName)
    plt.imshow(image)
    # iterating over the image for different objects
    for _,row in trainRCNN[trainRCNN.filename == imageFileName].iterrows():
        xmin = float(row.xmin)
        xmax = float(row.xmax)
        ymin = float(row.ymin)
        ymax = float(row.ymax)
        
        width = xmax - xmin
        height = ymax - ymin
        ClassName= row.cell_type 
        # Ambil semua baris bounding box untuk gambar tertentu. Ambil koordinat dan ukuran box.
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # assign different color to different classes of objects
        if row.cell_type == 'RBC':
            ax.annotate('RBC', xy=(xmax-40,ymin+20))
            rect = patches.Rectangle((xmin,ymin), width, height, edgecolor = 'r', facecolor = 'none')
        elif row.cell_type == 'WBC':
            ax.annotate('WBC', xy=(xmax-40,ymin+20))
            rect = patches.Rectangle((xmin,ymin), width, height, edgecolor = 'b', facecolor = 'none')
        elif row.cell_type == 'Platelets':
            ax.annotate('Platelets', xy=(xmax-40,ymin+20))
            rect = patches.Rectangle((xmin,ymin), width, height, edgecolor = 'g', facecolor = 'none')        
        else:
            print("nothing")
    
        ax.add_patch(rect)   
        #Tambah label kelas (annotate) dan kotak (Rectangle) sesuai warnanya: RBC = merah (r) WBC = biru (b) Platelets = hijau (g)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if not os.path.exists("imagesBox"):
            os.makedirs("imagesBox")

        fig.savefig('imagesBox/' + imageFileName, dpi=90, bbox_inches='tight')
    plt.close()
    print("ImageName: " + imageFileName + " is saved in imagesBox folder")
        
print("PLOTBOX COMPLETED!")
#Cek folder imagesBox, buat jika belum ada. Simpan gambar dengan anotasi ke dalam folder itu. Tutup plot agar tidak boros memori. Cetak status untuk tiap gambar. Memberi tahu proses selesai.
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------       