from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


DEPARTMENT_CHOICES = [
    ('Meslek Yüksekokulu (MYO)', (
        ('Adalet', 'Adalet'),
        ('Aşçılık', 'Aşçılık'),
        ('Bilgisayar Programcılığı', 'Bilgisayar Programcılığı'),
        ('Dış Ticaret', 'Dış Ticaret'),
        ('E-Ticaret ve Pazarlama', 'E-Ticaret ve Pazarlama'),
        ('Grafik Tasarımı', 'Grafik Tasarımı'),
        ('Halkla İlişkiler ve Tanıtım', 'Halkla İlişkiler ve Tanıtım'),
        ('Harita ve Kadastro', 'Harita ve Kadastro'),
        ('İç Mekan Tasarımı', 'İç Mekan Tasarımı'),
        ('İnşaat Teknolojisi', 'İnşaat Teknolojisi'),
        ('Lojistik', 'Lojistik'),
        ('Mimari Restorasyon', 'Mimari Restorasyon'),
        ('Mahkeme Büro Hizmetleri', 'Mahkeme Büro Hizmetleri'),
        ('Moda ve Tekstil Tasarımı', 'Moda ve Tekstil Tasarımı'),
        ('Otomotiv Teknolojisi', 'Otomotiv Teknolojisi'),
        ('Sivil Havacılık ve Kabin Hizmetleri', 'Sivil Havacılık ve Kabin Hizmetleri'),
        ('Sosyal Güvenlik', 'Sosyal Güvenlik'),
        ('Sosyal Hizmetler (MYO)', 'Sosyal Hizmetler'),
        ('Spor Yönetimi (MYO)', 'Spor Yönetimi'),
        ('Web Tasarım ve Kodlama', 'Web Tasarım ve Kodlama'),
        ('Bilişim Güvenliği Teknolojisi', 'Bilişim Güvenliği Teknolojisi'),
    )),
    ('Sağlık Hizmetleri Meslek Yüksekokulu (SHMYO)', (
        ('Acil Durum ve Afet Yönetimi', 'Acil Durum ve Afet Yönetimi'),
        ('Ağız ve Diş Sağlığı', 'Ağız ve Diş Sağlığı'),
        ('Ameliyathane Hizmetleri', 'Ameliyathane Hizmetleri'),
        ('Anestezi', 'Anestezi'),
        ('Diyaliz', 'Diyaliz'),
        ('Diş Protez Teknolojisi', 'Diş Protez Teknolojisi'),
        ('Elektronörofizyoloji', 'Elektronörofizyoloji'),
        ('Eczane Hizmetleri', 'Eczane Hizmetleri'),
        ('Fizyoterapi (SHMYO)', 'Fizyoterapi'),
        ('Çocuk Gelişimi Programı (SHMYO)', 'Çocuk Gelişimi Programı'),
        ('İlk ve Acil Yardım', 'İlk ve Acil Yardım'),
        ('İş Sağlığı ve Güvenliği', 'İş Sağlığı ve Güvenliği'),
        ('İş ve Uğraşı Terapisi', 'İş ve Uğraşı Terapisi'),
        ('Odyometri', 'Odyometri'),
        ('Optisyenlik', 'Optisyenlik'),
        ('Ortopedik Protez ve Ortez', 'Ortopedik Protez ve Ortez'),
        ('Patoloji Laboratuvar Teknikleri', 'Patoloji Laboratuvar Teknikleri'),
        ('Radyoterapi', 'Radyoterapi'),
        ('Sağlık Kurumları İşletmeciliği', 'Sağlık Kurumları İşletmeciliği'),
        ('Tıbbi Görüntüleme Teknikleri', 'Tıbbi Görüntüleme Teknikleri'),
        ('Tıbbi Laboratuvar Teknikleri', 'Tıbbi Laboratuvar Teknikleri'),
    )),
    ('Mühendislik ve Mimarlık Fakültesi', (
        ('Bilgisayar Mühendisliği', 'Bilgisayar Mühendisliği'),
        ('Elektrik-Elektronik Mühendisliği', 'Elektrik-Elektronik Mühendisliği'),
        ('Gıda Mühendisliği', 'Gıda Mühendisliği'),
        ('Harita Mühendisliği', 'Harita Mühendisliği'),
        ('İç Mimarlık', 'İç Mimarlık'),
        ('İnşaat Mühendisliği', 'İnşaat Mühendisliği'),
        ('Makine Mühendisliği', 'Makine Mühendisliği'),
        ('Mimarlık', 'Mimarlık'),
    )),
    ('Sağlık Bilimleri Fakültesi (SBF)', (
        ('Beslenme ve Diyetetik', 'Beslenme ve Diyetetik'),
        ('Çocuk Gelişimi (SBF)', 'Çocuk Gelişimi'),
        ('Ebelik', 'Ebelik'),
        ('Ergoterapi', 'Ergoterapi'),
        ('Fizyoterapi ve Rehabilitasyon', 'Fizyoterapi ve Rehabilitasyon'),
        ('Hemşirelik', 'Hemşirelik'),
        ('Odyoloji', 'Odyoloji'),
        ('Sağlık Yönetimi', 'Sağlık Yönetimi'),
        ('Sosyal Hizmet (SBF)', 'Sosyal Hizmet'),
    )),
    ('Spor Bilimleri Fakültesi', (
        ('Antrenörlük Eğitimi', 'Antrenörlük Eğitimi'),
        ('Egzersiz ve Spor Bilimleri', 'Egzersiz ve Spor Bilimleri'),
        ('Spor Yöneticiliği', 'Spor Yöneticiliği'),
        ('Rekreasyon', 'Rekreasyon'),
    )),
    ('İletişim Fakültesi', (
        ('Yeni Medya ve İletişim', 'Yeni Medya ve İletişim'),
        ('Görsel İletişim Tasarımı', 'Görsel İletişim Tasarımı'),
    )),
    ('Fen Edebiyat Fakültesi', (
        ('İngiliz Dili ve Edebiyatı', 'İngiliz Dili ve Edebiyatı'),
        ('Psikoloji', 'Psikoloji'),
        ('Türk Dili ve Edebiyatı', 'Türk Dili ve Edebiyatı'),
        ('Moleküler Biyoloji ve Genetik', 'Moleküler Biyoloji ve Genetik'),
        ('Mütercim Tercümanlık', 'Mütercim Tercümanlık'),
    )),
    ('İktisadi ve İdari Bilimler Fakültesi', (
        ('İşletme', 'İşletme'),
        ('İşletme (İngilizce)', 'İşletme (İngilizce)'),
        ('Siyaset Bilimi ve Kamu Yönetimi', 'Siyaset Bilimi ve Kamu Yönetimi'),
        ('Uluslararası İlişkiler', 'Uluslararası İlişkiler'),
        ('Maliye', 'Maliye'),
    )),
    ('Uygulamalı Bilimler Yüksekokulu', (
        ('Gastronomi ve Mutfak Sanatları', 'Gastronomi ve Mutfak Sanatları'),
        ('Yönetim Bilişim Sistemleri', 'Yönetim Bilişim Sistemleri'),
    )),
    ('Diğer / Genel', (
        ('Genel / Diğer', 'Genel / Diğer'),
    ))
]


ROLE_CHOICES = [
    ('student', 'Öğrenci / Student'),
    ('faculty', 'Akademisyen / Faculty Member'),
    ('ta', 'Asistan / Teaching Assistant'),
]

ROOM_TYPE_CHOICES = [
    ('course', 'Ders Odası / Course Room'),
    ('project', 'Proje & Çalışma Grubu / Project Group'),
    ('general', 'Genel Tartışma / General Discussion'),
]


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        if 'username' not in extra_fields or not extra_fields['username']:
            extra_fields['username'] = email.split('@')[0]
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if 'username' not in extra_fields or not extra_fields['username']:
            extra_fields['username'] = email.split('@')[0]

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True, verbose_name="Ad Soyad")
    email = models.EmailField(unique=True, null=True, verbose_name="E-Posta Adresi")
    bio = models.TextField(null=True, verbose_name="Hakkımda (Biyografi)")
    avatar = models.ImageField(null=True, default="avatar.svg", verbose_name="Profil Fotoğrafı (Avatar)")

    student_id = models.CharField(max_length=50, null=True, blank=True, verbose_name="Öğrenci / Sicil No")
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES, default='Genel / Diğer', verbose_name="Fakülte / Bölüm")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student', verbose_name="Akademik Rol")
    github_link = models.URLField(max_length=255, null=True, blank=True, verbose_name="GitHub Profili")
    linkedin_link = models.URLField(max_length=255, null=True, blank=True, verbose_name="LinkedIn Profili")

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, verbose_name="Bölüm / Akademik Konu")
    name = models.CharField(max_length=200, verbose_name="Çalışma Odası Adı")
    course_code = models.CharField(max_length=50, null=True, blank=True, verbose_name="Ders Kodu (örn: CENG201)")
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, default='general', verbose_name="Oda Türü")
    description = models.TextField(null=True, blank=True, verbose_name="Oda Açıklaması")
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]


class Resource(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200, verbose_name="Kaynak Başlığı")
    file = models.FileField(upload_to="resources/%Y/%m/", null=True, blank=True, verbose_name="Dosya (PDF, ZIP, Resim)")
    link = models.URLField(max_length=500, null=True, blank=True, verbose_name="Bağlantı (URL)")
    description = models.TextField(null=True, blank=True, verbose_name="Açıklama")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.title} ({self.room.name})"

    @property
    def extension(self):
        if self.file and self.file.name:
            return self.file.name.split('.')[-1].lower()
        return ''

    @property
    def is_audio(self):
        return self.extension in ['mp3', 'wav', 'ogg', 'webm', 'm4a']

    @property
    def is_video(self):
        return self.extension in ['mp4', 'mov', 'avi', 'mkv']

    @property
    def is_image(self):
        return self.extension in ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg']

    @property
    def is_pdf(self):
        return self.extension == 'pdf'

    @property
    def is_word(self):
        return self.extension in ['doc', 'docx']

    @property
    def is_excel(self):
        return self.extension in ['xls', 'xlsx', 'csv']

    @property
    def badge_color(self):
        if self.is_audio: return '#ec4899' # Pink
        if self.is_video: return '#8b5cf6' # Purple
        if self.is_pdf: return '#ef4444' # Red
        if self.is_word: return '#2563eb' # Blue
        if self.is_excel: return '#16a34a' # Green
        if self.is_image: return '#f59e0b' # Amber
        return '#64748b'


class Quiz(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='quizzes')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="Sınav / Test Başlığı")
    description = models.TextField(null=True, blank=True, verbose_name="Sınav Açıklaması ve Kurallar")
    duration_minutes = models.PositiveIntegerField(default=30, verbose_name="Süre (Dakika)")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Question(models.Model):
    OPTION_CHOICES = [
        ('A', 'A Seçeneği'),
        ('B', 'B Seçeneği'),
        ('C', 'C Seçeneği'),
        ('D', 'D Seçeneği'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(verbose_name="Soru Metni")
    option_a = models.CharField(max_length=300, verbose_name="A Seçeneği")
    option_b = models.CharField(max_length=300, verbose_name="B Seçeneği")
    option_c = models.CharField(max_length=300, verbose_name="C Seçeneği")
    option_d = models.CharField(max_length=300, verbose_name="D Seçeneği")
    correct_option = models.CharField(max_length=1, choices=OPTION_CHOICES, default='A', verbose_name="Doğru Cevap")

    def __str__(self):
        return self.text[:50]


class QuizSubmission(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(verbose_name="Puan")
    total_questions = models.IntegerField(verbose_name="Toplam Soru")
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        unique_together = ['quiz', 'student']

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title} ({self.score}/{self.total_questions})"

