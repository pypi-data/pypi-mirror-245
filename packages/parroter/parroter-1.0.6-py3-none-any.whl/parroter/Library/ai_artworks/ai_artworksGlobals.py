from parroter.Library.parroterGlobals import parroterGlobal
from parroter.Library.ai_artworks.ai_artworksConfig import ai_artworksConfig

class ai_artworksGlobal(parroterGlobal):
    
    """
    AIAWグローバル設定クラス
    """
    
    def __init__(self):
        
        """
        コンストラクタ
        """
        
        # 基底側コンストラクタ呼び出し
        super().__init__()
        
        self.ai_artworksConfig:ai_artworksConfig = None
        """ AIAW共通設定 """

# インスタンス生成(import時に実行される)
gv = ai_artworksGlobal()