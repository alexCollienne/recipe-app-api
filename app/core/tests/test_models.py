from assertpy import assert_that
from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTest(TestCase):
    def test_create_user_with_email_successful(self):
        email = "test@webcloud.be"
        password = "qwerty"
        user = get_user_model().objects.create_user(email=email, password=password)

        assert_that(user.email).is_equal_to(email)
        assert_that(user.check_password(password)).is_true()

    def test_new_user_email_normalized(self):
        email = "alex@gMAIL.COM"
        user = get_user_model().objects.create_user(email, "foobar")

        assert_that(email.lower()).is_equal_to(user.email)

    # def test_invalid_email(self):
    #     with self.assertRaises(ValueError):
    #         email = 'fssd!dfg.ne'
    #         user = get_user_model().objects.create_user(email, 'foobar')

    def test_no_email(self):
        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_user(None, "foobar")

    def test_create_superuser(self):

        user = get_user_model().objects.create_superuser("alex@gmail.com", "foobar")

        assert_that(user.is_superuser)
        assert_that(user.is_staff)
