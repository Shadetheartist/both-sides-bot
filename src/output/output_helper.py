
class OutputHelper(object):

    @staticmethod
    def quotify(text):
        quote = ''
        lines = text.split('\n')
        for line in lines:
            quote += '>' + line.strip() + '\n\n'

        return quote

    @staticmethod
    def get_nth(index):
        if(index < 20):
            return OutputHelper.nth[index + 1]
        else:
            return '#' + str(index + 1)

    nth = {
        1: "First",
        2: "Second",
        3: "Third",
        4: "Fourth",
        5: "Fifth",
        6: "Sixth",
        7: "Seventh",
        8: "Eighth",
        9: "Ninth",
        10: "Tenth",
        11: "Eleventh",
        12: "Twelfth",
        13: "Thirteenth",
        14: "Fourteenth",
        15: "Fifteenth",
        16: "Sixteenth",
        17: "Seventeenth",
        18: "Eighteenth",
        19: "Nineteenth",
        20: "Twentieth",
    }
