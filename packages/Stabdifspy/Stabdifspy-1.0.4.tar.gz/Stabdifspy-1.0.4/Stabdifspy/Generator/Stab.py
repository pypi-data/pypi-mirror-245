import os
import requests
import base64
import time

class GeStab():
    """
    GeStabクラス
    """
    
    def __init__(self, _gv, _rootPath) -> None:
        """
        コンストラクタ
        """

        # ルートパスを取得
        self.rootPath = _rootPath

        # 共通設定取得
        self.gv = _gv
        
    def generatePicture(self):
        """
        画像生成
        """
        
        # Get - response
        response = requests.post(url=self.gv.StabdifspyConfig.stableDiffusionSiteUrl + self.gv.StabdifspyConfig.endpointTxt2Img , json=self.getPayload())

        # parametersをログ出力
        print(response.json()["parameters"])
        
        # ファイル名
        filePath = os.path.join(
            os.path.dirname(self.rootPath), 
            self.gv.StabdifspyConfig.outputDirName, 
            self.gv.StabdifspyConfig.outputFileNameFormat.format(int(time.time())))

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