import os
import random
from parroter.Library.parroterBase import parroterBase
from parroter.Library.ai_artworks.ai_artworksConfig import ai_artworksConfig
from parroter.Library.ai_artworks.ai_artworksGlobals import gvAaw
from Stabdifspy.Generator.Stab import GeStab
from Stabdifspy.Library.StabdifspyGlobals import gvStab

class ai_artworksBot(parroterBase):
    
    """
    AIAWクラス
    """
        
    def __init__(self, rootPath, lang:str = parroterBase.botLang.jp) -> None:
        
        """
        コンストラクタ

        Parameters
        ----------
        rootPath : str
            ルートパス
        lang : str
            言語
        """
        
        # 基底側コンストラクタ
        super().__init__(rootPath, lang)
        
        # gvに設定情報をセット
        gvAaw.config = self.config
        gvAaw.ai_artworksConfig = self.settingConfig(rootPath)
        
        # AIAW共通設定をメンバ変数にセット
        self.parroterConfig = gvAaw.ai_artworksConfig
        
        # TwitterClient設定
        self.setTwitterClient()
        # TwitterApi設定
        self.setTwitterApi()
        
        # ログ出力先設定
        self.settingLogOutputPath()
        
        # Payload確保用変数
        self.Payload = {}
        
    def appName(self):
        
        """
        アプリ名
        """

        return 'ai_artworks'
    
    def settingConfig(self, rootPath):
        
        """
        parroter共通設定
        
        Parameters
        ----------
        rootPath : str
            ルートパス
        """
        
        # ai_artworks.ini
        kc = ai_artworksConfig()
        kc.getConfig(rootPath, os.path.join(self.config.startupCfg.configFolderPath, self.appName()))

        return kc
    
    def getHelloTweetText(self):
        
        """
        挨拶文を取得する
        """
        
        # 挨拶文の定型テキスト文取得
        return self.getHelloTweetTemplateText()
    
    def getHelloTweetImage(self):
        
        """
        ツイート画像アップロードパスを返す
        """
        
        # ツイート画像アップロードパスを返す
        return self.generateTweetImage(self.rootPathFull)
    
    def getHelloTweetTemplateText(self):

        """
        挨拶定型文を取得する
        """
        
        with open(os.path.join(
            self.rootPath, 
            self.parroterConfig.appListDir, 
            self.parroterConfig.appHelloTextFileName),'r',encoding='utf-8') as f:
            helloTemplateText= f.read()
        
        return helloTemplateText
            
    def generateTweetImage(self, _scriptFilePath):
        
        """
        ツイート画像を生成する
        """
        
        # GeStabクラスインスタンス生成
        gs = GeStab(gvStab, _scriptFilePath)
        # Payload確保
        self.Payload = gs.payLoad

        # 画像生成
        return gs.generatePicture(), gs.payLoad
