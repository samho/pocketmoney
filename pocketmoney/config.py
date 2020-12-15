import os

basedir = os.path.abspath(os.path.dirname(__file__))
TEMP_IMAGE_PATH = os.environ.get('POCKET_TEMP_IMAGE_PATH') or '%s/res' % basedir

BAIDU_API_KEY = os.environ.get('BAIDU_API_KEY') or 'testappkey'
BAIDU_SECRET_KEY = os.environ.get('BAIDU_SECRET_KEY') or 'testsecret'

TEMP_DOWNLOAD_PATH = os.environ.get('TEMP_DOWNLOAD_PATH') or '%s/download' % basedir

STOREX_DOWNLOAD_LIST = ("https://storex.cc/abq0rm3w7361/Network_Programming_with_Go.pdf",
                        "https://storex.cc/4w9m8cuzehpl/CentOS_7_Linux_Server_Cookbook_2nd_Edition.pdf",
                        "https://storex.cc/me89crp9rcbh/OReilly_Programming_Web_Services_with_SOAP.pdf",
                        "https://storex.cc/2dqc21mct43t/tmux_Taster.pdf",
                        "https://storex.cc/4quuz6ptrd4l/Learning_Docker.pdf",
                        "https://storex.cc/wv4jvih6ar5q/Apache_Kafka_Cookbook.pdf",
                        "https://storex.cc/gb5xaftptd2n/Vim-101-Hacks.pdf",
                        "https://storex.cc/magyfj8ehziu/Sed-and-Awk-101-Hacks-CN.pdf",
                        "https://storex.cc/tofvtucrdrkx/Linux-101-Hacks.pdf",
                        "https://storex.cc/acp2htn1sr25/The_Python_Standard_Library_by_Example.pdf")
