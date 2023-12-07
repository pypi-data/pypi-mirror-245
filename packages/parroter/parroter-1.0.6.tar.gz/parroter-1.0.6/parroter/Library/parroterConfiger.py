import LibHanger.Library.uwLogger as Logger
from LibHanger.Library.uwGlobals import configer
from LibHanger.Library.uwGlobals import *
from parroter.Library.parroterGlobals import *
from parroter.Library.ai_artworks.ai_artworksConfig import ai_artworksConfig

class parroterConfiger(configer):
    
    """
    parroter共通設定クラス
    """
    
    def __init__(self, _tgv:parroterGlobal, _file, _configFolderName = ''):
        
        """
        コンストラクタ
        """
        
        # parroter.iniv 
        da = ai_artworksConfig()
        da.getConfig(_file)

        # gvセット
        _tgv.parroterConfig = da
        
        # ロガー設定
        Logger.setting(da)
