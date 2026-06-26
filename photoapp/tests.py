#GPT 5.5 assisted in the creation of this code

'''
  SR-1  Anonymous users may NOT create content (must authenticate first).
  SR-2  Anonymous users may NOT update or delete content.
  SR-3  A logged-in user MAY update/delete content they own.
  SR-4  A logged-in user may NOT update/delete content owned by someone else.
  SR-5  An administrator MAY update/delete ANY content.
  SR-6  Ownership of new content is taken from the session, not from client input.
  SR-7  Weak passwords are rejected at registration.

'''

import tempfile
from io import BytesIO

from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from PIL import Image

from .models import Photo

User = get_user_model()

#Write uploaded test images to a throwaway directory, not the real MEDIA_ROOT.
TEST_MEDIA_ROOT = tempfile.mkdtemp()

#A strong password reused across the test accounts so it passes the validators.
TEST_PASSWORD = 'Sup3r-Str0ng-pw!'


def make_image(name='test.jpg'):
    '''Return a genuinely valid 1x1 JPEG so the ImageField form validation
    (which uses Pillow) accepts it.'''
    buffer = BytesIO()
    Image.new('RGB', (1, 1)).save(buffer, format='JPEG')
    buffer.seek(0)
    return SimpleUploadedFile(name, buffer.read(), content_type='image/jpeg')


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class AccessControlTests(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password=TEST_PASSWORD)
        self.other = User.objects.create_user(username='other', password=TEST_PASSWORD)
        #An administrator is modelled as a staff user (is_staff=True).
        self.admin = User.objects.create_user(
            username='admin', password=TEST_PASSWORD, is_staff=True,
        )
        self.photo = Photo.objects.create(
            title='Owned photo',
            description='belongs to owner',
            image=make_image(),
            user=self.owner,
        )
        self.create_url = reverse('photo:create')
        self.update_url = reverse('photo:update', args=[self.photo.pk])
        self.delete_url = reverse('photo:delete', args=[self.photo.pk])

    #SR-1
    def test_anonymous_cannot_access_create(self):
        '''SR-1: an anonymous create attempt is redirected to the login page.'''
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    #SR-2
    def test_anonymous_cannot_access_update_or_delete(self):
        '''SR-2: anonymous update/delete attempts are redirected to login.'''
        for url in (self.update_url, self.delete_url):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn(reverse('login'), response.url)

    #Sr-3
    def test_owner_can_update_own_photo(self):
        '''SR-3: the owner can edit their own content.'''
        self.client.login(username='owner', password=TEST_PASSWORD)
        response = self.client.post(self.update_url, {
            'title': 'Edited title',
            'description': 'edited',
            'tags': 'sometag',
        })
        self.assertEqual(response.status_code, 302)  # success -> redirect
        self.photo.refresh_from_db()
        self.assertEqual(self.photo.title, 'Edited title')

    def test_owner_can_delete_own_photo(self):
        '''SR-3: the owner can delete their own content.'''
        self.client.login(username='owner', password=TEST_PASSWORD)
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Photo.objects.filter(pk=self.photo.pk).exists())

    #SR-4
    def test_non_owner_cannot_update(self):
        '''SR-4: a different logged-in user is forbidden (403) from editing,
        and the content is left unchanged.'''
        self.client.login(username='other', password=TEST_PASSWORD)
        response = self.client.post(self.update_url, {
            'title': 'Hijacked',
            'description': 'x',
            'tags': 'sometag',
        })
        self.assertEqual(response.status_code, 403)
        self.photo.refresh_from_db()
        self.assertEqual(self.photo.title, 'Owned photo')  # unchanged

    def test_non_owner_cannot_delete(self):
        '''SR-4: a different logged-in user is forbidden (403) from deleting,
        and the content still exists afterwards.'''
        self.client.login(username='other', password=TEST_PASSWORD)
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Photo.objects.filter(pk=self.photo.pk).exists())

    #SR-5
    def test_admin_can_update_any_photo(self):
        '''SR-5: an administrator can edit content they do not own.'''
        self.client.login(username='admin', password=TEST_PASSWORD)
        response = self.client.post(self.update_url, {
            'title': 'Admin edit',
            'description': 'by admin',
            'tags': 'sometag',
        })
        self.assertEqual(response.status_code, 302)
        self.photo.refresh_from_db()
        self.assertEqual(self.photo.title, 'Admin edit')

    def test_admin_can_delete_any_photo(self):
        '''SR-5: an administrator can delete content they do not own.'''
        self.client.login(username='admin', password=TEST_PASSWORD)
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Photo.objects.filter(pk=self.photo.pk).exists())

    #SR-6
    def test_created_photo_owned_by_session_user_not_form(self):
        '''SR-6: ownership is taken from the logged-in session. A forged 'user'
        field in the POST body is ignored, so a user cannot create content on
        behalf of someone else.'''
        self.client.login(username='owner', password=TEST_PASSWORD)
        response = self.client.post(self.create_url, {
            'title': 'New photo',
            'description': 'created in test',
            'image': make_image('new.jpg'),
            'tags': 'sometag',
            'user': self.other.pk,   # attacker attempts to set a different owner
        })
        self.assertEqual(response.status_code, 302)
        new_photo = Photo.objects.get(title='New photo')
        self.assertEqual(new_photo.user, self.owner)      # session user wins
        self.assertNotEqual(new_photo.user, self.other)   # forged value ignored


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class RegistrationSecurityTests(TestCase):

    #SR-7
    def test_weak_password_rejected_at_signup(self):
        '''SR-7: AUTH_PASSWORD_VALIDATORS reject a common password, so no
        account is created.'''
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'password',   # a well-known common password
            'password2': 'password',
        })
        # Form re-renders with errors (HTTP 200) and the user is NOT created.
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_strong_password_creates_account(self):
        '''SR-7 (positive case): a strong password is accepted and an account
        is created, confirming the validators are not over-blocking.'''
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': TEST_PASSWORD,
            'password2': TEST_PASSWORD,
        })
        self.assertEqual(response.status_code, 302)  # success -> redirect to login
        self.assertTrue(User.objects.filter(username='newuser').exists())
