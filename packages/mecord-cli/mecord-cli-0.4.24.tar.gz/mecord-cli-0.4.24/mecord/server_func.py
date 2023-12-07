import requests
import os
import json, time
from urllib.parse import *
from PIL import Image

from mecord import xy_pb
from mecord import store
from mecord import taskUtils
from mecord import utils
from pathlib import Path 

class MecordAIGCTask:
    funName = None
    country = None
    ready = None

    def __init__(self, func: str, taskUUID=None):
        if store.is_multithread() or taskUUID != None:
            self.country = taskUtils.taskCountryWithUUID(taskUUID)
        else:
            firstTaskUUID, self.country = taskUtils.taskInfoWithFirstTask()
        if self.country == None:
            self.country = "test"
            
        self.checking = False
        self.result = False, "Unknow"
        self.widgetid = xy_pb.findWidget(self.country, func)
        if self.widgetid <= 0:
            print(f"widget {func} not found with {self.country}")
            self.ready = False
            return
        self.checkUUID = ""
        self.checkCount = 0
        self.funName = func
        self.ready = True
        
    def syncCall(self, params):
        if self.ready == False:
            return None

        self.checkUUID = xy_pb.createTask(self.country, self.widgetid, params)
        self.checking = True
        self.checkCount = 0
        while self.checking or self._timeout():
            finish, success, data = xy_pb.checkTask(self.country, self.checkUUID)
            if finish:
                self.checking = False
                if success == False:
                    raise Exception(f"aigc fail, reason={data}")
                return data
            self.checkCount += 1
            time.sleep(1)
        return None

    def _timeout(self):
        return self.checkCount > 600
    
class TTSFunc(MecordAIGCTask):
    text = None
    def __init__(self, text: str, taskUUID=None):
        super().__init__("TaskTTS", taskUUID)
        self.text = text

    def syncCall(self, roles: list[dict]) -> tuple[float, str]:
        data = super().syncCall({
            "mode": 0,
            "param":{
                "messages": [
                    {
                        "content": self.text,
                        "roles": roles,
                    }
                ],
                "task_types": [
                    "generate_tts"
                ]
            }
        })
        try:
            tts_url = data[0]["content"]["tts_results"][0]["tts_mp3"]
            tts_duration = data[0]["content"]["tts_results"][0]["duration"]
            return tts_duration, tts_url
        except:
            return 0, None
        
class Txt2ImgFunc(MecordAIGCTask):
    text = None
    def __init__(self, text: str, taskUUID=None):
        super().__init__("TaskChapterImage", taskUUID)
        self.text = text

    def syncCall(self, roles: list[dict]) -> str:
        data = super().syncCall({
            "mode": 0,
            "param":{
                "messages": [
                    {
                        "content": self.text,
                        "content_summary": self.text,
                        "is_content_finish": True,
                        "message_type": "normal",
                        "roles": roles,
                    }
                ],
                "task_types": [
                    "generate_chapter_image"
                ]
            }
        })
        try:
            return data[0]["content"]["chapter_image_urls"][0]
        except:
            return None
        

# tts_duration, tts_url = TTSFunc("啊哈哈哈哈，这是什么呀").syncCall()
# if tts_duration > 0:
#     print(f"tts成功。生成音频长度为{tts_duration}, 链接为{tts_url}")

# img_url = Txt2ImgFunc("啊哈哈哈哈，这是什么呀").syncCall()
# if img_url:
#     print(f"文生图成功   {img_url}")
