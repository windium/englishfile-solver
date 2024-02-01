import requests
import json
import xmltodict
import re
from time import sleep

class App:
    def __init__(self):
        self.lessonCount = 0
        self.activityCount = 0
        self.cookie = "oup-cookie=; authsessionId=; CSRFCOOKIES="
        self.payload = {
            "data": "{\"activityAttempts\":[{\"data\":\"{\\\"order\\\":1,\\\"maxScore\\\":8,\\\"state\\\":\\\"<state><attempts>-1</attempts></state>\\\"}\",\"unit\":\"12\",\"lesson\":\"01\",\"activity\":\"03\",\"fileName\":\"EF4e_03_12_01_03\",\"time\":161,\"activityType\":\"fill_in_blank_text\",\"score\":1,\"studentId\":0}],\"order\":1,\"maxScore\":8,\"state\":\"<state><attempts>-1</attempts></state>\"}",
            "unit": "12",
            "lesson": "01",
            "activity": "04",
            "fileName": "EF4e_03_12_01_04",
            "time": 160,
            "activityType": "fill_in_blank_sentence",
            "score": 1,
            "studentId": 0
        }
        self.headers = {
            "content-type": "application/json",
            "sec-ch-ua": "\"Not A(Brand\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"",
            "Referer": "https://englishfile4e.oxfordonlinepractice.com/",
            "Origin": "https://englishfile4e.oxfordonlinepractice.com",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "sec-ch-ua-platform": "\"Windows\"",
            "authority": "englishfile4e.oxfordonlinepractice.com",
            "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "accept-language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5",
            "cache-control": "no-cache",
            "cookie": self.cookie,
            "pragma": "no-cache",
            "referer": "https://englishfile4e.oxfordonlinepractice.com/app/dashboard/book/34/unit/12/lesson/01/activity/03",
            "sec-fetch-dest": "image",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "expires": "0",
            "timestamp": "Wed, 31 Jan 2024 12:58:36 GMT",
            "timezone": "01-31-2024 15:58:36+0300",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "image",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "cross-site",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "x-requested-with": "XMLHttpRequest",
            "origin": "https://englishfile4e.oxfordonlinepractice.com"
        }

    def run(self):
        # ENGLISHFILE 4e PreInt : bookId=02 bookId2=34
        # ENGLISHFILE 4e Int : bookId=03 bookId2=35
        self.bookId = "03"
        self.bookId2 = "35"
        self.unit = 1
        self.lesson = 1
        self.activityNo = 5
        self.getActivity(f"02", f"01", f"EF4e_{self.bookId}_02_01_01")
        self.loop(0)

    def loop(self, _):
        if(int(self.lesson) < self.lessonCount+1):
            if(self.activityNo < self.activityCount+1):
                activity = self.getActivity(f"{self.unit:02d}", f"{self.lesson:02d}", f"EF4e_{self.bookId}_{self.unit:02d}_{self.lesson:02d}_{self.activityNo:02d}")
                if(activity["activityType"] == "checkbox"): 
                    data = "{\"activityAttempts\":[{\"data\":\"{\\\"order\\\":1,\\\"maxScore\\\":1,\\\"state\\\":\\\"<state><attempts>1</attempts></state>\\\"}\",\"unit\":\""+f"{self.unit:02d}"+"\",\"lesson\":\""+f"{self.lesson:02d}"+"\",\"activity\":\""+f"{self.activityNo:02d}"+"\",\"fileName\":\""+f"EF4e_{self.bookId}_{self.unit:02d}_{self.lesson:02d}_{self.activityNo:02d}"+"\",\"time\":2,\"activityType\":\"checkbox\",\"score\":1,\"studentId\":0}],\"order\":1,\"maxScore\":1,\"state\":\"<state><attempts>1</attempts></state>\"}"
                    self.post(data, f"{self.unit:02d}", f"{self.lesson:02d}", f"{self.activityNo:02d}", f"EF4e_{self.bookId}_{self.unit:02d}_{self.lesson:02d}_{self.activityNo:02d}", activity["activityType"], activity["maxScore"])
                    self.activityNo = int(self.activityNo)+1
                    sleep(1)
                    self.loop(0)
                elif(activity["activityType"] == "fill_in_blank_text"):
                    print(f"{self.unit:02d} {self.lesson:02d} {self.activityNo:02d} is fill_in_blank_text")
                    answers = self.getAnswers(activity["fileName"], activity["activityType"])
                    strs = re.findall(r"\[(.*?)\]", str(answers)[1:])
                    strsEdited = [x.split("|")[0] for x in strs]
                    strsGapped = ["<gap>"+x+"</gap>" for x in strsEdited]
                    strsGapped = "".join(strsGapped)
                    maxScore = activity["maxScore"]
                    data = "{\"activityAttempts\":[{\"data\":\"{\\\"order\\\":1,\\\"maxScore\\\":"+f"{maxScore}"+",\\\"state\\\":\\\"<state>"+f"{strsGapped}"+"<attempts>1</attempts></state>\\\"}\",\"unit\":\""+f"{self.unit:02d}"+"\",\"lesson\":\""+f"{self.lesson:02d}"+"\",\"activity\":\""+f"{self.activityNo:02d}"+"\",\"fileName\":\""+f"EF4e_{self.bookId}_{self.unit:02d}_{self.lesson:02d}_{self.activityNo:02d}"+"\",\"time\":65,\"activityType\":\"fill_in_blank_text\",\"score\":"+f"{maxScore}"+",\"studentId\":0}],\"order\":1,\"maxScore\":"+f"{maxScore}"+",\"state\":\"<state>"+f"{strsGapped}"+"<attempts>-1</attempts></state>\"}"
                    self.post(data, f"{self.unit:02d}", f"{self.lesson:02d}", f"{self.activityNo:02d}", f"EF4e_{self.bookId}_{self.unit:02d}_{self.lesson:02d}_{self.activityNo:02d}", activity["activityType"], activity["maxScore"])
                    self.activityNo = int(self.activityNo)+1
                    sleep(1)
                    self.loop(0)
                elif(activity["activityType"] == "fill_in_blank_sentence"):
                    answers = self.getAnswers(activity["fileName"], activity["activityType"])
                    strs = re.findall(r"\[(.*?)\]", str(answers)[1:])
                    strsEdited = [x.split("|")[0] for x in strs]
                    strsGapped = ["<gap>"+x+"</gap>" for x in strsEdited]
                    strsGapped = "".join(strsGapped)
                    maxScore = activity["maxScore"]
                    data = "{\"activityAttempts\":[{\"data\":\"{\\\"order\\\":1,\\\"maxScore\\\":"+f"{maxScore}"+",\\\"state\\\":\\\"<state>"+f"{strsGapped}"+"<attempts>1</attempts></state>\\\"}\",\"unit\":\""+f"{self.unit:02d}"+"\",\"lesson\":\""+f"{self.lesson:02d}"+"\",\"activity\":\""+f"{self.activityNo:02d}"+"\",\"fileName\":\""+f"EF4e_{self.bookId}_{self.unit:02d}_{self.lesson:02d}_{self.activityNo:02d}"+"\",\"time\":65,\"activityType\":\"fill_in_blank_sentence\",\"score\":"+f"{maxScore}"+",\"studentId\":0}],\"order\":1,\"maxScore\":"+f"{maxScore}"+",\"state\":\"<state>"+f"{strsGapped}"+"<attempts>-1</attempts></state>\"}"
                    self.post(data, f"{self.unit:02d}", f"{self.lesson:02d}", f"{self.activityNo:02d}", f"EF4e_{self.bookId}_{self.unit:02d}_{self.lesson:02d}_{self.activityNo:02d}", activity["activityType"], activity["maxScore"])
                    self.activityNo = int(self.activityNo)+1
                    sleep(1)
                    self.loop(0)
                elif(activity["activityType"] == "dictation_multi_word"):
                    answers = self.getAnswers(activity["fileName"], activity["activityType"])
                    strs = re.findall(r"\[(.*?)\]", str(answers)[1:])
                    strsEdited = [x.split("|")[0] for x in strs]
                    strsGapped = ["<gap>"+x+"</gap>" for x in strsEdited]
                    strsGapped = "".join(strsGapped)
                    maxScore = activity["maxScore"]
                    data = "{\"activityAttempts\":[{\"data\":\"{\\\"order\\\":1,\\\"maxScore\\\":"+f"{maxScore}"+",\\\"state\\\":\\\"<state>"+f"{strsGapped}"+"<attempts>1</attempts></state>\\\"}\",\"unit\":\""+f"{self.unit:02d}"+"\",\"lesson\":\""+f"{self.lesson:02d}"+"\",\"activity\":\""+f"{self.activityNo:02d}"+"\",\"fileName\":\""+f"EF4e_{self.bookId}_{self.unit:02d}_{self.lesson:02d}_{self.activityNo:02d}"+"\",\"time\":65,\"activityType\":\"dictation_multi_word\",\"score\":"+f"{maxScore}"+",\"studentId\":0}],\"order\":1,\"maxScore\":"+f"{maxScore}"+",\"state\":\"<state>"+f"{strsGapped}"+"<attempts>-1</attempts></state>\"}"
                    self.post(data, f"{self.unit:02d}", f"{self.lesson:02d}", f"{self.activityNo:02d}", f"EF4e_{self.bookId}_{self.unit:02d}_{self.lesson:02d}_{self.activityNo:02d}", activity["activityType"], activity["maxScore"])
                    self.activityNo = int(self.activityNo)+1
                    sleep(1)
                    self.loop(0)
                elif(activity["activityType"] == "sentence_dropdown_text_only"):
                    answers = self.getAnswers(activity["fileName"], activity["activityType"])
                    strs = re.findall(r"\[(.*?)\]", str(answers)[1:])
                    strsEdited = [x.replace("\"","") for x in strs]
                    strsEdited = [x.split(" / ")[0] for x in strsEdited]
                    strsEdited = [x.replace("\\'", "\'") for x in strsEdited]
                    strsGapped = ["<gap>"+x+"</gap>" for x in strsEdited]
                    strsGapped = "".join(strsGapped)
                    maxScore = activity["maxScore"]
                    activityType = activity["activityType"]
                    data = "{\"activityAttempts\":[{\"data\":\"{\\\"order\\\":1,\\\"maxScore\\\":"+f"{maxScore}"+",\\\"state\\\":\\\"<state>"+f"{strsGapped}"+"<attempts>1</attempts></state>\\\"}\",\"unit\":\""+f"{self.unit:02d}"+"\",\"lesson\":\""+f"{self.lesson:02d}"+"\",\"activity\":\""+f"{self.activityNo:02d}"+"\",\"fileName\":\""+f"EF4e_{self.bookId}_{self.unit:02d}_{self.lesson:02d}_{self.activityNo:02d}"+"\",\"time\":65,\"activityType\":\""+f"{activityType}"+"\",\"score\":"+f"{maxScore}"+",\"studentId\":0}],\"order\":1,\"maxScore\":"+f"{maxScore}"+",\"state\":\"<state>"+f"{strsGapped}"+"<attempts>-1</attempts></state>\"}"
                    self.post(data, f"{self.unit:02d}", f"{self.lesson:02d}", f"{self.activityNo:02d}", f"EF4e_{self.bookId}_{self.unit:02d}_{self.lesson:02d}_{self.activityNo:02d}", activity["activityType"], activity["maxScore"])
                    self.activityNo = int(self.activityNo)+1
                    sleep(1)
                    self.loop(0)
                elif(activity["activityType"] == "sorting_text_only"):
                    answers = self.getAnswers(activity["fileName"], activity["activityType"])
                    strs = ""
                    for x in answers["bin"]:
                        for y in x["items"]["item"]:
                            header = x["header"]
                            header = header.replace("p>", "bin>")
                            y = y.replace("p>", "text>")
                            strs += f"<item>{y}{header}</item>"
                    maxScore = activity["maxScore"]
                    activityType = activity["activityType"]
                    data = "{\"activityAttempts\":[{\"data\":\"{\\\"order\\\":1,\\\"maxScore\\\":"+f"{maxScore}"+",\\\"state\\\":\\\"<state>"+f"{strs}"+"<attempts>1</attempts></state>\\\"}\",\"unit\":\""+f"{self.unit:02d}"+"\",\"lesson\":\""+f"{self.lesson:02d}"+"\",\"activity\":\""+f"{self.activityNo:02d}"+"\",\"fileName\":\""+f"EF4e_{self.bookId}_{self.unit:02d}_{self.lesson:02d}_{self.activityNo:02d}"+"\",\"time\":65,\"activityType\":\""+f"{activityType}"+"\",\"score\":"+f"{maxScore}"+",\"studentId\":0}],\"order\":1,\"maxScore\":"+f"{maxScore}"+",\"state\":\"<state>"+f"{strs}"+"<attempts>-1</attempts></state>\"}"
                    self.post(data, f"{self.unit:02d}", f"{self.lesson:02d}", f"{self.activityNo:02d}", f"EF4e_{self.bookId}_{self.unit:02d}_{self.lesson:02d}_{self.activityNo:02d}", activity["activityType"], activity["maxScore"])
                    self.activityNo = int(self.activityNo)+1
                    sleep(1)
                    self.loop(0)
                elif(activity["activityType"] == ("video_interactive" or "mc_image_answer_choices" or "matching_text_only" or "matching_text_audio" or "mc_questions_single_image")):
                    maxScore = activity["maxScore"]
                    activityType = activity["activityType"]
                    data = "{\"activityAttempts\":[{\"data\":\"{\\\"order\\\":1,\\\"maxScore\\\":"+f"{maxScore}"+",\\\"state\\\":\\\"<state><attempts>1</attempts></state>\\\"}\",\"unit\":\""+f"{self.unit:02d}"+"\",\"lesson\":\""+f"{self.lesson:02d}"+"\",\"activity\":\""+f"{self.activityNo:02d}"+"\",\"fileName\":\""+f"EF4e_{self.bookId}_{self.unit:02d}_{self.lesson:02d}_{self.activityNo:02d}"+"\",\"time\":65,\"activityType\":\""+f"{activityType}"+"\",\"score\":"+f"{maxScore}"+",\"studentId\":0}],\"order\":1,\"maxScore\":"+f"{maxScore}"+",\"state\":\"<state><attempts>-1</attempts></state>\"}"
                    self.post(data, f"{self.unit:02d}", f"{self.lesson:02d}", f"{self.activityNo:02d}", f"EF4e_{self.bookId}_{self.unit:02d}_{self.lesson:02d}_{self.activityNo:02d}", activity["activityType"], activity["maxScore"])
                    self.activityNo = int(self.activityNo)+1
                    sleep(1)
                    self.loop(0)
                else:
                    print(f"{self.unit:02d} {self.lesson:02d} {self.activityNo:02d} is not count type skipping")
                    self.activityNo = int(self.activityNo)+1
                    self.loop(0)
            else:
                print("there is no activity in this lesson")
                self.activityNo = 1
                self.lesson = int(self.lesson)+1
                self.loop(0)
        else:
            print("there is no lesson in this lesson")
            self.activityNo = 1
            self.lesson = 1
            self.unit = int(self.unit)+1
            self.loop(0)

    def post(self, data, unit, lesson, activity, fileName, activityType, score):
        self.payload["data"] = data
        self.payload["unit"] = unit
        self.payload["lesson"] = lesson
        self.payload["activity"] = activity
        self.payload["fileName"] = fileName
        self.payload["activityType"] = activityType
        self.payload["score"] = score

        #print(self.payload)
        response = requests.post(
            f"https://englishfile4e.oxfordonlinepractice.com/api/books/{self.bookId2}/activities",
            headers=self.headers,
            json=self.payload,
        )
        print(response.json())

    def getAnswers(self, activityNo, activityType):
        response = requests.get(
            f"https://englishfile4e.oxfordonlinepractice.com/common-components/activities-data/activities/{activityType}/{activityNo}.xml?nocache=1426453202872",
        )
        xml_data = xmltodict.parse(response.text)
        json_data = json.dumps(xml_data)
        data = json.loads(json_data)
        if(activityType == "sorting_text_only"):
            return data[activityType]["bins"]
        else:
            item = data[activityType]["items"]["item"]
            if(len(item) > 1): 
                return item
            else:
                return item["text"]

    def getActivity(self, unitNo, lessonNo, activityNo):
        response = requests.get(
            f"https://englishfile4e.oxfordonlinepractice.com/api/books/{self.bookId2}/activities",
            headers=self.headers
        )
        data = json.loads(response.content)

        unit = next(x for x in data["data"]["units"] if x["unit"] == unitNo)

        lesson = next(x for x in unit["lessons"] if x["lesson"] == lessonNo)

        activity = next(x for x in lesson["activities"] if x["fileName"] == activityNo)

        self.lessonCount = len(unit["lessons"])
        self.activityCount = len(lesson["activities"])

        return activity
