import face_recognition
import os, sys
import cv2
import numpy as np
import math


# surat yuzde kac eslesme sagliyor bunu hesaplamak için bircok algoritma var bunu sectik.
def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'


class FaceRecognition:
    #Calisma aninda alacagimiz verileri icine koymak ve gerektiginde verileri kıyaslayabilmek icin listlerimizi tanimliyoruz.
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True

    #constructor olarak olusan nesne encode_faces fonksiyonu cagirmaktan vazgectik.
    #def __init__(self):
     #   self.encode_faces()
        
    

    #encode faces ile faces klasorundeki gorsellerimi encode edip bilinen suratlar listeme ekliyorum
    #gorsel isimlerini de bilinen surat isimleri olarak listeme ekliyorum ve konsola isimleri gormek icin yazdiriyorum
    def encode_faces(self):
        for image in os.listdir('faces'):
            face_image = face_recognition.load_image_file(f"faces/{image}")
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)
            #program calisirken yuz fotografi kaydettikten sonra bilinen isimlerimizi de guncellemek icin encode faces fonksiyonunu cagiriyoruz.
            #encode faces her cagirildiginda listeye isimleri append ettigi icin ayni isimler arka arkaya eklenebilir bunu engellemek icin;
            # q ile kameramiz kapanirken bilinen isimler listemizi temizleyecegiz
            #self.known_face_names = list(set(self.known_face_names)) -> self ile unique yapmak ise yaramiyor cunku sira karisiyor.

        #konsol ekraninda kontrol saglamak icin degerlerimizi print ediyorum.    
        print(self.known_face_names)
        print(face_encoding)

    #yuz tanima fonksiyonumu yazmaya basliyorum.
    def run_recognition(self):
        video_capture = cv2.VideoCapture(0) #0 default webcamdir pcde varsa onu kullanacagim

        if not video_capture.isOpened(): #eger default webcami acamadiysam webcam bulunamadi yazdiriyorum.
            sys.exit('Video source not found...')

        while True:
            ret, frame = video_capture.read()

            # sadece o anki kareyi islemek icin if kontrolu
            if self.process_current_frame:
                #Daha hızlı bir surat tanıma islemi yapabilmek icin Video cercevesini 1/4 oraninda kucultuyorum
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                
                # Gorseli openCV ile actigimiz icin BGR renk kanalini kullaniyor
                # Fakat face_recognition kutuphanesini kullanmak icin gorseli RGB renk bandina cevirmemiz gerekiyor
                rgb_small_frame = small_frame[:, :, ::-1]

                # calisma zamaninda videonun o anki karesinde olan suratlarin konumunu buluyorum
                self.face_locations = face_recognition.face_locations(small_frame)

                # ekranda buldugum surat lokasyonlarini encode edip listee atiyorum
                # bu listeyi daha sonra bildigimiz suratlarla karsilastiracagiz
                self.face_encodings = face_recognition.face_encodings(small_frame, self.face_locations)

                self.face_names = []

                # calisma zamaninda encode ettigim suratlari tek tek geziyorum bilinen encode edilmis gorsellerimle kiyasliyorum
                for face_encoding in self.face_encodings:
                    
                    # Kiyaslama sonucunda eslesme sonuclarini matches listeme atiyorum
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)

                    #default olarak isim ve tahmin gerceklik degeri (guveni) bilinmeyen yani unknown olarak ayarliyorum. 
                    name = "Unknown"
                    confidence = '???'

                    # Calculate the shortest distance to face
                    # surata en yakin olan mesafeyi hesaplayip buldugumuz index degerini kiyaslama listemiz olan matchesa veriyoruz
                    # Boylece en yuksek oranda benzeyen suratların indexini bulmus oluyoruz 
                    # Bu indexteki surat ismini ve en yukarda yazmis oldugumuz guven algoritmasini ilgili degiskenlere ekliyoruz.
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        confidence = face_confidence(face_distances[best_match_index])

                    self.face_names.append(f'{name} ({confidence})')

            # Kodun daha saglikli olması icin sonuclari yazdirmadan hemen once o anki goruntuyu islemeyi birakmak icin bool degerimizi
            # false yapiyoruz.
            self.process_current_frame = not self.process_current_frame

            # Sonuclari goruntuleme kisimi
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                # 1/4 oraninda kucultulmus bir cercevede suratlari tespit ettigimiz icin surat lokasyonlarini 4le carparak
                # normal yerlerine getiriyoruz.
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                
                # Suratimizin etrafinda olusacak cerceveyi yapip isimimizi yazdiriyoruz.
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

            # Sonucta ulastigimiz gorseli goruntuluyoruz.
            cv2.imshow('Yuz Tanima -cikmak icin Q basiniz.', frame)

            # Programdan cikmak icin q tusuna basilmasini bekliyoruz
            if cv2.waitKey(1) == ord('q'):
                #kamera kapanirken bilinen isimler listemi temizliyorum cunku buton ile tekrar cagirilirsam listeyi bastan doldurarak
                #yeni isimleri de almak isterim. listeyi temizlemezsek eski isimler ust uste eklenmiş olur.
                self.known_face_names = []
                break

        # pencerelerimizi kapatiyoruz.
        video_capture.release()
        cv2.destroyAllWindows()

# denemeler yaparken dogrudan bu kodu compile ederek de programimizi calistirabilmek icin __name__ kullandik.
if __name__ == '__main__':
    fr = FaceRecognition()
    fr.run_recognition()

#Batuhan Demirci