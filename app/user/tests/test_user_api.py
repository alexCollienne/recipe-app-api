from assertpy import assert_that
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("user:create-user")


class PublicUserApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def get_create_payload(self, **kwargs):
        return {
            "email": kwargs.get("email", "alex@webcloud.be"),
            "password": kwargs.get("email", "foobar"),
            "name": kwargs.get("email", "Alexandre Collienne"),
        }

    def test_create_valid_success(self):
        payload = self.get_create_payload()
        response = self.client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.get(**response.data)

        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)
        assert_that(user.check_password(payload["password"])).is_true()
        assert_that("password").is_not_in(response.data)

    def test_create_existing_user(self):
        payload = self.get_create_payload()
        self.client.post(CREATE_USER_URL, payload)
        response = self.client.post(CREATE_USER_URL, payload)

        assert_that(response.status_code).is_equal_to(status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        payload = self.get_create_payload(password="abc")
        response = self.client.post(CREATE_USER_URL, payload)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()

        assert_that(response.status_code).is_equal_to(status.HTTP_400_BAD_REQUEST)
        assert_that(user_exists).is_false()
