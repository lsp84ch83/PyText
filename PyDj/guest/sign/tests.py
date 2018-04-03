#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author  : Soner
@version :
@Time    : 2017/11/3/0003 15:11
@license : Copyright(C), Your Company
'''

from django.test import TestCase
from sign.models import Event,Guest
from django.contrib.auth.models import User

# Create your tests here.

class ModelTest(TestCase):

    def setUp(self):
        Event.objects.create(id = 1, name = 'oneplus 3 event', status = True, limit = 2000,
                             address = 'shenzhen', start_time = '2018-03-31 11:02:25')
        Guest.objects.create(id = 1, event_id = 1, realname = 'alen',
                             phone = '13711001101', email = 'alen@mail.com', sign = False)

    def test_event_models(self):
        result = Event.objects.get(name = 'oneplus 3 event')
        self.assertEqual(result.address, 'shenzhen')
        self.assertTrue(result.status)


    def test_guest_models(self):
        result = Guest.objects.get(phone = '13711001101')
        self.assertEqual(result.realname, 'alen')
        self.assertFalse(result.sign)

class IndexPageTest(TestCase):
    # 测试index 登录首页
    def test_index_page_renders_index_template(self):
        # 测试 index 视图
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

# 登录相关测试
class LoginActionTest(TestCase):
    # 测试登录动作
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')

    def test_add_admin(self):
        # 测试添加用户
        user = User.objects.get(username = 'admin')
        self.assertEqual(user.username, 'admin')
        self.assertEqual(user.email, 'admin@mail.com')

    def test_login_action_username_password_null(self):
        # 用户密码为空
        test_data = { 'username': '', 'password': '' }
        response = self.client.post('/login_action/', data = test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('账号或密码错误!', (response.content).decode('utf-8'))

    def test_login_action_username_password_error(self):
        # 用户名 密码错误
        test_data = { 'username': 'abc', 'password': '123' }
        response = self.client.post('/login_action/', data = test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('账号或密码错误!', (response.content).decode('utf-8'))

    def test_login_action_success(self):
        # 登录成功
        test_data = { 'username': 'admin', 'password': 'admin123456' }
        response = self.client.post('/login_action/', data = test_data)
        self.assertEqual(response.status_code, 302)

# 测试发布会管理
class EventMangeTest(TestCase):
    # 发布会管理
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(name = 'xiaomi5', limit = 2000, address = 'beijing',
                             status = 1, start_time = '2018-04-03 17:55:00')
        self.login_user = { 'username':'admin', 'password':'admin123456' }

    def test_event_mange_success(self):
        # 测试发布会：xiaomi5
        response = self.client.post('/login_action/', data = self.login_user)
        response = self.client.post('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'xiaomi5', response.content)
        self.assertIn(b'beijing', response.content)

    def test_event_mange_sreach_success(self):
        # 测试发布会搜索
        response = self.client.post('/login_action/', data = self.login_user)
        response = self.client.post('/search_name/', { 'name':'xiaomi5' })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'xiaomi5', response.content)
        self.assertIn(b'beijing', response.content)

# 测试嘉宾管理
class GuestManageTest(TestCase):
    # 嘉宾管理
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(id = 1, name = 'xiaomi5', limit = 2000, address = 'beijing',
                             status = 1, start_time = '2018-4-3 18:11:00')
        Guest.objects.create(realname = 'alen', phone = 18611001100, email = 'alen@mail.com',
                             sign = 0, event_id =1)
        self.login_user = { 'username':'admin', 'password':'admin123456' }

    def test_event_mange_success(self):
        # 测试嘉宾茜茜：alen
        response = self.client.post('/login_action/', data = self.login_user)
        response = self.client.post('/guest_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'alen', response.content)
        self.assertIn(b'18611001100', response.content)

    def test_guest_manage_sreach_success(self):
        # 测试嘉宾搜索
        response = self.client.post('login_action/', data = self.login_user)
        response = self.client.post('/search_phone/', { 'phone':'18611001100' })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'alen', response.content)
        self.assertIn(b'18611001100', response.content)

# 测试用户签到
class SignIndexActionTest(TestCase):
    # 初始化数据
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(id = 1, name = 'xiaomi5', limit = 2000, address = 'beijing',
                             status = 1, start_time = '2018-4-3 18:45:00')
        Event.objects.create(id=2, name='oneplus4', limit=2000, address='shenzhen',
                             status=1, start_time='2018-4-3 18:45:00')
        Guest.objects.create(realname = 'alen', phone = 18611001100, email = 'alen@mail.com',
                             sign = 0, event_id = 1)
        Guest.objects.create(realname='una', phone=18611001101, email='un@mail.com',
                             sign=1, event_id=2)
        self.login_user = { 'username':'admin', 'password':'admin123456' }

    def test_sign_index_action_phone_null(self):
        # 手机号为空
        response = self.client.post('/login_action/', data = self.login_user)
        response = self.client.post('/sign_index_action/1/', { 'phone':'' })
        self.assertEqual(response.status_code, 200)
        self.assertIn('手机号不存在', (response.content).deconde('utf-8'))
