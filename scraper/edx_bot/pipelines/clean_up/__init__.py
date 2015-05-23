class Cleaner(object):

    @staticmethod
    def rm_whitespace(text):
        '''
        Removes leading and ending spaces, as well as
        duplicate spaces (as well as \n, \r...).

        http://stackoverflow.com/a/8270146/2708484
        '''
        return " ".join(text.split())
