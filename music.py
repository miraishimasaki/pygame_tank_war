from pygame import mixer


class Music():
    def __init__(self):
        self.filepath = 'music/bgm.wav' #需要mp3格式音乐播放
        mixer.init()
        mixer.music.load(self.filepath)

    def play_music(self):
        mixer.music.play(-1) #参数-1表示循环播放
    ''' mixer.music.play(start = 0.0)
        time.sleep(33)
        mixer.music.stop()                       如果这类代码放在主循环，会导致无画面             '''

    def _stop(self):
        mixer.music.stop()


