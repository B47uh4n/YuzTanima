import cv2
import os
import tkinter
import customtkinter
from recognition import FaceRecognition


# Batuhan Demirci

def Take():
    #degiskenler
    vid = cv2.VideoCapture(0)
    directory = r"faces" #yuz fotograflarimi faces klasorunde tutacagim bu yuzden programin duzgunce calisabilmesi icin faces klasorunun silinmemesi gerek.
    cwd = os.getcwd() #programin working dir her pcde farkli olacagi icin bu veriyi dinamik olarak aliyorum.

    #faces klasorundeki imglardan bir liste olusturuyorum bu liste sayesinde kontroller saglayabilicem.
    RegisteredNames = []
    for image in os.listdir('faces'):
        RegisteredNames.append(image)
        

    try:
        userN = name.get()
        userPng = f"{userN}.png"
    except:
        finishLabel.configure(text="Hata olustu")

    if userPng in RegisteredNames:
        finishLabel.configure(text="Farkli bir isim giriniz!!", text_color="red")
    elif userN == "":
        finishLabel.configure(text="Lutfen kutucugu doldurunuz!!", text_color="red")
    else:
        finishLabel.configure(text="---------------Yuzunuz sisteme basariyla kaydedildi!!---------------\n", text_color="green")

        while(True):
            ret, image = vid.read()
            cv2.imshow("image", image)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            os.chdir(directory)
            cv2.imwrite(f"{userN}.png", image)

            os.chdir(cwd) # burasi
            
           
        vid.release()
        #bu butun pencereleri kapatma kodu sikinti olabilir dikkat.
        cv2.destroyAllWindows()
        #app.destroy()    

    
#ui icin sistem gorunus modu ve mavi tema yapiyorum.
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")
#pencere ayarlari
app = customtkinter.CTk()
app.geometry("854x480")
app.title(" Yuz Tanima Sistemi")

# kullanici elementleri
tanitLbl = customtkinter.CTkFrame(app,corner_radius=10)
tanitLbl.pack(pady=30)
title = customtkinter.CTkLabel(tanitLbl, text="\nYüzünüzü tanitmak icin adinizi Türkçe karakter kullanmadan assagidaki kutucuga girip fotograf cek butonuna basabilirsiniz.\n\nKamera acildiginda yuzunuzun gozuktugunden emin olup q tusuna basiniz!")
title.pack(padx=10, pady=10)

#adsoyad girdi
name_var = tkinter.StringVar()
name = customtkinter.CTkEntry(tanitLbl, width=350, height=40, textvariable=name_var)
name.pack()

#isim onay ve fotografcek butonu        
go = customtkinter.CTkButton(tanitLbl, text="Fotograf Cek",command=Take)
go.pack(padx=10,pady=10)

#kaydedildi-hata dinamik labeli
finishLabel= customtkinter.CTkLabel(app, text="")
finishLabel.pack()


#yuz tanima label ve buton
mylabelframe = customtkinter.CTkFrame(app,corner_radius=10)
mylabelframe.pack(pady=30)
title2 = customtkinter.CTkLabel(mylabelframe, text="\nYuzunuz veritabanimiza kayit olduysa Yuz Tanima butonu ile yuzunuzu okutabilirsiniz.\n\nKamerayi kapatmak icin q tusuna basabilirsiniz.")
title2.pack(padx=10, pady=10)
fr = FaceRecognition()
go2 = customtkinter.CTkButton(mylabelframe, text="Yuz Tanima",command=lambda : [fr.encode_faces(), fr.run_recognition()])
go2.pack(padx=10,pady=10)

sign = customtkinter.CTkLabel(app, text="Batuhan Demirci")
sign.pack(padx=10)

app.mainloop()


    

#if __name__ == '__main__':
 #   pht = photo()
  #  pht.menu()
    
