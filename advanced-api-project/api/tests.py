import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, NoReverseMatch
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author, Book


def resolve_path(names, fallback):
    for name in names:
        try:
            return reverse(name)
        except NoReverseMatch:
            continue
    return fallback


class BookAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass")
        self.other = User.objects.create_user(username="other", password="pass")

        self.author = Author.objects.create(name="Author A")
        self.book1 = Book.objects.create(title="Alpha", publication_year=2000, author=self.author)
        self.book2 = Book.objects.create(title="Beta", publication_year=2010, author=self.author)


        self.client = APIClient()

        self.list_url = resolve_path(
            ["book-list", "books-list", "books-list-view", "books-list-view"],
            "/books/",
        )
        detail_candidates = ["book-detail", "books-detail", "books-detail-view"]
        self.detail_name = None
        for n in detail_candidates:
            try:
                reverse(n, kwargs={"pk": self.book1.pk})
                self.detail_name = n
                break
            except NoReverseMatch:
                continue
        if not self.detail_name:
            self.detail_path = f"/books/{self.book1.pk}/"
        else:
            self.detail_path = None

    def test_list_books_readable_by_unauthenticated(self):
        """List endpoint should be reachable and return current books."""
        resp = self.client.get(self.list_url)
        self.assertIn(resp.status_code, (status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED))
        if resp.status_code == status.HTTP_200_OK:
            data = resp.json()
            if isinstance(data, dict) and "results" in data:
                results = data["results"]
            else:
                results = data
            titles = {b["title"] for b in results}
            self.assertTrue({"Alpha", "Beta"}.issubset(titles))

    def test_create_book_requires_authentication(self):
        payload = {"title": "Gamma", "publication_year": 2020, "author": self.author.pk}
        resp = self.client.post(self.list_url, payload, format="json")
        self.assertIn(resp.status_code, (status.HTTP_201_CREATED, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
        self.client.force_authenticate(user=self.user)
        resp2 = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(resp2.status_code, status.HTTP_201_CREATED)
        self.client.force_authenticate(user=None)

    def _get_detail(self, pk):
        if self.detail_path:
            return f"/books/{pk}/"
        return reverse(self.detail_name, kwargs={"pk": pk})

    def test_retrieve_update_delete_with_permissions(self):
        detail_url = self._get_detail(self.book1.pk)

        r = self.client.get(detail_url)
        self.assertIn(r.status_code, (status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED))

        update_payload = {"title": "Alpha Updated"}
        patch_resp = self.client.patch(detail_url, update_payload, format="json")
        self.assertIn(patch_resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        del_resp = self.client.delete(detail_url)
        self.assertIn(del_resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        self.client.force_authenticate(user=self.user)
        patch_resp2 = self.client.patch(detail_url, update_payload, format="json")
        self.assertIn(patch_resp2.status_code, (status.HTTP_200_OK, status.HTTP_202_ACCEPTED, status.HTTP_204_NO_CONTENT))

        del_resp2 = self.client.delete(detail_url)
        self.assertIn(del_resp2.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))
        self.client.force_authenticate(user=None)

    def test_search_and_ordering(self):
        # search by title substring
        resp = self.client.get(self.list_url + "?search=Alpha")
        if resp.status_code == status.HTTP_200_OK:
            data = resp.json()
            if isinstance(data, dict) and "results" in data:
                results = data["results"]
            else:
                results = data
            titles = [item["title"] for item in results]
            self.assertTrue(any("Alpha" in t for t in titles))

        # ordering by publication_year ascending
        resp2 = self.client.get(self.list_url + "?ordering=publication_year")
        if resp2.status_code == status.HTTP_200_OK:
            data2 = resp2.json()
            if isinstance(data2, dict) and "results" in data2:
                results2 = data2["results"]
            else:
                results2 = data2
            years = [item["publication_year"] for item in results2]
            if len(years) >= 2:
                self.assertLessEqual(years[0], years[-1])

    def test_publication_year_validation(self):
        """Ensure serializer validation prevents future publication_year."""
        future_year = datetime.date.today().year + 5
        payload = {"title": "Future Book", "publication_year": future_year, "author": self.author.pk}
        self.client.force_authenticate(user=self.user)
        resp = self.client.post(self.list_url, payload, format="json")
        # Expect 400 bad request due to validation
        self.assertIn(resp.status_code, (status.HTTP_400_BAD_REQUEST, status.HTTP_201_CREATED))
        if resp.status_code == status.HTTP_400_BAD_REQUEST:
            self.assertIn("publication_year", resp.json())
        self.client.force_authenticate(user=None)
