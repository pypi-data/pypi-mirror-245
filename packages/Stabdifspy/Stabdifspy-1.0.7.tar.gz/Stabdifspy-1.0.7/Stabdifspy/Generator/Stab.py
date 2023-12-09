import os
import requests
import base64
import time
import json
import LibHanger.Library.uwLogger as Logger
from Stabdifspy.Library.StabdifspyGlobals import StabdifspyGlobal

class GeStab():
    """
    GeStabクラス
    """
    
    def __init__(self, _gv:StabdifspyGlobal, _rootPath) -> None:
        """
        コンストラクタ
        """

        # ルートパスを取得
        self.rootPath = _rootPath

        # 共通設定取得
        self.gv = _gv
        
        # Payload初期化
        self.payLoad = {}
        
    def generatePicture(self):
        """
        画像生成
        """
        
        # Get - response
        response = requests.post(url=self.gv.StabdifspyConfig.stableDiffusionSiteUrl + self.gv.StabdifspyConfig.endpointTxt2Img , json=self.getPayload())

        # parametersをログ出力
        Logger.logging.info(response.json()["parameters"])
        
        # 出力ディレクトリチェック
        if (not os.path.dirname(self.rootPath)):
            os.makedirs(os.path.dirname(self.rootPath), exist_ok=True)
        
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
        Payload取得
        """

        jsonFilePath = os.path.join(os.path.dirname(self.rootPath), self.gv.StabdifspyConfig.promptJsonPath)
        with open(jsonFilePath) as f:
            self.payLoad = json.loads(f.read())
        return self.payLoad