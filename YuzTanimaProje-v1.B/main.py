from recognition import FaceRecognition
import cv2
import os
import tkinter
import customtkinter
import photo
# pip install cmake dlib==19.22
# burada main bir sayfa olsun 2 yeni sekmelere gitmek istedim olmayinca vazgectim burasi bir ise yaramaz calistirmayin!

if __name__ == '__main__':
    
    #ui icin sistem gorunus modu ve mavi tema yapiyorum.
    customtkinter.set_appearance_mode("system")
    customtkinter.set_default_color_theme("blue")

    #pencere ayarlari
    app2 = customtkinter.CTk()
    app2.geometry("720x480")
    app2.title("surat tanima")

    #kullanici elementleri
    title = customtkinter.CTkLabel(app2, text="Yüzünüzü kayit etmek icin yuz kayit, yuzunuzu taratmak icin yuz tanima butonuna basin")
    title.pack(padx=10, pady=10)

    #yuz kayit buton
    btn1 = customtkinter.CTkButton(app2, text="yuz kayit",command=photo.Take)
    btn1.pack(padx=10,pady=10)

    #yuz tarama buton
    
    btn2 = customtkinter.CTkButton(app2,text="yuz kayit")



    app2.mainloop()
    

    #fr = FaceRecognition()
    #fr.run_recognition()
