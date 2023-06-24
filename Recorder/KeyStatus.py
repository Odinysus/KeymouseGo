class KeyStatus:
    _keyStatus = {}

    def __int__(self):
        _keyStatus = {}

    def onKeyDown(self, key_code):
        if self._keyStatus.__contains__(key_code) is False or self._keyStatus[key_code] == 0:
            self._keyStatus[key_code] = 1
            return True
        else:
            return False

    def onKeyUp(self, key_code):
        self._keyStatus[key_code] = 0
        return True

    def reset(self):
        self._keyStatus = {}
