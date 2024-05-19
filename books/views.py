# books/views.py
import requests
import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from .models import Book, Like, Comment, UserPreference, BookRecommendation
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from .forms import RecommendedBookForm
from django.http import HttpResponse
from .models import Book
def index(request):
    return HttpResponse("Welcome to the Book Recommendation System")
# books/views.py

from django.http import JsonResponse
from .models import BookRecommendation

def delete_recommendation(request, recommendation_id):
    if request.method == 'DELETE':
        try:
            recommendation = BookRecommendation.objects.get(pk=recommendation_id)
            recommendation.delete()
            return JsonResponse({'status': 'success', 'message': 'Recommendation deleted successfully'})
        except BookRecommendation.DoesNotExist:
            return JsonResponse({'error': 'Recommendation not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
@require_POST
def submit_recommendation(request):
    data = json.loads(request.body)
    title = data.get('title', '')
    author = data.get('author', '')
    description = data.get('description', '')
    cover_image = data.get('cover_image', '')
    ratings = data.get('ratings', 0)
    genre = data.get('genre', '')

    recommendation = BookRecommendation.objects.create(
        title=title,
        author=author,
        description=description,
        cover_image=cover_image,
        ratings=ratings,
        genre=genre
    )
    return JsonResponse({'message': 'Recommendation saved successfully'})

def fetch_books(query):
    url = 'https://www.googleapis.com/books/v1/volumes'
    params = {'q': query}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('items', [])
    except requests.RequestException:
        return None

@require_GET
def search_books(request):
    query = request.GET.get('query')
    if not query:
        return JsonResponse({'error': 'Query parameter is required'}, status=400)

    books = fetch_books(query)
    if books is None:
        return JsonResponse({'error': 'Failed to fetch books from Google Books API'}, status=500)

    books_info = []
    for book in books:
        volume_info = book.get('volumeInfo', {})
        book_info = {
            'title': volume_info.get('title', ''),
            'authors': volume_info.get('authors', []),
            'description': volume_info.get('description', ''),
            'cover_image': volume_info.get('imageLinks', {}).get('thumbnail', ''),
            'ratings': volume_info.get('averageRating', 0)
        }
        books_info.append(book_info)

    return JsonResponse({'books': books_info})

@require_GET
def get_all_recommendations(request):
    recommendations = BookRecommendation.objects.all()
    serialized_recommendations = [model_to_dict(recommendation) for recommendation in recommendations]
    return JsonResponse({'recommendations': serialized_recommendations})

@require_GET
def get_recommendation_by_id(request, recommendation_id):
    try:
        recommendation = BookRecommendation.objects.get(pk=recommendation_id)
        serialized_recommendation = model_to_dict(recommendation)
        return JsonResponse(serialized_recommendation)
    except BookRecommendation.DoesNotExist:
        return JsonResponse({'error': 'Recommendation not found'}, status=404)

@require_GET
def filter_recommendations(request):
    genre = request.GET.get('genre')
    min_rating = request.GET.get('min_rating')
    max_rating = request.GET.get('max_rating')
    order_by = request.GET.get('order_by', 'ratings')

    recommendations = BookRecommendation.objects.all()

    if genre:
        recommendations = recommendations.filter(genre__iexact=genre)
    if min_rating:
        recommendations = recommendations.filter(ratings__gte=float(min_rating))
    if max_rating:
        recommendations = recommendations.filter(ratings__lte=float(max_rating))

    recommendations = recommendations.order_by(order_by)

    serialized_recommendations = [model_to_dict(recommendation) for recommendation in recommendations]
    return JsonResponse({'recommendations': serialized_recommendations})

@csrf_exempt
@require_POST
@login_required
def like_recommendation(request, recommendation_id):
    user = request.user
    try:
        recommendation = BookRecommendation.objects.get(pk=recommendation_id)
        Like.objects.get_or_create(user=user, book=recommendation)
        return JsonResponse({'status': 'success'})
    except BookRecommendation.DoesNotExist:
        return JsonResponse({'error': 'Recommendation not found'}, status=404)

@csrf_exempt
@require_POST
@login_required
def comment_recommendation(request, recommendation_id):
    user = request.user
    content = request.POST.get('content')
    if not content:
        return JsonResponse({'error': 'Content is required'}, status=400)
    try:
        recommendation = BookRecommendation.objects.get(pk=recommendation_id)
        Comment.objects.create(user=user, book=recommendation, content=content)
        return JsonResponse({'status': 'success'})
    except BookRecommendation.DoesNotExist:
        return JsonResponse({'error': 'Recommendation not found'}, status=404)

def search_results(request):
    return render(request, 'search_results.html')

def interactive(request):
    return render(request, 'interactive.html')

def search_suggestions(request):
    query = request.GET.get('query', '')
    suggestions = BookRecommendation.objects.filter(title__icontains=query).values_list('title', flat=True)[:10]
    return JsonResponse(list(suggestions), safe=False)

def dynamic_filter(request):
    genre = request.GET.get('genre')
    min_rating = request.GET.get('min_rating')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    filtered_books = BookRecommendation.objects.all()

    if genre:
        filtered_books = filtered_books.filter(genre=genre)
    if min_rating:
        filtered_books = filtered_books.filter(ratings__gte=min_rating)
    if start_date:
        filtered_books = filtered_books.filter(publication_date__gte=start_date)
    if end_date:
        filtered_books = filtered_books.filter(publication_date__lte=end_date)

    filtered_books_data = list(filtered_books.values())
    
    return JsonResponse(filtered_books_data, safe=False)

def personal_recommendations(request):
    if request.user.is_authenticated:
        preferences = UserPreference.objects.filter(user=request.user)
        recommendations = BookRecommendation.objects.filter(genre__in=preferences.values_list('favorite_genre', flat=True))
        return JsonResponse(list(recommendations.values()), safe=False)

@require_GET
def get_recommendations(request):
    recommendations = BookRecommendation.objects.all().values()
    return JsonResponse({'recommendations': list(recommendations)})
# views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def submit_book(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Process data here, for example, save to the database
            return JsonResponse({'status': 'success', 'message': 'Recommendation saved successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
def filter_books(request):
    try:
        genre = request.GET.get('genre')
        min_rating = float(request.GET.get('min_rating', 0))
        max_rating = float(request.GET.get('max_rating', 5))
        order_by = request.GET.get('order_by', 'ratings')

        if not genre:
            return HttpResponseBadRequest("Genre is required")

        books = Book.objects.filter(genre=genre, rating__gte=min_rating, rating__lte=max_rating).order_by(order_by)
        
        # Assuming you have a template named 'books/filter_results.html'
        return render(request, 'books/filter_results.html', {'books': books})
    except ValueError:
        return HttpResponseBadRequest("Invalid rating values")
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

def add_recommendation(request):
    if request.method == 'POST':
        form = RecommendedBookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Redirect to a success page
    else:
        form = RecommendedBookForm()
    return render(request, 'add_recommendation.html', {'form': form})
    # Start with all books
    filtered_books = Book.objects.all()

    # Apply filters
    if genre:
        filtered_books = filtered_books.filter(genre=genre)
    if min_rating:
        filtered_books = filtered_books.filter(ratings__gte=min_rating)
    if max_rating:
        filtered_books = filtered_books.filter(ratings__lte=max_rating)

    # Order the filtered books
    filtered_books = filtered_books.order_by('title')

    # Convert queryset to list of dictionariess
    filtered_books_data = list(filtered_books.values())

    # Return the filtered books as JSON response
    return JsonResponse({'books': filtered_books_data})
