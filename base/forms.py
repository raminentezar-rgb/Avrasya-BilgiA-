from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User, Resource, Quiz, Question


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'department', 'role', 'student_id']
        labels = {
            'name': 'Ad Soyad',
            'username': 'Kullanıcı Adı',
            'email': 'E-Posta Adresi',
            'department': 'Fakülte / Bölüm',
            'role': 'Akademik Rol',
            'student_id': 'Öğrenci / Sicil Numarası',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        role = self.data.get('role') or self.cleaned_data.get('role')
        if role == 'teacher' and email:
            if not email.lower().strip().endswith('@avrasya.edu.tr'):
                self.add_error('email', 'Akademisyen / Öğretim Üyesi kaydı için yalnızca resmi Avrasya Üniversitesi e-posta adresi (@avrasya.edu.tr) kullanılmalıdır!')
        return email

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role') or self.data.get('role')
        email = cleaned_data.get('email')
        if role == 'teacher' and email:
            if not email.lower().strip().endswith('@avrasya.edu.tr'):
                self.add_error('email', 'Akademisyen / Öğretim Üyesi kaydı için yalnızca resmi Avrasya Üniversitesi e-posta adresi (@avrasya.edu.tr) kullanılmalıdır!')
        return cleaned_data


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']
        labels = {
            'topic': 'Bölüm / Akademik Konu',
            'name': 'Çalışma Odası Adı',
            'course_code': 'Ders Kodu (örn: CENG201)',
            'room_type': 'Oda Türü',
            'description': 'Oda Açıklaması',
        }


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio', 'department', 'role', 'student_id', 'github_link', 'linkedin_link']
        labels = {
            'avatar': 'Profil Fotoğrafı (Avatar Seçimi)',
            'name': 'Ad Soyad',
            'username': 'Kullanıcı Adı',
            'email': 'E-Posta Adresi',
            'bio': 'Hakkımda (Biyografi)',
            'department': 'Fakülte / Bölüm',
            'role': 'Akademik Rol',
            'student_id': 'Öğrenci / Sicil Numarası',
            'github_link': 'GitHub Profili',
            'linkedin_link': 'LinkedIn Profili',
        }

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        email = cleaned_data.get('email')
        if role == 'teacher' and email:
            if not email.lower().strip().endswith('@avrasya.edu.tr'):
                self.add_error('email', 'Akademisyen / Öğretim Üyesi hesabı için yalnızca resmi Avrasya Üniversitesi e-posta adresi (@avrasya.edu.tr) kullanılmalıdır!')
        return cleaned_data


class ResourceForm(ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'file', 'link', 'description']
        labels = {
            'title': 'Kaynak Başlığı',
            'file': 'Dosya (PDF, ZIP, Resim vb.)',
            'link': 'Bağlantı (URL)',
            'description': 'Açıklama',
        }


class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'duration_minutes']
        labels = {
            'title': 'Sınav / Test Başlığı',
            'description': 'Sınav Açıklaması ve Kurallar',
            'duration_minutes': 'Sınav Süresi (Dakika)',
        }


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option']
        labels = {
            'text': 'Soru Metni',
            'option_a': 'A Seçeneği',
            'option_b': 'B Seçeneği',
            'option_c': 'C Seçeneği',
            'option_d': 'D Seçeneği',
            'correct_option': 'Doğru Cevap Seçeneği',
        }

