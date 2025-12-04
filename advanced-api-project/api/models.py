from django.db import models

# Create Authors and Books models with a ForeignKey relationship
class Author(models.Model):
    name = models.CharField(max_length=100)


# Create Book model with ForeignKey to Author
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.name
