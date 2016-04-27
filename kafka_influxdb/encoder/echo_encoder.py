class Encoder(object):
    @staticmethod
    def encode(msg):
        """
        Don't change the message at all
        :param msg:
        """
        msg=str(msg, encoding = "utf-8")
        return msg
