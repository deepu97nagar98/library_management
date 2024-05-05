from django.shortcuts import render
from rest_framework.views import APIView
from .serializers   import BookSerializer, MemberSerializer, TransactionSerializer
from BookApp.models import Book, Member, Transaction
from rest_framework.response import Response
from rest_framework import status
from .helper import rent_on_book_return
import datetime
import requests

class GetAllBooks(APIView):
    def get(self, request):
        books_objects = Book.objects.all()
        book_data = BookSerializer(books_objects, many = True)
        return Response(data=response_data, status=status.HTTP_200_OK)


class AddBook(APIView):
    def post(self, request):
        book_request = BookSerializer(data = request.data)
        if book_request.is_valid():
            book_request.save()
            return Response({"message":"Success"},status=status.HTTP_201_CREATED)
        return Response(book_request.errors, status=status.HTTP_400_BAD_REQUEST)

class AddMember(APIView):
    def post(self, request):
        member_request = MemberSerializer(data = request.data)
        if member_request.is_valid():
            member_request.save()
            return Response({"message":"Success"},status=status.HTTP_201_CREATED)
        return Response(book_request.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueBook(APIView):
  def post(self, request):
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
      book = serializer.validated_data["book"]
      member = serializer.validated_data["member"]
      if book.quantity == 0:
        return Response({"error": "Book unavailable!"}, status=status.HTTP_400_BAD_REQUEST)
      elif member.outstanding_debt > 500:
        return Response({"error": "Member has outstanding dues exceeding Rs.500!"}, status=status.HTTP_400_BAD_REQUEST)
      serializer.save()
      book.quantity -= 1 # we subtracting 1 quantity from the total quantity of the book
      book.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReturnBook(APIView):
  def post(self, request, transaction_id):

    try:
      transaction = Transaction.objects.get(pk=transaction_id)
    except Transaction.DoesNotExist:
      return Response({"error": "Transaction not found!"}, status=status.HTTP_404_NOT_FOUND)
    # Implemented rent calculation logic here (based on return date and book daily rent)
    amount = rent_on_book_return(transaction)
    transaction.return_date = datetime.date.today()  # Replace with actual return date calculation
    transaction.save()
    member = transaction.member
    member.outstanding_debt += amount 
    member.save()
    serializer = TransactionSerializer(transaction)
    return Response(serializer.data, status=status.HTTP_200_OK)


class ImportBooks(APIView):
    def post(self, request):
        url = "https://gutendex.com/books/"

        search_query = request.data.get('search', '')
        page = request.data.get('page', 1)
        num_books = request.data.get('num_books', 32)

        params = {'page': page, 'search': search_query}

        response = requests.get(url, params=params)

        if response.status_code == 200:
            books_data = response.json()['results'][:num_books]

            # Iterate through books data and create book records
            for book_data in books_data:
                # Check if book already exists in the database based on title
                # quantity and fee on book can be reset from django admin page
                if not Book.objects.filter(title=book_data['title']).exists():
                    book_info = {'title': book_data['title'], 'author': book_data['authors'][0]['name']}
                    serializer = BookSerializer(data=book_info)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return Response({'error': 'Failed to create book record' + str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'Books imported successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Failed to fetch books from the API'}, status=status.HTTP_400_BAD_REQUEST)

# search book by title and author 
class SearchBooks(APIView):
    def get(self, request):
        title = request.GET.get('title', '')
        author = request.GET.get('author', '')

        books = Book.objects.all()

        if title:
            books = books.filter(title__icontains=title)
        
        if author:
            books = books.filter(author__icontains=author)

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


            