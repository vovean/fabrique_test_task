from django.db import models

from polls.exceptions import EndDateBeforeStartException


class Poll(models.Model):
    title = models.CharField(max_length=60)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()

    class Meta:
        ordering = ('title', 'id')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.end_date < self.start_date:
            raise EndDateBeforeStartException
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f"Poll ({self.id}): \"{self.title}\""


class Question(models.Model):
    QUESTION_TYPES = (
        ('TEXT', 'Text question'),
        ('SO', 'Single-option questions'),
        ('MO', 'Multiple-option questions'),
    )
    text = models.TextField()
    question_type = models.TextField(choices=QUESTION_TYPES)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return f"{self.question_type} Question ({self.id}): {self.text[:15]}..."


class Answer(models.Model):
    user_id = models.PositiveIntegerField()
    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return f"Answer ({self.id}) to Question ({self.question.id}): {self.text[:15]}..."
