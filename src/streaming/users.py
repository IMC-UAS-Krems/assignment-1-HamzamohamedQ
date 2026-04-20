# This module defines the User class hierarchy, which represents different types of users (free, premium, family account) in the music streaming service.
from datetime import date
from typing import List, Sequence, Set, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .sessions import ListeningSession


class User:
    

    def __init__(self, user_id: str, name: str, age: int):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions: List["ListeningSession"] = []

    def add_session(self, session: "ListeningSession") -> None:
       
        self.sessions.append(session)

    def total_listening_seconds(self) -> int:
        
        return sum(s.duration_listened_seconds for s in self.sessions)

    def total_listening_minutes(self) -> float:
        
        return self.total_listening_seconds() / 60.0

    def unique_tracks_listened(self) -> Set[str]:
        
        return {s.track.track_id for s in self.sessions}


class FreeUser(User):
   

    def __init__(self, user_id: str, name: str, age: int, subscription_start: Optional[date] = None):
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start


class PremiumUser(User):
    

    MAX_SKIPS_PER_HOUR: int = 6

    def __init__(self, user_id: str, name: str, age: int, subscription_start: Optional[date] = None):
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start  # Accept but may not be used


class FamilyAccountUser(PremiumUser):
    

    def __init__(self, user_id: str, name: str, age: int, subscription_start: Optional[date] = None):
        super().__init__(user_id, name, age, subscription_start)
        self.sub_users: List["FamilyMember"] = []

    def add_sub_user(self, sub_user: "FamilyMember") -> None:
        
        self.sub_users.append(sub_user)

    def all_members(self) -> Sequence[User]:
       
        return [self] + self.sub_users


class FamilyMember(User):
    

    def __init__(self, user_id: str, name: str, age: int, parent: FamilyAccountUser):
        super().__init__(user_id, name, age)
        self.parent = parent