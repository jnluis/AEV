from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup, name="signup"),
    path("upload", views.upload, name="upload"),
    path("crop", views.crop, name="crop"),
    path("verification", views.forgotpass, name="verification"),
    path("maik", views.maik, name="maik"),
    path("mail_verification", views.signup_verification, name="signup_verification"),
    path("changepass", views.changepass, name="changepass"),
    path("verify_otp", views.verify_otp, name="verify_otp"),
    path("sendm", views.sendm, name="sendm"),
    path("chatsearch", views.searchchat, name="chatsearch"),
    path("getm/<str:rr>/", views.getm, name="getm"),
    path("chat", views.chat, name="chat"),
    path("deletepost", views.deletepost, name="deletepost"),
    path("followsme", views.followsme, name="followsme"),
    path("youfollows", views.youfollows, name="youfollows"),
    path("cover", views.cover, name="cover"),
    path("temp", views.tempp, name="temp"),
    path("search", views.search, name="search"),
    path("follow", views.follow, name="follow"),
    path("profile/<str:pk>", views.profile, name="profile"),
    path("chatroom/<str:pk>", views.chatroom, name="chatroom"),
    path("like_post", views.like_post, name="like_post"),
    path("signin", views.signin, name="signin"),
    path("signout", views.signout, name="signout"),
    path("psettings", views.psettings, name="psettings"),
    path("comment_post", views.comment_post, name="comment_post"),
    path("security", views.security, name="security"),
    path('tests', views.honeypot, name="honeypot_root"), # fake endpoint
    path('manual', views.honeypot, name="honeypot_manual_root"), #fake endpoint

]

# Fake endpoints and subendpoints
fake_endpoints = {
    'admin': ['login', 'dashboard', 'config', 'users'],
    'config': ['settings', 'database', 'env'],
    'backup': ['db', 'files', 'config'],
    'api': ['v1/users', 'v1/posts', 'v1/comments'],
    'wp-admin': ['login', 'admin-ajax.php', 'update'],
    'db': ['mysql', 'backup', 'config'],
    'uploads': ['images', 'videos', 'files'],
    'logs': ['error.log', 'access.log', 'database.log'],
}

# Create URL patterns for the fake endpoints
for main_endpoint in fake_endpoints.keys():
    urlpatterns += [
        path(f'tests/{main_endpoint}/', views.honeypot, name=f"honeypot_{main_endpoint}_root"), 
    ]
    # Define subpaths under each fake endpoint
    for subendpoint in fake_endpoints[main_endpoint]:
        urlpatterns += [
            path(f'tests/{main_endpoint}/{subendpoint}/', views.honeypot, name=f"honeypot_{main_endpoint}_{subendpoint}"),
        ]

manual_languages = ['en', 'es', 'fr', 'de', 'ru', 'zh', 'jp', 'pt','it', 'ko','ar', 'ro','sv','ca','cn','nl']
manual_subcategories = ['developer', 'faq', 'howto', 'misc', 'index.html', 'mod', 'programs', 'ssl', 'install', 'config', 'update']

# Create URL patterns for the /manual fake endpoint
for language in manual_languages:
    urlpatterns += [
        path(f'manual/{language}', views.honeypot, name=f"honeypot_manual_{language}_root"),
    ]
    for subcategory in manual_subcategories:
        urlpatterns += [
            path(f'manual/{language}/{subcategory}', views.honeypot, name=f"honeypot_manual_{language}_{subcategory}"),
        ]

if settings.ADMIN_ENABLED:
    urlpatterns += path("admin/", admin.site.urls)
