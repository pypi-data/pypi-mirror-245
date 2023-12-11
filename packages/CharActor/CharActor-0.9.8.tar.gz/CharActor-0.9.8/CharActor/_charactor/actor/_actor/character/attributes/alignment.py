from abc import ABC as _ABC
from typing import Optional as _Optional
import json as _json

from CharActor._charactor.dicts import load_dict

def _load_json(path):
    with open(path, 'r') as f:
        return _json.load(f)



ALIGNMENTS = load_dict('alignments')

ALIGNMENT_INSTANCES = {}

_ETHICS_SCORES = {'lawful': 1, 'neutral': 0, 'chaotic': -1}
_MORALS_SCORES = {'good': 1, 'neutral': 0, 'evil': -1}

class AbstractAlignment:
    _title: str
    _ethics: str
    _ethics_mod: int
    _morals: str
    _morals_mod: int
    _alignment_mod: int

    @property
    def title(self) -> str:
        return self._title
    
    @title.setter
    def title(self, title):
        self._title = title

    @property
    def ethics(self) -> str:
        return self._ethics
    
    @ethics.setter
    def ethics(self, ethics):
        self._ethics = ethics
        self._ethics_mod = _ETHICS_SCORES[ethics]
        
    @property
    def ethics_mod(self) -> int:
        return self._ethics_mod

    @property
    def morals(self) -> str:
        return self._morals
    
    @morals.setter
    def morals(self, morals):
        self._morals = morals
        self._morals_mod = _MORALS_SCORES[morals]

    @property
    def morals_mod(self) -> int:
        return self._morals_mod

    def __repr__(self):
        return self.title
    


class BaseAlignment(AbstractAlignment):
    def __init__(self, title):
        attrs = ALIGNMENTS[title]
        self.title = title.replace('_', ' ').title()
        self.ethics = attrs['ethics'].lower()
        self.morals = attrs['morals'].lower()
        
    def __json__(self):
        return {
            'title': self.title,
            'ethics': self.ethics,
            'morals': self.morals
        }

class AlignmentFactory:
    @staticmethod
    def create_alignment(title):
        alignment_instance = type(title.replace('_', ' ').title().replace(' ', ''), (BaseAlignment, ), {})(title)
        ALIGNMENT_INSTANCES[title.replace('_', ' ').title().replace(' ', '')] = alignment_instance
        globals().update(ALIGNMENT_INSTANCES)
        return globals()[title.title().replace('_', '')]