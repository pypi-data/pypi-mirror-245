from LibHanger.Library.uwGlobals import globalValues
from parroter.Library.parroterConfig import parroterConfig

class parroterGlobal(globalValues):
    
    """
    parroterグローバル設定クラス
    """
    
    def __init__(self):
        
        """
        コンストラクタ
        """
        
        # 基底側コンストラクタ呼び出し
        super().__init__()
        
        self.parroterConfig:parroterConfig = None
        """ parroter共通設定 """

# インスタンス生成(import時に実行される)
gv = parroterGlobal()
