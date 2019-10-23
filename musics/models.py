from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    
# Artist 와 1:N 구조 형성
# music.artist / artist.music_set -> related_name 사용
class Music(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='musics')
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


# music 과 1:N 구조 형성
class Comment(models.Model):
    music = models.ForeignKey(Music, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()

    def __str__(self):
        return f'{self.music.pk}번 음악의 {self.pk}번 댓글'
