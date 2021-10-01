import unittest
from rest_framework import status
from rest_framework.test import APIClient


class TestModelApi(unittest.TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_register_detail(self):
        """
        TestCase for register user.
        Test will run successfully if user registered
        """
        response = self.client.post('/register/', {"username": "test", "email": "test@gmail.com",
                                                   "password": "qwerty"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login(self):
        """
        TestCase for login user.
        """
        response = self.client.post('/login/', {"username": "test",
                                                "password": "qwerty"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_csv(self):
        """
        TestCase for upload csv file and add employee in database.
        """
        myfile = open('employee/csv/employee_data.csv', 'r')
        response = self.client.post('/upload/', {'csv': myfile})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_employee_list(self):
        """ TestCase for getting all employee """
        response = self.client.get('/employee/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
