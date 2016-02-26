from __future__ import unicode_literals

from django.db import models


class Player(models.Model):
    sciper = models.IntegerField(default=0, unique=True)
    name = models.TextField(max_length=200)
    contaminations = models.IntegerField(default=0)
    token_spent = models.IntegerField(default=0)
    zombie = models.BooleanField(default=False)
    revive_count = models.IntegerField(default=0)

    @classmethod
    def generate_sciper():
        exists = Player.objects().filter(sciper__lt=10000).count() < 0
        new = None
        if exists:
            greatest = Player.objects().filter(sciper__lt=10000)[0]
            new = greatest + 1
        else:
            new = 0
        return new

    @classmethod
    def create(name, sciper=None):
        if sciper is None:
            sciper = Player.generate_sciper()
        player = Player(sciper=sciper)
        player.save()

    def has_contaminated(self, other):
        if self.zombie:
            if not other.contaminate():
                return False
            self.contamination += 1
            self.save()
        return self.zombie

    def contaminate(self):
        if not self.zombie:
            self.zombie = True
            self.save()
        return not self.zombie

    def revive(self):
        if self.zombie:
            self.zombie = False
            self.revive_count += 1
            self.save()
        return self.zombie

    def spend_token(self, count):
        self.token_spent += count
        self.save()
        return self.token_spent

    class Meta:
        ordering = ('contaminations',)
