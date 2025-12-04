from django.db import models

# Create Author model with a name field
class Author(models.Model):
    name = models.CharField(max_length=100)

# Create Book model with a ForeignKey relationship to Author
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()    
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.name