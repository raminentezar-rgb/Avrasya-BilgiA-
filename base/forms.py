from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User, Resource, Quiz, Question, QuestionBankItem


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
        fields = ['title', 'description', 'duration_minutes', 'start_time', 'end_time']
        labels = {
            'title': 'Sınav / Test Başlığı',
            'description': 'Sınav Açıklaması ve Kurallar',
            'duration_minutes': 'Sınav Süresi (Dakika)',
            'start_time': 'Başlangıç Tarihi ve Saati (İsteğe Bağlı)',
            'end_time': 'Bitiş Tarihi ve Saati (İsteğe Bağlı)',
        }
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_type', 'points', 'text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option']
        labels = {
            'question_type': 'Soru Tipi (Test veya Yazılı)',
            'points': 'Soru Puanı / Baram',
            'text': 'Soru Metni',
            'option_a': 'A Seçeneği (Sadece Test için)',
            'option_b': 'B Seçeneği (Sadece Test için)',
            'option_c': 'C Seçeneği (Sadece Test için)',
            'option_d': 'D Seçeneği (Sadece Test için)',
            'correct_option': 'Doğru Cevap Seçeneği (Sadece Test için)',
        }
        widgets = {
            'question_type': forms.Select(attrs={'style': 'width: 100%; padding: 10px 14px; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 0.95rem; background: #fff;'}),
            'points': forms.NumberInput(attrs={'style': 'width: 100%; padding: 10px 14px; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 0.95rem;'}),
            'text': forms.Textarea(attrs={'rows': 3, 'style': 'width: 100%; padding: 12px 14px; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 0.95rem;'}),
            'option_a': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px 14px; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 0.95rem;'}),
            'option_b': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px 14px; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 0.95rem;'}),
            'option_c': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px 14px; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 0.95rem;'}),
            'option_d': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px 14px; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 0.95rem;'}),
            'correct_option': forms.Select(attrs={'style': 'padding: 10px 18px; border-radius: 8px; border: 2px solid #ea580c; font-weight: bold; font-size: 0.95rem; background: #fff;'}),
        }


class QuestionBankItemForm(ModelForm):
    class Meta:
        model = QuestionBankItem
        fields = ['title', 'question_type', 'points', 'text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option']
        labels = {
            'title': 'Konu / Kategori Başlığı',
            'question_type': 'Soru Tipi',
            'points': 'Varsayılan Puan',
            'text': 'Soru Metni',
            'option_a': 'A Seçeneği',
            'option_b': 'B Seçeneği',
            'option_c': 'C Seçeneği',
            'option_d': 'D Seçeneği',
            'correct_option': 'Doğru Cevap',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Örn: Vize, 1. Ünite vb.', 'style': 'width: 100%; padding: 10px 14px; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 0.95rem;'}),
            'question_type': forms.Select(attrs={'style': 'width: 100%; padding: 10px 14px; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 0.95rem; background: #fff;'}),
            'points': forms.NumberInput(attrs={'style': 'width: 100%; padding: 10px 14px; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 0.95rem;'}),
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Soruyu buraya yazın...', 'style': 'width: 100%; padding: 12px 14px; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 0.95rem;'}),
            'option_a': forms.TextInput(attrs={'placeholder': 'A şıkkı', 'style': 'width: 100%; padding: 10px 14px; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 0.95rem;'}),
            'option_b': forms.TextInput(attrs={'placeholder': 'B şıkkı', 'style': 'width: 100%; padding: 10px 14px; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 0.95rem;'}),
            'option_c': forms.TextInput(attrs={'placeholder': 'C şıkkı', 'style': 'width: 100%; padding: 10px 14px; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 0.95rem;'}),
            'option_d': forms.TextInput(attrs={'placeholder': 'D şıkkı', 'style': 'width: 100%; padding: 10px 14px; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 0.95rem;'}),
            'correct_option': forms.Select(attrs={'style': 'padding: 10px 18px; border-radius: 8px; border: 2px solid #ea580c; font-weight: bold; font-size: 0.95rem; background: #fff;'}),
        }

