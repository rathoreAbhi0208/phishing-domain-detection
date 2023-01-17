from phishing.logger import logging
from phishing.exception import PhishingException
import os ,sys

# def test_logger_and_exception():
#     try:
#         logging.info("Starting the test_logger_and_exception")
#         result =3/0
#         print(result)
#         logging.info("Stopping test_logger_and_exception")
#     except Exception as e:

#         logging.debug(str(e))
#         raise PhishingException(e, sys)


if __name__ == "__main__":
    try:
        #test_logger_and_exception()
        pass
    except Exception as e:
        print(e)
