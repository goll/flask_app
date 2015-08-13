#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import unittest
import json
import dr


class DrTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        dr.db = dr.client['test']
        dr.users = dr.db['users']

    @classmethod
    def tearDownClass(cls):
        dr.client.drop_database('test')

    def setUp(self):
        self.app = dr.app.test_client()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(404, response.status_code)

    def test_add(self):
        response = self.app.get('/add')
        self.assertEqual(405, response.status_code)

    def test_show(self):
        response = self.app.get('/show')
        self.assertEqual(400, response.status_code)

    def test_invalid_entry(self):
        data = 1
        response = self.app.post('/add', data=json.dumps(data))
        self.assertEqual(400, response.status_code)

    def test_all_entries_added(self):
        data = [
            {
                'uid': '1',
                'name': 'John Doe',
                'date': '2015-05-12T14:36:00.451765',
                'md5checksum': 'e8c83e232b64ce94fdd0e4539ad0d44f'
            },
            {
                'uid': '2',
                'name': 'Jane Doe',
                'date': '2015-05-13T14:36:00.451765',
                'md5checksum': '13065eda9a6ab62be1e63276cc7c46b0'
            },
            {
                'uid': '3',
                'name': 'Foo Bar',
                'date': '2015-05-15T14:36:00.451765',
                'md5checksum': '840df1f02ff506ac643349a2df6dc998'
            }
        ]
        return_data = {
            "message": "All entries added",
            "success": "true"
        }
        response = self.app.post('/add', data=json.dumps(data))
        self.assertEqual(200, response.status_code)
        self.assertEqual(return_data, json.loads(response.data))

    def test_no_entries_added_checksum_mismatch(self):
        data = [
            {
                'uid': '1',
                'name': 'John Doe',
                'date': '2015-05-12T14:36:00.451765',
                'md5checksum': 'e8c83e232b64ce94fdd0e4539ad0d441'
            },
            {
                'uid': '2',
                'name': 'Jane Doe',
                'date': '2015-05-13T14:36:00.451765',
                'md5checksum': '13065eda9a6ab62be1e63276cc7c46b1'
            }
        ]
        return_data = {
            "message": "No entries added (checksum mismatch or invalid format)",
            "success": "false"
        }
        response = self.app.post('/add', data=json.dumps(data))
        self.assertEqual(200, response.status_code)
        self.assertEqual(return_data, json.loads(response.data))

    def test_no_entries_added_uid_not_integer(self):
        data = [
            {
                'uid': 'foo',
                'name': 'John Doe',
                'date': '2015-05-12T14:36:00.451765',
                'md5checksum': 'a6a710631e468f3667a94700ef459a31'
            },
            {
                'uid': 'bar',
                'name': 'Jane Doe',
                'date': '2015-05-13T14:36:00.451765',
                'md5checksum': 'c7bced98fc3261ba018a1dd934dcc7e5'
            }
        ]
        return_data = {
            "message": "No entries added (checksum mismatch or invalid format)",
            "success": "false"
        }
        response = self.app.post('/add', data=json.dumps(data))
        self.assertEqual(200, response.status_code)
        self.assertEqual(return_data, json.loads(response.data))

    def test_no_entries_added_date_not_datetime(self):
        data = [
            {
                'uid': '1',
                'name': 'John Doe',
                'date': 'foo',
                'md5checksum': '6b76e62c30b85c6ca265d1c5f00ccf39'
            },
            {
                'uid': '2',
                'name': 'Jane Doe',
                'date': 'bar',
                'md5checksum': 'd20b018aae5a2a517dca0f541227f96e'
            }
        ]
        return_data = {
            "message": "No entries added (checksum mismatch or invalid format)",
            "success": "false"
        }
        response = self.app.post('/add', data=json.dumps(data))
        self.assertEqual(200, response.status_code)
        self.assertEqual(return_data, json.loads(response.data))

    def test_no_entries_added_missing_uid(self):
        data = [
            {
                'name': 'John Doe',
                'date': '2015-05-12T14:36:00.451765',
                'md5checksum': '0f1569a8702cafaee6140fdda2445a5f'
            },
            {
                'name': 'Jane Doe',
                'date': '2015-05-13T14:36:00.451765',
                'md5checksum': '4c732227cce0cd0c2ac109b709e4a9c9'
            }
        ]
        return_data = {
            "message": "No entries added (checksum mismatch or invalid format)",
            "success": "false"
        }
        response = self.app.post('/add', data=json.dumps(data))
        self.assertEqual(200, response.status_code)
        self.assertEqual(return_data, json.loads(response.data))

    def test_no_entries_added_missing_date(self):
        data = [
            {
                'uid': '1',
                'name': 'John Doe',
                'md5checksum': '92687cb2165259f108062f225b86f76f'
            },
            {
                'uid': '2',
                'name': 'Jane Doe',
                'md5checksum': '58dc105e1acc388189ec7508a64d6ca6'
            }
        ]
        return_data = {
            "message": "No entries added (checksum mismatch or invalid format)",
            "success": "false"
        }
        response = self.app.post('/add', data=json.dumps(data))
        self.assertEqual(200, response.status_code)
        self.assertEqual(return_data, json.loads(response.data))

    def test_some_entries_added_checksum_mismatch(self):
        data = [
            {
                'uid': '1',
                'name': 'John Doe',
                'date': '2015-05-12T14:36:00.451765',
                'md5checksum': 'e8c83e232b64ce94fdd0e4539ad0d44f'
            },
            {
                'uid': '2',
                'name': 'Jane Doe',
                'date': '2015-05-13T14:36:00.451765',
                'md5checksum': '13065eda9a6ab62be1e63276cc7c46b1'
            }
        ]
        return_data = {
            "message": "Only some entries added (checksum mismatch or invalid format)",
            "success": "true"
        }
        response = self.app.post('/add', data=json.dumps(data))
        self.assertEqual(200, response.status_code)
        self.assertEqual(return_data, json.loads(response.data))

    def test_some_entries_added_uid_not_integer(self):
        data = [
            {
                'uid': '1',
                'name': 'John Doe',
                'date': '2015-05-12T14:36:00.451765',
                'md5checksum': 'e8c83e232b64ce94fdd0e4539ad0d44f'
            },
            {
                'uid': 'bar',
                'name': 'Jane Doe',
                'date': '2015-05-13T14:36:00.451765',
                'md5checksum': 'c7bced98fc3261ba018a1dd934dcc7e5'
            }
        ]
        return_data = {
            "message": "Only some entries added (checksum mismatch or invalid format)",
            "success": "true"
        }
        response = self.app.post('/add', data=json.dumps(data))
        self.assertEqual(200, response.status_code)
        self.assertEqual(return_data, json.loads(response.data))

    def test_some_entries_added_date_not_datetime(self):
        data = [
            {
                'uid': '1',
                'name': 'John Doe',
                'date': '2015-05-12T14:36:00.451765',
                'md5checksum': 'e8c83e232b64ce94fdd0e4539ad0d44f'
            },
            {
                'uid': '2',
                'name': 'Jane Doe',
                'date': 'bar',
                'md5checksum': 'd20b018aae5a2a517dca0f541227f96e'
            }
        ]
        return_data = {
            "message": "Only some entries added (checksum mismatch or invalid format)",
            "success": "true"
        }
        response = self.app.post('/add', data=json.dumps(data))
        self.assertEqual(200, response.status_code)
        self.assertEqual(return_data, json.loads(response.data))

    def test_some_entries_added_missing_uid(self):
        data = [
            {
                'uid': '1',
                'name': 'John Doe',
                'date': '2015-05-12T14:36:00.451765',
                'md5checksum': 'e8c83e232b64ce94fdd0e4539ad0d44f'
            },
            {
                'name': 'Jane Doe',
                'date': '2015-05-13T14:36:00.451765',
                'md5checksum': '4c732227cce0cd0c2ac109b709e4a9c9'
            }
        ]
        return_data = {
            "message": "Only some entries added (checksum mismatch or invalid format)",
            "success": "true"
        }
        response = self.app.post('/add', data=json.dumps(data))
        self.assertEqual(200, response.status_code)
        self.assertEqual(return_data, json.loads(response.data))

    def test_some_entries_added_missing_date(self):
        data = [
            {
                'uid': '1',
                'name': 'John Doe',
                'date': '2015-05-12T14:36:00.451765',
                'md5checksum': 'e8c83e232b64ce94fdd0e4539ad0d44f'
            },
            {
                'uid': '2',
                'name': 'Jane Doe',
                'md5checksum': '58dc105e1acc388189ec7508a64d6ca6'
            }
        ]
        return_data = {
            "message": "Only some entries added (checksum mismatch or invalid format)",
            "success": "true"
        }
        response = self.app.post('/add', data=json.dumps(data))
        self.assertEqual(200, response.status_code)
        self.assertEqual(return_data, json.loads(response.data))

    def test_show_entries(self):
        return_data = {
            "date": "2015-05-15",
            "occurrences": 1,
            "success": "true",
            "uid": 3
        }
        response = self.app.get('/show?uid=3&date=2015-05-15')
        self.assertEqual(200, response.status_code)
        self.assertEqual(return_data, json.loads(response.data))

    def test_show_entries_missing_uid(self):
        return_data = {
            "message": "Invalid parameters",
            "success": "false"
        }
        response = self.app.get('/show?date=2015-05-15')
        self.assertEqual(400, response.status_code)
        self.assertEqual(return_data, json.loads(response.data))

    def test_show_entries_missing_date(self):
        return_data = {
            "message": "Invalid parameters",
            "success": "false"
        }
        response = self.app.get('/show?uid=3')
        self.assertEqual(400, response.status_code)
        self.assertEqual(return_data, json.loads(response.data))

    def test_show_entries_uid_not_integer(self):
        return_data = {
            "message": "Invalid parameters",
            "success": "false"
        }
        response = self.app.get('/show?uid=foo&date=2015-05-15')
        self.assertEqual(400, response.status_code)
        self.assertEqual(return_data, json.loads(response.data))

    def test_show_entries_date_not_datetime(self):
        return_data = {
            "message": "Invalid parameters",
            "success": "false"
        }
        response = self.app.get('/show?uid=3&date=bar')
        self.assertEqual(400, response.status_code)
        self.assertEqual(return_data, json.loads(response.data))

    def test_show_entries_invalid_parameters(self):
        return_data = {
            "message": "Invalid parameters",
            "success": "false"
        }
        response = self.app.get('/show?uid=foo&date=bar')
        self.assertEqual(400, response.status_code)
        self.assertEqual(return_data, json.loads(response.data))

    def test_show_entries_empty_parameters(self):
        return_data = {
            "message": "Invalid parameters",
            "success": "false"
        }
        response = self.app.get('/show?uid=&date=')
        self.assertEqual(400, response.status_code)
        self.assertEqual(return_data, json.loads(response.data))

    def test_show_entries_empty_uid(self):
        return_data = {
            "message": "Invalid parameters",
            "success": "false"
        }
        response = self.app.get('/show?uid=&date=2015-05-15')
        self.assertEqual(400, response.status_code)
        self.assertEqual(return_data, json.loads(response.data))

    def test_show_entries_empty_date(self):
        return_data = {
            "message": "Invalid parameters",
            "success": "false"
        }
        response = self.app.get('/show?uid=3&date=')
        self.assertEqual(400, response.status_code)
        self.assertEqual(return_data, json.loads(response.data))

if __name__ == '__main__':
    unittest.main()
