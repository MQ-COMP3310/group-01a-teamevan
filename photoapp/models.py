#gpt5.5 assisted in the creation of this code

'''Photoapp Models'''

from django.db import models
from django.conf import settings

from taggit.managers import TaggableManager


class Photo(models.Model):

    #model ownership for object-level access control:
    #Every photo records WHO created it. This is the data that the access-control rules are builton. Without an owner recorded on the object, ownership cannot be enforced.
    #Referenced settings.AUTH_USER_MODEL instead of importing the User model directly. This keeps the foreign key correct even if the project later swaps in a custom user model which allows avoiding a latent dependency bug.
    #null=True / blank=True: photos created before this feature existed (the seed/fixture data) have no owner. The access-control logic treats an unowned photo as ADMIN-ONLY (fail-safe default): a regular user is never granted access to an object whose owner is unknown.
    #on_delete=models.CASCADE: when an account is deleted, the content it owns is deleted with it. This is a deliberate data-lifecycle decision recorded in the design spec, rather than leaving orphaned, unowned records behind.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='photos',
    )

    title = models.CharField(max_length=45)

    description = models.CharField(max_length=250)

    created = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(upload_to='photos/')

    tags = TaggableManager()

    def __str__(self):
        return self.title
