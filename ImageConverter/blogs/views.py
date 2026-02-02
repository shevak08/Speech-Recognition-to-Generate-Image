from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime

def homepage(request):
    return render(request,"index.html",{})

def login(request):
    return render(request,"login.html",{})

import MySQLdb
con=MySQLdb.connect("localhost","root","","ImageConverter")
c1=con.cursor()
def registration(request):
    if request.method=="POST":
        name = request.POST["t1"]
        mailid = request.POST["t2"]
        mno = request.POST["t3"]
        uid = request.POST["t4"]
        pwd = request.POST["t5"]
        c1.execute("insert into users values('%s','%s','%s','%s','%s')"
                   %(name,mailid,mno,uid,pwd))
        con.commit()
        return render(request, "registration.html",
                      {"msg": "New User Registered!!"})
    return render(request,"registration.html",{})

def login(request):
    if request.method=="POST":
        uid = request.POST["t1"]
        pwd = request.POST["t2"]
        c1.execute("select * from users where userid='%s' and password='%s'"%
                   (uid,pwd))
        if c1.rowcount>=1:
            return redirect(userhome)
        else:
            return render(request, "login.html", {"msg":"You're not authorized user"})
    return render(request,"login.html",{})

def userhome(request):
    return render(request, "userhome.html", {})

def about(request):
    return render(request,"about.html",{})

def contact(request):
    return render(request,"contact.html",{})

def signout(request):
    return render(request,"index.html",{})

import speech_recognition as sr

def speech_text(request):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Talk")
        audio_text = r.listen(source)
        print("Time over, thanks")
        try:
            text = r.recognize_google(audio_text, language="en-IN")
            print("User Saying : "+str(text))
            return render(request,"ImageConverter.html",{"text":str(text)})
        except:
            print("Sorry, I did not get that")


def ImageConverter(request):
    text_images={"kids with cycling":"cycling2.jpg","men with cycling":"cycling.jpg","peacock feather":"peacock.jpg","men with dog":"dog.jpg",
                 "elephant with men":"elephant.jpg","elephant eating":"elephant2.jpg","playing cricket":"cricket1.jpg","people in beach":"beach.jpg",
                 "horse in beach":"horse1.jpg","horse riding":"horse2.jpg","kids in park":"park.jpg","peacock feather spreading":"peacock.jpg",
                 "people in rain":"rain.jpg","people in flood":"rain2.jpg","people swimming":"swim.jpg","tiger hunting":"tiger1.jpg",
                 "tiger in zoo":"tiger2.jpg","men in umbrella":"umbrella.jpg","sachin with bat":"sachin.jpeg","cricket":"cricket.jpeg"}
    if request.method=="POST":
        start_time = datetime.now()
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Talk")
            audio_text = r.listen(source)
            print("Time over, thanks")
            try:
                text = r.recognize_google(audio_text, language="en-IN")
                print("User Saying : " + str(text))
            except:
                print("Sorry, I did not get that")

        #text = request.POST["t1"]
        print(text)


        flag = text in text_images.keys()
        print(flag)
        if flag:
            image = text_images[text]
            print(image)
            end_time = datetime.now()
            process_time=end_time - start_time
            #print(process_time)
            #print(start_time)
            #print(process_time)
            #print(end_time)
            process_time=str(process_time)
            index=process_time.rfind(":")+1
            process_time=process_time[index:]
            process_time=float(process_time)/100
            #print(process_time)
            #process_time=int(process_time)/100
            process_time="{:.2f}".format(process_time)
            print(process_time)
            #end_time=end_time[5:]
            #end_time=int(end_time)/100
            return render(request, "ImageConverter.html",
                          {"flag":flag,"image":image,"text":text,"total_time":process_time})
        else:
            return render(request, "ImageConverter.html",
                          {"flag":flag,"msg": "Image could not search for the given text!!",
                           "text":text})
    return render(request,"ImageConverter.html",{})


from django.http import FileResponse
from django.conf import settings

def download_file(request,filename):
    filepath=str(settings.BASE_DIR)+"/activity_images/"+filename
    response = FileResponse(open(filepath,"rb"))
    response['Content-Disposition'] = 'attachment; filename=' + filename
    return response