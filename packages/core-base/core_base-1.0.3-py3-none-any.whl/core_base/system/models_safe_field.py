#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：sobase 
@File    ：models_safe_field.py
@Author  ：cx
@Date    ：2023/12/6 8:33 上午 
@Desc    ：数据加密脱敏显示
'''
from django.db import models
from core_base.utils.rsaUtil import rsaUtil

# 自动加解密
rsa_util_obj = rsaUtil()


# 手机
class EncrypyMobileField(models.TextField):
    def get_db_prep_value(self, value, connection, prepared=False):
        # 保存到数据库加密
        return rsa_util_obj.encrypt_by_public_key(value)

    def from_db_value(self, value, expression, connection):
        # 从数据库中读取解密
        if value:
            return rsa_util_obj.decrypt_by_private_key(value)
        # 加星号 ***
        return value
