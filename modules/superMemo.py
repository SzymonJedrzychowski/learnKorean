import time


def superMemo(answer: int, word: dict):
    """Returns updatet parameters for the word that was repeated.

    :param answer: Correctness of answer: 1-correct, 0-incorrect,
    :param word: Word that was answered

    :return word: Updated word
    """

    if answer == 1:
        if word["currentStreak"] == 0:
            word["interval"] = 1

        elif word["currentStreak"] == 1:
            word["interval"] = 6

        else:
            word["interval"] = round(word["interval"]*word["easeFactor"], 2)

        word["easeFactor"] = round(word["easeFactor"]+0.05, 2)
        if word["easeFactor"] < 1.3:
            word["easeFactor"] = 1.3

        word["currentStreak"] += 1

    else:
        word["currentStreak"] = 0
        word["interval"] = 0
        word["easeFactor"] = max(0, round(word["easeFactor"]-0.3, 2))
    word["count"] += 1
    word["date"] = int(time.time()+word["interval"]*3600*24)
    word["localTime"] = time.localtime().tm_gmtoff

    return word
