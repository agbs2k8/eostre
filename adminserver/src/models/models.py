import secrets
import datetime
from collections import defaultdict
import sqlalchemy as sa 
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from src.db import Base, role_permission_table
import config as cfg
# TODO: Restore the tags object


class Account(Base):
    __tablename__ = 'account'
    id: Mapped[int] = mapped_column(sa.Integer, sa.Identity(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(255), nullable=False, unique=True)
    display_name: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    active: Mapped[bool] = mapped_column(default=True)
    created_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(tz=datetime.timezone.utc))
    modified_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(tz=datetime.timezone.utc))
    deleted: Mapped[bool] = mapped_column(default=False)
    grants: Mapped[list['Grant']] = relationship('Grant', back_populates='account', foreign_keys='Grant.account_id')

    def __repr__(self):
        return f"Account(id={self.id!r}, name={self.name!r})"
    
    def __hash__(self):
        return hash(self.id)
    
    async def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "display_name": self.display_name,
            "active": self.active,
            "created_date": self.created_date.isoformat(),
            "modified_date": self.modified_date.isoformat()
        }
    
    @staticmethod
    async def get(account_id, db_session):
        result = await db_session.execute(sa.select(Account).where(Account.id == account_id))
        return result.scalars().first()


class Permission(Base):
    __tablename__ = 'permission'
    id: Mapped[int] = mapped_column(sa.Integer, sa.Identity(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(255), nullable=False, unique=True)
    display_name: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    active: Mapped[bool] = mapped_column(default=True)
    created_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(tz=datetime.timezone.utc))
    modified_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(tz=datetime.timezone.utc))
    deleted: Mapped[bool] = mapped_column(default=False)
    # scope = Create, Read, Update or Delete
    scope: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    roles: Mapped[list["Role"]] = relationship(secondary=role_permission_table, back_populates='permissions')

    def __repr__(self):
        return f"Permission(id={self.id!r}, name={self.name!r})"
    
    async def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "display_name": self.display_name,
            "active": self.active,
            "created_date": self.created_date.isoformat(),
            "modified_date": self.modified_date.isoformat(),
            "scope": self.scope
        }


class Role(Base):
    __tablename__ = 'role'
    id: Mapped[int] = mapped_column(sa.Integer, sa.Identity(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(255), nullable=False, unique=True)
    display_name: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    active: Mapped[bool] = mapped_column(default=True)
    created_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(tz=datetime.timezone.utc))
    modified_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(tz=datetime.timezone.utc))
    deleted: Mapped[bool] = mapped_column(default=False)
    permissions: Mapped[list[Permission]] = relationship(secondary=role_permission_table, 
                                                         back_populates='roles',
                                                         lazy='selectin')

    def __repr__(self):
        return f"Role(id={self.id!r}, name={self.name!r})"
    
    async def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "display_name": self.display_name,
            "active": self.active,
            "created_date": self.created_date.isoformat(),
            "modified_date": self.modified_date.isoformat(),
            "permissions": [permission.name for permission in self.permissions]
        }
    
    @staticmethod
    async def get(role_id, db_session):
        result = await db_session.execute(sa.select(Role).where(Role.id == role_id))
        return result.scalars().first()


class Email(Base):
    __tablename__ = 'email'
    id: Mapped[int] = mapped_column(sa.Integer, sa.Identity(), primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(sa.String(255), nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))
    primary: Mapped[bool] = mapped_column(default=False)
    active: Mapped[bool] = mapped_column(default=True)
    created_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(tz=datetime.timezone.utc))
    deleted: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f"Email(id={self.id!r}, email={self.email!r})"
    
    def __str__(self) -> str:
        return str(self.email   )


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(sa.Integer, sa.Identity(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(255), nullable=False, unique=True)
    type: Mapped[str] = mapped_column(sa.String(50), nullable=False, default="user")  # user vs service
    email: Mapped[Email] = relationship('Email', lazy='selectin')
    alternate_emails: Mapped[list["Email"]] = relationship('Email')
    personal_name: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    family_names: Mapped[list[str]] = mapped_column(sa.String(255), nullable=True)
    display_name: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    active: Mapped[bool] = mapped_column(default=True)
    created_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(tz=datetime.timezone.utc))
    modified_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(tz=datetime.timezone.utc))
    password: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    grants: Mapped[list['Grant']] = relationship('Grant', 
                                                 back_populates='user', 
                                                 foreign_keys='Grant.user_id', 
                                                 lazy='selectin')
    deleted: Mapped[bool] = mapped_column(default=False)

    def __init__(self, name: str, password: str, email: str, 
                 type: str = "user", 
                 display_name = None, 
                 personal_name = None,
                 family_names = None):
        self.name = name
        self.type = type
        self.email = Email(email=email, primary=True)
        self.alternate_emails = []
        self.personal_name = personal_name
        self.family_names = [x.strip() for x in family_names.split(',')] if family_names else None
        self.display_name = display_name
        self.active = True
        self.created_date = datetime.datetime.now(tz=datetime.timezone.utc)
        self.modified_date = datetime.datetime.now(tz=datetime.timezone.utc)
        self.password = generate_password_hash(password)
        self.deleted = False

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r})"
    
    def __hash__(self):
        return hash(self.id)
    
    def check_password(self, password: str) -> bool:
        """
        Check if the provided password matches the stored hashed password.
        :param password: The password to check.
        :return: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password, password)
    
    async def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "display_name": self.display_name,
            "active": self.active,
            "created_date": self.created_date.isoformat(),
            "modified_date": self.modified_date.isoformat(),
            "email": self.email.email if self.email else None#,
            #"accounts": [account.name for account in self.accounts],
            #"grants": [await grant.to_dict() for grant in self.grants]
        }

    @staticmethod
    async def find(name: str, db_session):
        """
        Find a user by name.
        :param name: The name of the user to find.
        :return: User object or None if not found.
        """
        result = await db_session.execute(sa.select(User).where(User.name == name))
        return result.scalars().first()

    @staticmethod
    async def username_login(name: str, password: str, db_session):
        """
        Log in a user by checking their name and password.
        :param name: The name of the user.
        :param password: The password to check.
        :param db_session: The database session to use for the query.
        :return: User object if login is successful, None otherwise.
        """
        
        user = await User.find(name, db_session)
        if user and user.check_password(password):
            return user
        return None

    @staticmethod 
    async def email_login(email: str, password: str, db_session):
        """
        Log in a user by checking their email and password.
        :param email: The email of the user.
        :param password: The password to check.
        :param db_session: The database session to use for the query.
        :return: User object if login is successful, None otherwise.
        """
        result = await db_session.execute(sa.select(User).join(Email).where(Email.email == email))
        user = result.scalars().first()
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    async def get(user_id, db_session):
        """
        Get a user by ID.
        :param user_id: The ID of the user to get.
        :return: User object or None if not found.
        """
        result = await db_session.execute(sa.select(User).where(User.id == user_id))
        return result.scalars().first()
    
    async def get_grants(self, db_session):
        """
        Get all grants for the user.
        :param db_session: The database session to use for the query.
        :return: List of Grant objects associated with the user.
        """
        result = await db_session.execute(sa.select(Grant).where(Grant.user_id == self.id, Grant.active == True))
        return result.scalars().all()
    
    async def get_permissions(self, db_session):
        """
        Get all permissions for the user.
        :param db_session: The database session to use for the query.
        :return: List of Permission objects associated with the user.
        """
        grants = await self.get_grants(db_session)
        result = defaultdict(set)
        for grant in grants:
            if grant.active and grant.account_id and grant.role:
                for perm in grant.role.permissions:
                    result[grant.account_id].add(perm.name)

        return {account_id: sorted(list(perms)) for account_id, perms in result.items()}

    async def get_authorized_accounts(self, db_session):
        """
        Get all accounts the user is authorized to access.
        :param db_session: The database session to use for the query.
        :return: List of Account objects the user is authorized to access.
        """
        grants = await self.get_grants(db_session)
        result = []
        for grant in grants:
            result.append(grant.account)
        return list(set(result))

    async def grant_role(self, role_id: str, account_id: str, db_session):
        role = await db_session.get(Role, role_id)
        account = await db_session.get(Account, account_id)
        grant = Grant(user=self, role=role, account=account)
        db_session.add(grant)
        await db_session.commit()
        return grant


class Grant(Base):
    __tablename__ = 'grant'
    id: Mapped[int] = mapped_column(sa.Integer, sa.Identity(), primary_key=True)
    active: Mapped[bool] = mapped_column(default=True)
    granted_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(tz=datetime.timezone.utc))
    role_id: Mapped[int] = mapped_column(sa.ForeignKey("role.id"))
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))
    user: Mapped[User] = relationship('User', back_populates='grants', foreign_keys=[user_id])
    account_id: Mapped[int] = mapped_column(sa.ForeignKey("account.id"), nullable=True)
    account: Mapped[Account] = relationship('Account', 
                                            back_populates='grants', 
                                            foreign_keys=[account_id],
                                            lazy='selectin')
    role: Mapped[Role] = relationship('Role', lazy='selectin')
    revoked_date: Mapped[datetime.datetime] = mapped_column(
        nullable=True)

    def __repr__(self):
        return f"Grant(id={self.id!r}, user_id={self.user.id!r})"
    
    async def to_dict(self):
        return {
            "id": self.id,
            "active": self.active,
            "granted_date": self.granted_date.isoformat(),
            "role_id": self.role_id,
            "role_name": self.role.name,
            "user_id": self.user_id,
            "account_id": self.account_id,
            "account_name": self.account.name,
            "account_display_name": self.account.display_name,
            "revoked_date": self.revoked_date.isoformat() if self.revoked_date else None,
        }


class Event(Base):
    __tablename__ = 'event'
    id: Mapped[int] = mapped_column(sa.Integer, sa.Identity(), primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(sa.String(50), nullable=False)
    description: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    data: Mapped[dict] = mapped_column(sa.JSON, nullable=True)
    date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(tz=datetime.timezone.utc))
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))
    user: Mapped[User] = relationship('User')
    # account_id & account

    def __repr__(self):
        return f"Event(id={self.id!r}, type={self.type!r})"
    
    async def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "description": self.description,
            "data": self.data,
            "date": self.date.isoformat(),
            "user_id": self.user_id,
        }


class UserInvite(Base):
    __tablename__ = 'user_invite'
    id: Mapped[int] = mapped_column(sa.Integer, sa.Identity(), primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))
    token: Mapped[str] = mapped_column(sa.String(255), unique=True, nullable=False)
    invited_by_user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))
    invite_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(tz=datetime.timezone.utc))
    accepted: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f"UserInvite(id={self.id!r})"
    
    async def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "invited_by_user_id": self.invited_by_user_id,
            "invite_date": self.invite_date.isoformat(),
            "accepted": self.accepted
        }
    
    async def generate_url(self, db_session):
        self.token = secrets.token_urlsafe(32)
        db_session.add(self)
        await db_session.commit()
        return f"{cfg.APP_URL}/invite/{self.token}"
        