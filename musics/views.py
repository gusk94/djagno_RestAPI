from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Music, Artist, Comment
from .serializers import MusicSerializer, ArtistSerializer, CommentSerializer, ArtistDetailSerializer


@api_view(['GET'])
def music_list(request):
    # 만약에 artist_pk 가 Query Params 로 넘어온다면 artist_pk 로 필터링한 값만 응답
    params = {}
    artist_pk = request.GET.get('artist_pk')
    if artist_pk is not None:
        params['artist_id'] = artist_pk
    musics = Music.objects.filter(**params)
    serializer = MusicSerializer(musics, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def music_detail(request, music_pk):
    music = get_object_or_404(Music, pk=music_pk)
    if request.method == 'GET':
        serializer = MusicSerializer(music)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MusicSerializer(data=request.data, instance=music)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)
    else:
        music.delete()
        return Response({'message': 'music has been deleted'})


@api_view(['GET'])
def artists_list(request):
    artists = Artist.objects.all()
    serializer = ArtistSerializer(artists, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def artist_detail(request, artist_pk):
    artist = get_object_or_404(Artist, pk=artist_pk)
    serializer = ArtistDetailSerializer(artist)
    return Response(serializer.data)


@api_view(['GET'])
def comments_list(request):
    comments = Comment.objects.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CommentSerializer(data=request.data, instance=comment)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)
    else:
        comment.delete()
        return Response({'message': 'Comment has been deleted'})


@api_view(['POST'])
def comments_create(request, music_pk):
    print(request.data)
    serializer = CommentSerializer(data=request.data)
    # 검증에 실패하면 400 Bad Request Error 발생시킴
    if serializer.is_valid(raise_exception=True):
        serializer.save(music_id=music_pk)
    return Response(serializer.data)

