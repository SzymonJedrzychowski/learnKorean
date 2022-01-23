from playsound import playsound


class playControl:
    """Class used to control playing the sound"""

    def __init__(self):
        self.currentlyPlaying = False

    def playSound(self, file: str):
        """Play sound

        :param file: file location and name
        """

        if self.currentlyPlaying == False:
            self.currentlyPlaying = True
            playsound(file)
            self.currentlyPlaying = False
