from django.contrib.auth.models import User, AnonymousUser
from django.test import RequestFactory, TestCase
from rest_framework.views import APIView
from api.permissions import IsInvestor, IsAdmin
from api.models import UserProfile


class IsInvestorPermissionTests(TestCase):
    def setUp(self):
        self.permission = IsInvestor()
        self.view = APIView()
        self.factory = RequestFactory()
        self.user_investor = User.objects.create(username='investor')
        self.user_admin = User.objects.create(username='admin')
        UserProfile.objects.create(user=self.user_investor, user_type='investor')
        UserProfile.objects.create(user=self.user_admin, user_type='admin')

    def test_has_permission_investor(self):
        request = self.factory.get('/path/to/endpoint')
        request.user = self.user_investor
        has_permission = self.permission.has_permission(request, self.view)
        self.assertTrue(has_permission)

    def test_has_permission_admin(self):
        request = self.factory.get('/path/to/endpoint')
        request.user = self.user_admin
        has_permission = self.permission.has_permission(request, self.view)
        self.assertFalse(has_permission)

    def test_has_permission_anonymous(self):
        request = self.factory.get('/path/to/endpoint')
        request.user = AnonymousUser()
        has_permission = self.permission.has_permission(request, self.view)
        self.assertFalse(has_permission)


class IsAdminPermissionTests(TestCase):
    def setUp(self):
        self.permission = IsAdmin()
        self.view = APIView()
        self.factory = RequestFactory()
        self.user_investor = User.objects.create(username='investor')
        self.user_admin = User.objects.create(username='admin')
        UserProfile.objects.create(user=self.user_investor, user_type='investor')
        UserProfile.objects.create(user=self.user_admin, user_type='admin')

    def test_has_permission_admin(self):
        request = self.factory.get('/path/to/endpoint')
        request.user = self.user_admin
        has_permission = self.permission.has_permission(request, self.view)
        self.assertTrue(has_permission)

    def test_has_permission_investor(self):
        request = self.factory.get('/path/to/endpoint')
        request.user = self.user_investor
        has_permission = self.permission.has_permission(request, self.view)
        self.assertFalse(has_permission)

    def test_has_permission_anonymous(self):
        request = self.factory.get('/path/to/endpoint')
        request.user = AnonymousUser()
        has_permission = self.permission.has_permission(request, self.view)
        self.assertFalse(has_permission)
