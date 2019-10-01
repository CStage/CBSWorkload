from bs4 import BeautifulSoup
import requests
import re
import pylab

def test():
    r=requests.get("https://kursuskatalog.cbs.dk/2018-2019/BA-BPOLO1278U.aspx")

    soup=BeautifulSoup(r.content, "html.parser")

#    print(soup.prettify())
    body=soup.body
    #print(body.contents[1])
    WorkLoad=body.find_all(id="WorkloadContainer")

    #print(body.find_all(id="WorkloadContainer"))
    for connect in body.find(id="WorkloadContainer").find_all("td"):
        print(connect)


#    print("td is: ",body.find(id="WorkloadContainer").td)
#    print("Double sibling is:", body.find(id="WorkloadContainer").td.next_sibling.next_sibling)
    hourlist=body.find(id="WorkloadContainer").find_all(string=re.compile("hours"))
    #print(body.find(id="WorkloadContainer").find_all(string=re.compile("hours")))

    TotalHourList=[0,0,0]
    index=0
    for hours in hourlist:
        hours=hours.strip(" hours")
#        print(hours)
        TotalHourList[index]+=float(hours)
        index+=1
    print(TotalHourList)

def CreateListOfURLS(URLS=None):
    URLList=[]
    Finished=False
    while Finished==False:
        CourseInput=input("Give me the URL of your course: ")
        if CourseInput==".":
            print("List done")
#            print(URLList)
            Finished=True
        else:
            URLList.append(CourseInput)

    URLLIST=list(dict.fromkeys(URLLIST))
    return URLList



def CalculateAllHours(ListOfURLS):
    print("Calculating...")
    TotalHourList=[0,0,0]
    for URL in ListOfURLS:
        print("This is the URL", URL)
        r=requests.get(URL)
        soup=BeautifulSoup(r.content, "html.parser")
        body=soup.body
        hourlist=body.find(id="WorkloadContainer").find_all(string=re.compile("hours"))
        index=0
        if len(hourlist)>3:
            print("Oh boy. Here we go")
            for connect in body.find(id="WorkloadContainer").find_all("td"):
                if "Preparation" in str(connect):
                    print("Connect", connect)
                    print("PREPARATION FOUND!")
#                        TotalHours[0]=float(connect.next_sibling.next_sibling)
                    val=str(connect.next_sibling.next_sibling)
                    val=val.strip("<td>")
                    val=val.strip("</td>")
                    val=val.strip(" hours")
                    print("Prepval", val)
                    val=val.strip(" hours")
                    TotalHourList[0]+=float(val)
                if "Lecture" in str(connect) or "Exercise" in str(connect):
                    print("LECTURE / EXERCISE FOUND!")
                    val=str(connect.next_sibling.next_sibling)
                    val=val.strip("<td>")
                    val=val.strip("</td>")
                    val=val.strip(" hours")
                    print("Classval", val)
                    TotalHourList[1]+=float(val)
#                        TotalHours[1]=float(connect.next_sibling.next_sibling)
                if "Exam" in str(connect):
                    print("EXAM FOUND!")
                    val=str(connect.next_sibling.next_sibling)
                    val=val.strip("<td>")
                    val=val.strip("</td>")
                    val=val.strip(" hours")
                    print("Examval", val)
                    val=val.strip(" hours")
                    TotalHourList[2]+=float(val)
#                        print("Float", float(connect.next_sibling.next_sibling))
        else:
            for hours in hourlist:
                hours=hours.strip(" hours")
#            print(hours)
                TotalHourList[index]+=float(hours)
                index+=1
#        print("TotalHourList", TotalHourList)
    print("Done")
    return TotalHourList

def CreateHistogram(HoursList):
    colors=["green", "red", "purple"]
    pylab.figure()
    pylab.title("Hours spent at IBP")
    pylab.xlabel("Allocation")
    pylab.ylabel("Time")
    x=pylab.arange(3)
    pylab.bar(x, height=HoursList, color=colors)
    pylab.xticks(x, ["Prep", "Lectures/Exercises", "Exam"])
#    pylab.hist(x, HoursList)
    pylab.show()

def AutoHours(LinkToCourses=None):
    StartOfStudy=input("When did you start studying? a: 2018, b:2019: ")
    r=requests.get("https://kursuskatalog.cbs.dk/search.aspx?level_programme=BA%C2%A4HA-POL")

    soup=BeautifulSoup(r.content, "html.parser")

    body=soup.body
    AutoGenerate=[]
    for link in body.find_all("a"):
        AutoGenerate.append(link.get("href"))
#<        print(link.get("href"))

        for element in AutoGenerate:
            if StartOfStudy=="a" or StartOfStudy=="A":
                if "2018-2019" not in element:
                    AutoGenerate.remove(element)
            if StartOfStudy=="b" or StartOfStudy=="B":
                if "2019-2020" not in element:
                    AutoGenerate.remove(element)
        CleanUp=[]
        for element in AutoGenerate:
            CleanUp.append("https://kursuskatalog.cbs.dk/" + str(element))

    CleanUp=list(dict.fromkeys(CleanUp))

    print(CleanUp, "Year of study:", StartOfStudy)
    return CleanUp


#NewList=CreateListOfURLS()
#TotalHours=CalculateAllHours(NewList)
#print(TotalHours)
#CreateHistogram(TotalHours)

#test()

#Courses=AutoHours()
#TotalHours=CalculateAllHours(Courses)
#print(TotalHours)
#CreateHistogram(TotalHours)

#Use below to create a tree, where one can pick their studies, then move it on
#to ask for year of study. There's a problem with electives/internship

def HoldOnForLater():
    r=requests.get("https://kursuskatalog.cbs.dk/search.aspx")

    soup=BeautifulSoup(r.content, "html.parser")
    body=soup.body
    StudyDict={}
    for option in body.find_all("option"):
        if "option value" in str(option):
            if "BA" in str(option) or "DIP" in str(option) or "MA" in str(option) or "KAN" in str(option) or "PHD" in str(option):
                Raw=str(option)
                Code=Raw.strip("<option value=")
                Code=Code.split(">", 1)[0]
#                print(Code)
#                print(Raw)
                Study=Raw.split(">", 1)[1]
                Study=Study.split("<", 1)[0]
                Study=Study.lstrip()
#                print(Study)
                StudyDict[str(Code)]=str(Study)
            else:
#                print("oops")
                pass
    print(StudyDict)

HoldOnForLater()
#What would be really cool is if you were able to just type your program and your year
#and then it collects all the data
