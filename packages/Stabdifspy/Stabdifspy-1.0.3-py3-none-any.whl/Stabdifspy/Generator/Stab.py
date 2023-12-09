import os
import requests
import base64
import time
from Stabdifspy.Library.StabdifspyGlobals import *

class GeStab():
    """
    GeStabクラス
    """
    
    def __init__(self, _rootPath) -> None:
        """
        コンストラクタ
        """

        # ルートパスを取得
        self.rootPath = _rootPath
    
    def generatePicture(self):
        """
        画像生成
        """
        
        # Get - response
        response = requests.post(url=gv.StabdifspyConfig.stableDiffusionSiteUrl + gv.StabdifspyConfig.endpointTxt2Img , json=self.getPayload())

        # parametersをログ出力
        print(response.json()["parameters"])
        
        # ファイル名
        filePath = os.path.join(
            os.path.dirname(self.rootPath), 
            gv.StabdifspyConfig.outputDirName, 
            gv.StabdifspyConfig.outputFileNameFormat.format(int(time.time())))

        # 画像生成
        with open(filePath, "wb") as f:
            f.write(base64.b64decode(response.json()["images"][0]))

        # ファイルパスを返す
        return filePath
    
    def getPayload(self):
        """
        payload取得
        """

        return {
            "prompt":"line stamp, 1girl, solo, chain, Chibi, Half-smile, Santa Claus, comic, blue eyes, long hair, headphones, parted lips, black hair",
            "negative_prompt": "worst quality, large head, low quality, extra digits, bad eye, EasyNegativeV2, ng_deepnegative_v1_75t, text"
        }