from LibHanger.Library.uwGlobals import globalValues
from Stabdifspy.Library.StabdifspyConfig import StabdifspyConfig

class StabdifspyGlobal(globalValues):
    
    def __init__(self):
        
        """
        コンストラクタ
        """
        
        # 基底側コンストラクタ呼び出し
        super().__init__()

        self.StabdifspyConfig:StabdifspyConfig = None
        """ Stabdifspy共通設定 """

# インスタンス生成(import時に実行される)
gvStab = StabdifspyGlobal()
