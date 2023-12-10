from LibHanger.Library.uwConfig import cmnConfig

class StabdifspyConfig(cmnConfig):
    
    """
    Stabdifspy共通設定クラス(RolexReserverConfig)
    """ 
    
    class settingValueStruct(cmnConfig.settingValueStruct):

        """
        設定値構造体
        """ 

    def __init__(self):
        
        """
        コンストラクタ
        """
        
        # 基底側コンストラクタ
        super().__init__()
        
        self.stableDiffusionSiteUrl = ''
        """ StableDiffusion Site URL """
        
        self.endpointTxt2Img = ''
        """ EndPoint txt2img """
        
        self.outputDirName = ''
        """ Pic Output directoryName """
        
        self.outputFileNameFormat = ''
        """ Pic Output filename format """
        
        self.promptJsonPath = ''
        """ PromptJsonFile Path """
        
        self.processAbortFile = 'stopper.txt'
        """ process abort file """

        # 設定ファイル名追加
        self.setConfigFileName('Stabdifspy.ini')
        
    def getConfig(self, _scriptFilePath: str, configFileDir: str = ''):
        
        """ 
        設定ファイルを読み込む 
        
        Parameters
        ----------
        _scriptFilePath : str
            スクリプトファイルパス
        configFileDir : str
            設定ファイルの格納場所となるディレクトリ
        """

        # 基底側のiniファイル読込
        super().getConfig(_scriptFilePath, configFileDir)
        
    def setInstanceMemberValues(self):
        
        """ 
        インスタンス変数に読み取った設定値をセットする
        """
        
        # 基底側実行
        super().setInstanceMemberValues()
        
        # StableDiffusion Site URL
        self.setConfigValue('stableDiffusionSiteUrl',self.config_ini,'SITE','STABLEDIFFUSION_SITE_URL',str)

        # EndPoint txt2img
        self.setConfigValue('endpointTxt2Img',self.config_ini,'ENDPOINT','TXT2IMG',str)

        # Pic Output directoryName
        self.setConfigValue('outputDirName',self.config_ini,'DIR','OUTPUT_DIR',str)
        
        # Pic FileName format
        self.setConfigValue('outputFileNameFormat',self.config_ini,'DEFAULT','OUTPUT_FILE_FORMAT',str)
        
        # PromptJsonFile Path
        self.setConfigValue('promptJsonPath',self.config_ini,'DIR','PROMPT_JSON_PATH',str)
        
        # process abort file
        self.setConfigValue('processAbortFile',self.config_ini,'ABORT','PROCESS_ABORT_FILE',str)
        