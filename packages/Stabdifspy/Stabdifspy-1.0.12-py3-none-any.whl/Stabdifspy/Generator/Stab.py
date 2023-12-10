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

        # ルートパスをログ出力
        Logger.logging.info(self.rootPath)
        
        # ファイル名
        baseFilePath = os.path.join(
            os.path.dirname(self.rootPath), 
            self.gv.StabdifspyConfig.outputDirName, 
            self.gv.StabdifspyConfig.outputFileNameFormat.format(int(time.time())))

        # 出力ディレクトリチェック
        if (not os.path.exists(os.path.dirname(baseFilePath))):
            os.makedirs(os.path.dirname(baseFilePath), exist_ok=True)

        # 出力パスをログ出力
        Logger.logging.info(baseFilePath)

        # 画像生成
        filelist = []
        fileCount = 0
        for image in response.json()["images"]:
            fileCount += 1
            filePath = os.path.join(os.path.dirname(baseFilePath), os.path.splitext(os.path.basename(baseFilePath))[0] + str(fileCount) + os.path.splitext(baseFilePath)[1])
            with open(filePath, "wb") as f:
                f.write(base64.b64decode(image))
                filelist.append(filePath)

        # ファイルパスを返す
        return filelist
    
    def getPayload(self):
        """
        Payload取得
        """

        jsonFilePath = self.gv.StabdifspyConfig.promptJsonPath
        print('j:' + jsonFilePath)
        with open(jsonFilePath) as f:
            self.payLoad = json.loads(f.read())
        return self.payLoad