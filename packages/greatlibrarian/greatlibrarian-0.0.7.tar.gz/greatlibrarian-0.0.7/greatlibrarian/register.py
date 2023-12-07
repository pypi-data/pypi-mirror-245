from warnings import warn
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from greatlibrarian.Interactor import *
from greatlibrarian.FinalScore import *


class Test(unittest.TestCase):
    def __init__(self, llm, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.llm=llm

    def test_api_response(self, mock_post):
        # mock_post.return_value.status_code = 200
        # mock_post.return_value.text = "API Response Data"

        result = self.llm("你好")
        print(f'API_response result:{result}')
        if type(result) == str:
            return True
        else:
            return False

    # def test_api_failure(self, mock_post):
    #     mock_post.return_value.status_code = 500  
    #     mock_post.return_value.text = "API Error Message"

    #     result = self.llm("你好")
    #     print(f'API_wrong result:{result}')
    #     if result == 'API Problem':
    #         return True
    #     else:
    #         return False

class register():
    def __init__(self,conf):
        self.llm = conf.llm

    def checkllm(self):
        testobj = self.llm
        test = Test(testobj)
        mock_post = MagicMock()
        # api_failure = test.test_api_failure(mock_post)
        api_response = test.test_api_response(mock_post)

        if api_response:
            return True
        else:
             print('API response type is wrong')
             return False
        # if api_failure:
        #     print('API failure response is wrong')
