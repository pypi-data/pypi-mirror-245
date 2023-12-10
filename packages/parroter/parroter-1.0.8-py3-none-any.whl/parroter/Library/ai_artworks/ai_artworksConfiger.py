import LibHanger.Library.uwLogger as Logger
from LibHanger.Library.uwGlobals import configer
from LibHanger.Library.uwGlobals import *
from parroter.Library.parroterConfiger import parroterConfiger
from parroter.Library.parroterGlobals import *
from parroter.Library.ai_artworks.ai_artworksConfig import ai_artworksConfig
from parroter.Library.ai_artworks.ai_artworksGlobals import ai_artworksGlobal

class ai_artworksConfiger(parroterConfiger):
    
    """
    ai_artworks共通設定クラス
    """
    
    def __init__(self, _tgv:ai_artworksGlobal, _file, _configFolderName = ''):
        
        """
        コンストラクタ
        """
        
        # ai_artworks.ini
        aaw = ai_artworksConfig()
        aaw.getConfig(_file)

        # gvセット
        _tgv.parroterConfig = aaw
        
        # ロガー設定
        Logger.setting(aaw)
