# -*- coding: utf-8 -*-
'''
应用的配置
'''
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    #Flask-WTF配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    #Flask-Mail配置
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.qq.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
    MAIL_USE_TLS = False#os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '775242373@qq.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'bsrsrzsnhgbwbbeg'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = '775242373@qq.com'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or '775242373@qq.com'
    #SQLite数据库配置
    SQLALCHEMY_TRACK_MODIFICIATIONS = False
    
        
    @staticmethod
    def init_app(app):
        pass
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                            'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'
                        
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                            'sqlite:///' + os.path.join(basedir, 'data.sqlite')
                        
config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        
        'default': DevelopmentConfig
        }