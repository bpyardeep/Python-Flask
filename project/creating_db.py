# -*- coding: utf-8 -*-
"""
Created on Sun May 19 01:07:55 2019

@author: Pyardeep Birdi
"""

from project.models import db
db.create_all()


s = 'hello$world$this$is$best'
s = s.replace('$',',')
print(s)
