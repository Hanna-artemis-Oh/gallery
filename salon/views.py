from django.shortcuts import render
# from .dalle import dalle
from .models import SampleKeyword
from . import music
from mypage.models import Member
from salon.models import ImageUploadModel, MusicUploadModel

import re
import nltk
from nltk.corpus import stopwords

# import MinDalle
# model = MinDalle(is_mega=True, is_reusable=True)


def index(request):
    return render(request, 'salon/index.html', {})


def home(request):
    keywords = ['가장 재미있는','추천이 많은', 'Best 작품', '회원님이 좋아할만한 작품',"Today's Favorite"]
    if SampleKeyword.objects.all():
        keywords = SampleKeyword.objects.all()
    
    return render(request, 'salon/home.html', {'keywords':keywords})


# 입력창
def start(request):
    return render(request, 'salon/start.html', {})

# 출력창
def result(request):
    text = ''
    if request.method == "POST":
        text = request.POST['title']
        # music_file = music.generateMusic()
    # 이미지 파일이 나온다.
    # img = model.generate_image(text, 7, 1) 이곳에 모델 연결
    img = 'img'
    img_file =  text + '.png'
    # img = Image.open('./media/a.png')
    # img.save('./media/' + img_file, 'png')

    # 텍스트 -> 태그화 리스트
    only_english = re.sub('[^a-zA-Z]', ' ', text)   # 영어만 남기기
    no_capitals = only_english.lower().split()      # 대문자 -> 소
    stops = set(stopwords.words('english'))         # 불용어 제거
    no_stops = [word for word in no_capitals if not word in stops]

    stemmer = nltk.stem.SnowballStemmer('english')  # 어간 추출
    tags = [stemmer.stem(word) for word in no_stops]



    context = {'text': text, 
                'img':img, 
                # "music_file":music_file, 
                "img_file":img_file,
                "tags":tags}

    return render(request, 'salon/result.html', context)


def save_result(request):
    if request.method == 'POST':
        # member_id = request.session.get('user') # request.POST.get("member_id")
        member_id = request.session['user'] # dict로 id 키값을 가져옴
        selected = request.POST.getlist("selected")
        print("=============================", member_id, selected)
        user = Member.objects.get(id=member_id) # id=member_id
        for filepath in selected:
            if 'mid' == filepath[-3:]:
                musicfile = MusicUploadModel(user=user, title="music", file=filepath)
                musicfile.save()
            else:
                imgfile = ImageUploadModel(user=user, description="photo", document=filepath)
                imgfile.save()
        return render(request, 'salon/save_result.html', {'files':selected})
    
    return render(request, 'salon/save_result.html', {})

