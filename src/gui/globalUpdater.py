# GlobalUpdater solves some of the cyclical references in the codebase before
# Meant to be checked by other classes to see if they need to update (hence the flags)
class GlobalUpdater:
    # Flags for updates
    SONG_MENU =     0b100
    PLAYLIST_MENU = 0b010
    CENTER_MENU =   0b001
    def __init__(self):
        self.flag = 0
        # Holds currently displayed large playlist
        self.playlist_uid = ""

    def update(self, flag):
        self.flag |= flag

    def check(self, flag):
        return (self.flag & flag) == flag

    def check_and_unset(self, flag):
        check = self.check(flag)
        self.flag &= ~flag
        return check

