import datetime
import uuid

from sqlalchemy import Column, Boolean, DateTime, String
from sqlalchemy.orm import relationship
from tethysext.atcore.models.types.guid import GUID
from tethysext.atcore.mixins import StatusMixin, AttributesMixin, UserLockMixin

from .app_user import AppUsersBase
from .associations import organization_resource_association

__all__ = ['Resource']


class Resource(StatusMixin, AttributesMixin, UserLockMixin, AppUsersBase):
    """
    Definition for the resources table.
    """
    __tablename__ = 'app_users_resources'

    # Resource Types
    TYPE = 'resource'
    DISPLAY_TYPE_SINGULAR = 'Resource'
    DISPLAY_TYPE_PLURAL = 'Resources'

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    name = Column(String)
    description = Column(String)
    type = Column(String)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(String)
    status = Column(String)
    public = Column(Boolean, default=False)
    _attributes = Column(String)
    _user_lock = Column(String)

    # Relationships
    organizations = relationship('Organization',
                                 secondary=organization_resource_association,
                                 back_populates='resources')

    # Polymorphism
    __mapper_args__ = {
        'polymorphic_identity': TYPE,
        'polymorphic_on': type
    }

    def __repr__(self):
        return f'<{self.__class__.__name__} name="{self.name}" id="{self.id}" locked={self.is_user_locked}>'
