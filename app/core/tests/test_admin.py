from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from assertpy import assert_that
from rest_framework import status


class AdminSiteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="alex@qwerty.be", password="foobar", username="JeanSol"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="test@qwerty.be", password="foobar", username="Alex"
        )

    def test_users_listed(self):
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        assert_that(res.status_code).is_equal_to(status.HTTP_200_OK)

    def test_create_user_page(self):
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        assert_that(res.status_code).is_equal_to(status.HTTP_200_OK)
