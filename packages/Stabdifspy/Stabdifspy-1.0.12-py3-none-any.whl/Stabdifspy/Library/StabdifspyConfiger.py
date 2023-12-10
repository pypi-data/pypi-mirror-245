import LibHanger.Library.uwLogger as Logger
from LibHanger.Library.uwGlobals import configer
from LibHanger.Library.uwGlobals import *
from Stabdifspy.Library.StabdifspyGlobals import *

class StabdifspyConfiger(configer):
    
    """
    Stabdifspy共通設定クラス
    """
    
    def __init__(self, _tgv:StabdifspyGlobal, _file, _configFolderName = ''):
        
        """
        コンストラクタ
        """
        
        # Stabdifspy.ini
        da = StabdifspyConfig()
        da.getConfig(_file, _configFolderName)

        # gvセット
        _tgv.StabdifspyConfig = da
        
        # ロガー設定
        Logger.setting(da)
