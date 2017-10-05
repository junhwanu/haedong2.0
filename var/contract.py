# -*- coding: utf-8 -*-

class contract():
    ì¢…ëª©ì½”ë“œ = ''
    ë§¤ë„?ˆ˜êµ¬ë¶„ = ''
    ?ˆ˜?Ÿ‰ = 0
    ì²´ê²°?‘œ?‹œê°?ê²? = 0
    ?µ? ˆê°? = [0]
    ?†? ˆê°? = [0]

    def __init__(self, params):
        if 'ì¢…ëª©ì½”ë“œ' in params: self.ì¢…ëª©ì½”ë“œ = params['ì¢…ëª©ì½”ë“œ']
        if 'ë§¤ë„?ˆ˜êµ¬ë¶„' in params: self.ë§¤ë„?ˆ˜êµ¬ë¶„ = params['ë§¤ë„?ˆ˜êµ¬ë¶„']
        if '?ˆ˜?Ÿ‰' in params: self.?ˆ˜?Ÿ‰ = params['?ˆ˜?Ÿ‰']
        if 'ì²´ê²°?‘œ?‹œê°?ê²?' in params: self.ì²´ê²°?‘œ?‹œê°?ê²? = params['ì²´ê²°?‘œ?‹œê°?ê²?']
        if '?µ? ˆê°?' in params: self.?µ? ˆê°? = params['?µ? ˆê°?']
        if '?†? ˆê°?' in params: self.?†? ˆê°? = params['?†? ˆê°?']