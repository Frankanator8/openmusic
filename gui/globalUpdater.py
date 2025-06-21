class GlobalUpdater:
    SONG_MENU =     0b100
    PLAYLIST_MENU = 0b010
    CENTER_MENU =   0b001
    def __init__(self):
        self.flag = 0
        self.playlist_uid = ""

    def update(self, flag):
        self.flag |= flag

    def check(self, flag):
        return (self.flag & flag) == flag

    def check_and_unset(self, flag):
        check = self.check(flag)
        self.flag &= ~flag
        return check

