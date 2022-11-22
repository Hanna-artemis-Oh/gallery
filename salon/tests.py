from django.test import TestCase, Client
from django.contrib.auth.models import User
from salon.models import ArtUploadModel, KeywordModel, ArtKeywordModel
from salon.utils import uuid_name_upload_to
from googletrans import Translator
import os
from django.conf import settings


# Create your tests here.

class YourTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        print()
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        user = User.objects.create(username='testuser')
        user.set_password('1234')
        user.save()
        KeywordModel(word='tester').save()
        KeywordModel(word='testy').save()

    def setUp(self):
        print()
        print("==============setUp: Run once for every test method to setup clean data.")
        self.client = Client()
        self.client.login(username='testuser', password='1234')

    def tearDown(self):
        print("==============tearDown: Run once for every test method")
        self.client.logout()


    # def test_image_upload_model(self):
    #     user = User.objects.get(username='testuser')
    #     print(user)
    #     filepath = uuid_name_upload_to(None, filename="iamge_file.png")
    #     imgfile = ImageUploadModel(user=user, name="photo", filename=filepath)
    #     imgfile.save()
    #     print(imgfile)

    # def test_music_upload_model(self):
    #     user = User.objects.get(username='testuser')
    #     filepath = uuid_name_upload_to(None, filename="music_file.mid")
    #     muscifile = MusicUploadModel(user=user, name="music", filename=filepath)
    #     muscifile.save()
    #     print(muscifile)

    # def test_str_index(self):
    #     a = 'music_file.mid'
    #     print('---------', a[-3:])

    # def test_result_favorite(self):
    #     result_favorite = 1
    #     user = User.objects.get(username='testuser')
    #     favorite = MusicUploadModel(user = user, result_favorite=result_favorite)
    #     favorite.save()
    #     print(favorite, favorite.result_favorite )
    
    # def test_bulk_create_keyword(self):
    #     key_ins = KeywordModel.objects.bulk_create([
    #         KeywordModel(word='hello'),
    #         KeywordModel(word='world'),
    #         KeywordModel(word='you'),
    #         ]
    #     )

    #     key_all = KeywordModel.objects.all()
    #     print(len(key_ins), len(key_all))
    #     self.assertEquals(len(key_ins), len(key_all))

    # def test_image_keyword(self):
    #     user = User.objects.get(username='testuser')

    #     keywords = ['hello', 'world', 'you']

    #     keyword_models = [KeywordModel(word=key) for key in keywords]
    #     [k.save() for k in keyword_models]

    #     image = ImageUploadModel(user=user, name="photo", filename='test.png')
    #     image.save()

    #     ikms = [ImageKeywordModel(image=image, keyword=km) for km in keyword_models]
        
    #     ImageKeywordModel.objects.bulk_create(ikms)


    #     image_keywords = ImageKeywordModel.objects.all()
    #     print('----------->', len(image_keywords) )

    #     ###############################
    #     img = ImageUploadModel.objects.get(id=1)
    #     print('img id 1', img)
    #     imgkeys = ImageKeywordModel.objects.filter(image=img)
    #     print( imgkeys )

    #     ################################
    #     km = KeywordModel.objects.get(word='you')
    #     ikm = ImageKeywordModel.objects.filter(keyword=km)
    #     print(ikm[0].image.filename)
    #     print( [k.image.filename for k in ikm] )

    # def test_search(self):
    #     search_word = "test"
    #     search_token_list = search_word.split(' ')
    #     search_user_list=[]
    #     search_result_list=[]
    #     search_imagekeys_list=[ArtKeywordModel]
    #     for search_token in search_token_list:
    #         search_user_list.extend(User.objects.filter(username__contains=search_token))
    #         search_result_list.extend(KeywordModel.objects.filter(word__contains=search_token))
    #         search_imagekeys_list.extend(ArtKeywordModel.objects.filter(keyword__word__contains=search_token))
    #     del search_imagekeys_list[0]
    #     search_img_list = [imgkey.image for imgkey in search_imagekeys_list]
    #     search_img_set = set(search_img_list)
    #     context = {
    #         'search_user_list':search_user_list,
    #         'search_result_list':search_result_list, 
    #         'search_img_set':search_img_set,
    #     }
    #     print("====>", search_user_list, search_result_list, search_img_set)

    def test_translator(self):
        translator = Translator()
        print("****")
        prompt = "안녕하세요"

        which_lang = translator.detect("안녕하세요").lang
        print(which_lang)

        print("translate=>", translator.translate(text=prompt, dest='en', src='auto').text)
    
    def test_delete_art(self):
        user = User.objects.get(username='testuser')
        art = ArtUploadModel(kind=1, user=user, name='test', filename='test.png', input_text='test')
        art.save()
        keyword = KeywordModel.objects.get(word='tester')
        ak = ArtKeywordModel(keyword=keyword, art=art)
        ak.save()

        self.assertEqual('testuser 1 tester 1', f'{user} {art.id} {keyword} {ak.id}')

        # ArtKeywordModel.objects.filter(art=art).delete()
        art.delete()
        self.assertEqual('testuser None tester', f'{user} {art.id} {keyword}')

        # print( ArtKeywordModel.objects.all() )

    def test_del_storage(self):
        os.remove(os.path.join(settings.MEDIA_ROOT, 'images/banana.jpg'))
