import time

def superMemo(answer: int, word: dict):
    """Returns updatet parameters for the word that was repeated.
    
    :param answer: Correctness of answer: 1-correct, 0-incorrect,
    :param word: Word that was answered

    :return word: Updated word
    """

    if answer == 1:
        if word["n"] == 0:
            word["i"] = 1

        elif word["n"] == 1:
            word["i"] = 6

        else:
            word["i"] = round(word["i"]*word["ef"], 2)

        word["ef"] = round(word["ef"]+0.05, 2)
        if word["ef"] < 1.3:
            word["ef"] = 1.3

        word["n"] += 1

    else:
        word["n"] = 0
        word["i"] = 0
        word["ef"] = max(0, round(word["ef"]-0.3, 2))
    word["count"] += 1
    word["date"] = int(time.time()+word["i"]*3600*24)
    word["localTime"] = time.localtime().tm_gmtoff

    return word