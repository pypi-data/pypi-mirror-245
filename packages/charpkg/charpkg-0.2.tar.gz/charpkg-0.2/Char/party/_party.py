from typing import Optional as _Optional, List as _List, Tuple as _Tuple, Union as _Union
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from Char import *

_ETHICS_SCORES = {'lawful': 1, 'neutral': 0, 'chaotic': -1}
_MORALS_SCORES = {'good': 1, 'neutral': 0, 'evil': -1}
_ALIGNMENT_THRESHOLDS = {
    
}

class _AbstractParty(_ABC):
    _member_count: int
    _members: _List[actor.Charactor, ]
    _level: int
    _name: str
    _type: str
    _alignment: str
    _description: str
    _location: str
    _quests: _List
    _inventory: _List
    _gold: int
        
    @property
    def member_count(self) -> int:
        return self._member_count
    
    @property
    def members(self) -> _List[actor.Charactor, ]:
        return self._members
    
    @property
    def level(self) -> float:
        return self._level
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def type(self) -> str:
        return self._type
    
    @property
    def alignment(self) -> str:
        return self._alignment
    
    @property
    def description(self) -> str:
        return self._description

    @property
    def location(self) -> str:
        return self._location
    
    @property
    def quests(self) -> _List:
        return self._quests
    
    @property
    def inventory(self) -> _List:
        return self._inventory
    
    @property
    def gold(self) -> int:
        return self._gold
    
    @_abstractmethod
    def add_member(self, member: actor.Charactor) -> None:
        pass
    
    @_abstractmethod
    def remove_member(self, member: actor.Charactor) -> None:
        pass
    
    
class _BaseParty(_AbstractParty):
    def __init__(self, name: str = None):
        self._member_count = 0
        self._members = []
        self._level = 0
        self._name = name
        self._type = None
        self._alignment = None
        self._ethics = 0
        self._morals = 0
        self._description = None
        self._location = None
        self._quests = []
        self._inventory = []
        self._gold = 0
        
    def add_member(self, member: actor.Charactor) -> None:
        if member is not None and member in self._members:
            raise ValueError(f"{member} is already in the party.")
        if self.members == []:
            self._level = member.level
        elif member.level > self._level:
            self._level += ((member.level - self._level)/4) * (min(4, self._member_count + 1))
        self._gold += member.gold
        self._members.append(member)
        self._member_count += 1
            
    def remove_member(self, member: actor.Charactor) -> None:
        if member is not None and member not in self._members:
            raise ValueError(f"{member} is not in the party.")
        if self.members == []:
            raise ValueError("There are no members in the party.")
        if member.level > self._level:
            self._level -= ((member.level - self._level)/4) * (max(self._member_count - 1, 1))
        self._members.remove(member)
        self._member_count -= 1
        

class Party(_BaseParty):
    def __init__(self, name: str = None):
        super().__init__(name=name)
        
    def __repr__(self):
        return f"Party(name={self._name}, level={self._level}, count={self._member_count})"
    
    def __str__(self):
        return f"Party(name={self._name}, level={self._level}, count={self._member_count})"
        
    def __lt__(self, other):
        return self.level < other.level if isinstance(other, Party) else NotImplemented
        
    def __gt__(self, other):
        return self.level > other.level if isinstance(other, Party) else NotImplemented
        
    def __le__(self, other):
        return self.level <= other.level if isinstance(other, Party) else NotImplemented
        
    def __ge__(self, other):
        return self.level >= other.level if isinstance(other, Party) else NotImplemented
        
    def __hash__(self):
        return hash(self._name)
    
    def __len__(self):
        return len(self._members)
    
    def __getitem__(self, index):
        return self._members[index]
    
    def __setitem__(self, index, value):
        # TODO: Provide a way to alter different statuses of a member(i.e. health, turn, position, etc.)
        pass
        
    def __iter__(self):
        return iter(self._members)
    
    def __contains__(self, member_name: str):
        return member_name in [member.name for member in self._members]
    
    def __add__(self, other):
        if isinstance(other, Party):
            for member in other:
                self.add_member(member)
                other.remove_member(member)
            del other
            return self
        
    def __iadd__(self, new_member: actor.Charactor):
        if isinstance(new_member, actor.Charactor):
            self.add_member(new_member)
            return self