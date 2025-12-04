from django.db import models


# Author model with name field
class Author(models.Model):
    name = models.CharField(max_length=100)


# Book model with title, publication year, and foreign key to Author
class Book(models.Model):
    title = models.CharField(max_length=200)    
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.name
