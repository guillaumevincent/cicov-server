from os.path import dirname, join

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cicovapp.models import Product
from cicovapp.serializers import ProductSerializer
from cicovapp.views import (product_list, product_detail,
                            rfe_list, rfe_detail,
                            test_id_list, test_id_detail,
                            job_result_list, job_result_detail,
                            test_result_list, test_result_detail)


class SerializationTests(TestCase):
    def test_serialization(self):
        p = Product(name="OSP10", url="http://redhat.com/")
        p.save()
        s = ProductSerializer(p)
        self.assertEqual(len(s.data.keys()), 5, s.data)


class ApiTests(APITestCase):
    def setUp(self):
        self.p1 = {
            "name": "OSP10",
            "url": "http://redhat.com/",
        }
        self.create_url = reverse(product_list)
        self.list_url = self.create_url

    def create_product(self):
        response = self.client.post(self.create_url, self.p1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        return response

    def test_create_product(self):
        self.create_product()

    def test_create_product_inherited(self):
        response = self.create_product()
        self.p1['inherit'] = response.data['id']
        self.p1["product"] = "OSP11"
        response = self.create_product()
        self.assertNotEqual(response.data['id'], self.p1['inherit'])

    def test_list_products(self):
        self.create_product()
        response = self.client.get(self.list_url)
        self.assertEqual(len(response.data), 1)

    def test_product_detail(self):
        self.create_product()
        detail_url = reverse(product_detail, args=[1])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('name', response.data, response)
        self.assertEqual(response.data['name'], "OSP10")

    def test_create_rfe(self):
        self.create_product()
        response = self.client.post(reverse(rfe_list),
                                    {"name": "RFE 1",
                                     "product": 1,
                                     "url": "http://bz.com/1"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        response = self.client.get(reverse(rfe_detail, args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "RFE 1")

    def test_create_test_id(self):
        response = self.client.post(reverse(test_id_list),
                                    {"name": "TEST_ID 1",
                                     "url": "http://bz.com/1"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        response = self.client.get(reverse(test_id_detail, args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "TEST_ID 1")

    def test_create_job_result(self):
        response = self.create_product()
        response = self.client.post(reverse(job_result_list),
                                    {"product": response.data['id'],
                                     "build": "2018-06-20.1",
                                     "url": "http://jenkins.com/1"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        response = self.client.get(reverse(job_result_detail, args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['url'], "http://jenkins.com/1")

    def test_create_test_result(self):
        self.create_product()
        self.client.post(reverse(job_result_list),
                         {"product": 1,
                          "build": "2018-06-20.1",
                          "url": "http://jenkins.com/1"})
        self.client.post(reverse(test_id_list),
                         {"name": "TEST_ID 1",
                          "url": "http://bz.com/1"})
        response = self.client.post(reverse(test_result_list),
                                    {"job": 1,
                                     "test": 1,
                                     "result": True})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        response = self.client.get(reverse(test_result_detail, args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], True)

    def test_upload(self):
        xmlfile = open(join(dirname(__file__), 'tempest-results-full.1.xml'))
        self.create_product()
        response = self.client.post("/upload/",
                                    {"product": "OSP10",
                                     "url": "http://bz.com/1",
                                     "build": "2018-06-20.1",
                                     "file": xmlfile}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
