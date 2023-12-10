import os
import sys
import math
import datetime
import tweepy
import urllib3
import LibHanger.Library.uwLogger as Logger
from twython import TwythonError
from LibHanger.Library.uwConfig import cmnConfig
from parroter.Library.parroterConfig import parroterConfig

class parroterBase():
    
    """
    parroter基底クラス
    """
    
    class botLang():
        
        """
        言語設定
        """
        
        jp = 'Jp'
        """ 日本語 """

        en = 'En'
        """ 英語 """

    def __init__(self, rootPath, lang:str = botLang.jp) -> None:
        
        """
        コンストラクタ
        
        Parameters
        ----------
        rootPath : str
            ルートパス
        lang : str
            言語
        """

        # 言語設定
        self._lang = lang
        
        # LibHanger.ini
        dc = cmnConfig()
        dc.getConfig(rootPath)
        
        # ロガー設定
        Logger.setting(dc)
        
        # 共通設定
        self.config = dc
        self.parroterConfig:parroterConfig = None
        
        # TwitterClient初期化
        self.twitterClient = None
        # TwitterApi初期化
        self.twitterApi = None
        
        # ルートパス
        self.rootPathFull = rootPath
        self.rootPath = os.path.dirname(rootPath)
    
    @property
    def appName(self):
        
        """
        アプリ名
        """

        return ''
    
    def settingLogOutputPath(self):
        
        """
        ログ出力先設定
        """
        
        # ログ出力先ディレクトリを作成
        self.hello_id_dir, self.reply_log_dir = self.createLogOutputDir()
        
        # ログ出力先取得
        self.hello_id_path, self.reply_log_path = self.getLogOutputPath(self.hello_id_dir, self.reply_log_dir)
    
    def settingConfig(self):
        
        """
        parroter共通設定(派生側でオーバーライドする)
        """
        
        pass
    
    def setTwitterClient(self):
        
        """
        TwitterClientを設定する
        """
        
        # キートークン設定
        self.twitterClient = tweepy.Client(
            consumer_key=self.parroterConfig.consumer_key,
            consumer_secret=self.parroterConfig.consumer_secret,
            access_token=self.parroterConfig.access_token,
            access_token_secret=self.parroterConfig.access_token_secret,
        )

    def setTwitterApi(self):
        
        """
        TwitterApiを設定する
        """
        
        auth = tweepy.OAuthHandler(
            self.parroterConfig.consumer_key,
            consumer_secret=self.parroterConfig.consumer_secret
        )
        auth.set_access_token(
            self.parroterConfig.access_token,
            self.parroterConfig.access_token_secret,
        )
        # TwitterApiを設定する
        self.twitterApi = tweepy.API(auth)
        
    def tweetHello(self):
        
        """
        挨拶をツイートする
        """
        
        # 挨拶ツイート内容の設定
        helloTweetText = self.getHelloTweetText()

        # ツイートに含める画像の設定
        try:
            helloTweetImage, promptData = self.getHelloTweetImage()
        except urllib3.exceptions.MaxRetryError as e:
            # エラーロギング
            Logger.logging.error(e.args)
            # 処理を停止
            sys.exit(1)
        except Exception as e:
            # エラーロギング
            Logger.logging.error(e.args)
            # 処理を停止
            sys.exit(1)
        
        # 挨拶ツイートのArgument設定
        helloTweetText = helloTweetText.format(str(datetime.datetime.now()), promptData['prompt'].strip())

        # 挨拶をツイートする
        response, result = self.tweet(helloTweetText, helloTweetImage)
        if result:
            
            try:
                
                # 挨拶ツイートログ出力
                self.createHelloTweetLog(response, self.hello_id_path)
            
            except tweepy.TweepyException as e:
                # エラーロギング
                Logger.logging.error(e.args)
                # 処理を停止
                sys.exit(1)
                
            except Exception as e:
                # エラーロギング
                Logger.logging.error(e)
                # 処理を停止
                sys.exit(1)

        else:
            # 処理を停止
            sys.exit(1)
        
    def getHelloTweetText(self):
        
        """
        挨拶文を取得する
        """
        
        return ''
    
    def getHelloTweetImage(self):
        
        """
        挨拶ツイートに含める画像を取得する
        """
        
        return ''
    
    def getAdjustInsertPointY(self, insertText, indentYPoint, txtHeight, maxIndentCount):
        
        """
        テキスト挿入位置調整

        Parameters
        ----------
        insertText : str
            挿入文字列
        indentYPoint : int
            1行あたり文字数
        txtHeight : int
            文字高さ
        maxIndentCount : int
            最大字下げ数
        """
        
        insertTextLen = len(insertText)
        if insertTextLen <= indentYPoint:
            adjInsertPointY = 0
        else:
            baseLength = indentYPoint * maxIndentCount
            indentCount = math.floor(baseLength / insertTextLen) if insertTextLen < baseLength else maxIndentCount
            adjInsertPointY = -1 * (txtHeight * (maxIndentCount - indentCount))
        
        return adjInsertPointY
    
    def uploadImage(self, tweetImageFilePath):
        
        """
        イメージファイルをアップロードする

        Parameters
        ----------
        tweetImageFilePath : str
            イメージファイルパス
        """
        
        # イメージファイルアップロード
        image_upl_inf = self.twitterApi.media_upload(filename=tweetImageFilePath)
        # media_id取得
        media_id = image_upl_inf.media_id

        # 戻り値を返す
        return media_id
    
    def tweet(self, tweetText, tweetImageFilePath:list = None):
        
        """
        ツイートする
        
        Parameters
        ----------
        tweetText : str
            ツイート文
        tweetImageFilePath : str
            ツイート画像ファイルパス
        """
        
        response = None
        try:
            # 挨拶ツイート
            if tweetImageFilePath == None: # テキストのみ
                response = self.twitterClient.create_tweet(text = tweetText)
            else: # 画像付き
                mediaIdList = []
                for filePath in tweetImageFilePath:
                    if os.path.exists(filePath):
                        media_id = self.uploadImage(filePath)
                        mediaIdList.append(media_id)
                if len(mediaIdList) > 0:
                    response = self.twitterClient.create_tweet(text = tweetText, media_ids=mediaIdList)
                else:
                    response = self.twitterClient.create_tweet(text = tweetText)
        except TwythonError as e:
            # エラーロギング
            Logger.logging.error(e.msg)
            # Falseを返す
            return response, False
        else:
            return response, True
        
    def getLogOutputPath(self, hello_id_dir, reply_log_dir):
        
        """
        ログ出力先を返す

        Parameters
        ----------
        hello_id_dir : str
            挨拶ツイートIDログ出力先
        reply_log_dir : str
            返信ツイートIDログ出力先
        """
        
        # ログ出力先
        hello_id_path = os.path.join(
            hello_id_dir, 
            self.parroterConfig.hello_id_filename)
        reply_log_path = os.path.join(
            reply_log_dir, 
            self.parroterConfig.reply_log_filename)
        
        # ログ出力先を返す
        return hello_id_path, reply_log_path
    
    def createLogOutputDir(self):
        
        """
        ログ出力先ディレクトリ作成
        """

        # ログ出力先ディレクトリ
        hello_id_dir = os.path.join(
            self.rootPath, 
            self.parroterConfig.hello_id_folder)
        reply_log_dir = os.path.join(
            self.rootPath, 
            self.parroterConfig.reply_log_folder)
        
        # ログ出力先ディレクトリを作成
        os.makedirs(hello_id_dir, exist_ok=True)
        os.makedirs(reply_log_dir, exist_ok=True)
        
        # 作成したディレクトリパスを返す
        return hello_id_dir, reply_log_dir

    def createHelloTweetLog(self, response, hello_id_path):
        
        """
        挨拶ツイートログ出力

        Parameters
        ----------
        response : any
            tweet-response
        hello_id_path : str
            挨拶ツイートIDログ出力先
        """
        
        # 挨拶ツイートログ出力
        with open(hello_id_path, mode='w') as f:
            f.write(str(response[0]['id'])+","+str(response[0]['text']))
    
    def getHelloTweetLog(self, hello_id_path):
        
        """
        挨拶ツイートログ取得

        Parameters
        ----------
        hello_id_path : str
            挨拶ツイートIDログ出力先
        """
        
        # 挨拶ツイートログ取得
        with open(hello_id_path, mode='r', encoding='utf-8') as f:
            return f.read().split('\n')
