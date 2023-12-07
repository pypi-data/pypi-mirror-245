from parroter.Library.parroterConfig import parroterConfig

class ai_artworksConfig(parroterConfig):
    
    """
    AIAW共通設定クラス(ai_artworksConfig)
    """ 
    
    class wise_saying_pattern():
        
        """
        名言パターンリスト
        """
        
        def __init__(self):
            
            """
            コンストラクタ
            """
            
            self.pattern = ''
            self.font_name = ''
            self.say_ipX = 0
            self.say_ipY = 0
            self.say_fontSize = 0
            self.say_indentYPoint = 0
            self.say_txtHeight = 0
            self.category_ipX = 0
            self.category_ipY = 0
            self.category_fontSize = 0
            self.category_indentYPoint = 0
            self.category_txtHeight = 0
            self.speaker_ipX = 0
            self.speaker_ipY = 0
            self.speaker_fontSize = 0
            self.speaker_indentYPoint = 0
            self.speaker_txtHeight = 0
            self.category_label = ''

    def __init__(self):
        
        """
        コンストラクタ
        """
        
        # 基底側コンストラクタ
        super().__init__()

        self.wiseSayingJsonDir = ''
        """ 名言json格納先ディレクトリ """

        self.wiseSayingTweetNoLogDir = ''
        """ 名言TweetNoログ格納先ディレクトリ """

        self.wiseSayingJsonFileName = ''
        """ 名言jsonファイル名 """

        self.wiseSayingPtrnJsonFileName = ''
        """ 名言パターンリストjsonファイル名 """

        self.wiseSayingTweetNoLogFileName = ''
        """ 名言TweetNoログファイル名 """

        self.wiseSayingPattern = self.wise_saying_pattern()
        """ 名言パターンリスト """

        self.replyTweetNoLogFileName = ''
        """ 返信TweetNoログファイル名 """

        self.lastnameTargetStrTextFileName = ''
        """ 苗字判定用テキストファイル名 """
        
        # 設定ファイル名追加
        self.setConfigFileName('ai_artworks.ini')
        
    def getConfigFileName(self):
        
        """ 
        設定ファイル名 
        """

        return 'ai_artworks.ini'
    
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

        # wise_saying - json - FileName
        super().setConfigValue('wiseSayingJsonDir',self.config_ini,'DIR','WISE_SAYING_JSON_DIR',str)

        # wise_saying - json - FileName
        super().setConfigValue('wiseSayingTweetNoLogDir',self.config_ini,'DIR','WISE_SAYING_LOG_DIR',str)
        
        # wise_saying - json - FileName
        super().setConfigValue('wiseSayingJsonFileName',self.config_ini,'FILE','WISE_SAYING_JSON_FILENAME',str)

        # wise_saying_pattern - json - FileName
        super().setConfigValue('wiseSayingPtrnJsonFileName',self.config_ini,'FILE','WISE_SAYING_PATTERN_JSON_FILENAME',str)

        # wise_saying - log - FileName
        super().setConfigValue('wiseSayingTweetNoLogFileName',self.config_ini,'FILE','WISE_SAYING_LOG_FILENAME',str)

        # reply - log - FileName
        super().setConfigValue('replyTweetNoLogFileName',self.config_ini,'FILE','REPLY_LOG_FILENAME',str)

        # lastname_targetStr_txt-FileName
        super().setConfigValue('lastnameTargetStrTextFileName',self.config_ini,'FILE', 'LAST_NAME_TARGET_STR_TXT_FILENAME',str)
        