import uuid
import asyncio
import secrets
import datetime
from collections import defaultdict
from typing import ClassVar
import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from src.db import Base, role_permission_table
import config as cfg
import logging

logger = logging.getLogger(__name__)


class Account(Base):
    __tablename__ = 'account'
    id: Mapped[str] = mapped_column(
        sqlalchemy.String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4()), 
        unique=True
    )
    name: Mapped[str] = mapped_column(sqlalchemy.String(255), nullable=False, unique=True)
    display_name: Mapped[str] = mapped_column(sqlalchemy.String(255), nullable=True)
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
        result = await db_session.execute(sqlalchemy.select(Account).where(Account.id == account_id))
        return result.scalars().first()


class Permission(Base):
    __tablename__ = 'permission'
    id: Mapped[str] = mapped_column(
        sqlalchemy.String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4()), 
        unique=True
    )
    name: Mapped[str] = mapped_column(sqlalchemy.String(255), nullable=False, unique=True)
    display_name: Mapped[str] = mapped_column(sqlalchemy.String(255), nullable=True)
    active: Mapped[bool] = mapped_column(default=True)
    created_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(tz=datetime.timezone.utc))
    modified_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(tz=datetime.timezone.utc))
    deleted: Mapped[bool] = mapped_column(default=False)
    # scope = Create, Read, Update or Delete
    scope: Mapped[str] = mapped_column(sqlalchemy.String(255), nullable=False)
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
    id: Mapped[str] = mapped_column(
        sqlalchemy.String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4()), 
        unique=True
    )
    name: Mapped[str] = mapped_column(sqlalchemy.String(255), nullable=False, unique=True)
    display_name: Mapped[str] = mapped_column(sqlalchemy.String(255), nullable=True)
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
        result = await db_session.execute(sqlalchemy.select(Role).where(Role.id == role_id))
        return result.scalars().first()


class Email(Base):
    __tablename__ = 'email'
    id: Mapped[str] = mapped_column(
        sqlalchemy.String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4()), 
        unique=True
    )
    email: Mapped[str] = mapped_column(sqlalchemy.String(255), nullable=False, unique=True)
    user_id: Mapped[str] = mapped_column(sqlalchemy.ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User", back_populates="emails")
    primary: Mapped[bool] = mapped_column(default=False)
    active: Mapped[bool] = mapped_column(default=True)
    created_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(tz=datetime.timezone.utc))
    deleted: Mapped[bool] = mapped_column(default=False)
    validated: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f"Email(id={self.id!r}, email={self.email!r})"
    
    def __str__(self) -> str:
        return self.email
    
    async def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "primary": self.primary,
            "active": self.active,
            "created_date": self.created_date.isoformat(),
            "validated": self.validated
        }
    
    @staticmethod
    async def find(email: str, db_session):
        """
        Find a email obj by the email address.
        :param email: email address
        :return: Email object or None if not found.
        """
        result = await db_session.execute(sqlalchemy.select(Email).where(Email.email == email))
        return result.scalars().first()
    
    # Enfore single instance of primary per use when migrated to postgresql
    # __table_args__ = (
    #     # Enforce only one primary email per user
    #    sqlalchemy.Index(
    #         "uq_primary_email_per_user",
    #         "user_id",
    #         unique=True,
    #         postgresql_where=sqlalchemy.text("primary = true"),
    #     ),
    # )


class User(Base):
    __tablename__ = 'user'
    id: Mapped[str] = mapped_column(
        sqlalchemy.String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4()), 
        unique=True
    )
    name: Mapped[str] = mapped_column(sqlalchemy.String(255), nullable=False, unique=True)
    type: Mapped[str] = mapped_column(sqlalchemy.String(50), nullable=False, default="user")  # user vs service
    emails: Mapped[list["Email"]] = relationship(
        "Email",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan"
    )
    personal_name: Mapped[str] = mapped_column(sqlalchemy.String(255), nullable=True)
    family_names: Mapped[list[str]] = mapped_column(sqlalchemy.String(255), nullable=True)
    display_name: Mapped[str] = mapped_column(sqlalchemy.String(255), nullable=True)
    active: Mapped[bool] = mapped_column(default=True)
    created_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(tz=datetime.timezone.utc))
    modified_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(tz=datetime.timezone.utc))
    password: Mapped[str] = mapped_column(sqlalchemy.String(255), nullable=False)
    grants: Mapped[list['Grant']] = relationship('Grant', 
                                                 back_populates='user', 
                                                 foreign_keys='Grant.user_id', 
                                                 lazy='selectin')
    deleted: Mapped[bool] = mapped_column(default=False)

    def __init__(self, 
                 name: str, 
                 password: str, 
                 email: str, 
                 type: str = "user", 
                 display_name = None, 
                 personal_name = None,
                 family_names = None,
                 force_email = False):
        self.name = name
        self.type = type
        self.personal_name = personal_name
        self.family_names = [x.strip() for x in family_names.split(',')] if family_names else None
        self.display_name = display_name
        self.active = True
        self.created_date = datetime.datetime.now(tz=datetime.timezone.utc)
        self.modified_date = datetime.datetime.now(tz=datetime.timezone.utc)
        self.password = generate_password_hash(password)
        self.deleted = False
        if email and force_email:
            self.emails.append(Email(email=email, primary=True, validated=True))
        elif email:
            self.emails.append(Email(email=email, primary=True))

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r})"
    
    def __hash__(self):
        return hash(self.id)
    
    @property
    def primary_email(self) -> Email | None:
        return next((e for e in self.emails if e.primary), None)
    
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
            "email": self.primary_email.email if self.primary_email else None#,
            #"accounts": [account.name for account in self.accounts],
            #"grants": [await grant.to_dict() for grant in self.grants]
        }
    
    async def set_primary_email(self, new_primary_email: Email, db_sesion):
        for e in self.email:
            e.primary = False
        new_primary_email.primary = True
        await db_sesion.commit()

    async def get_grants(self, db_session):
        """
        Get all grants for the user.
        :param db_session: The database session to use for the query.
        :return: List of Grant objects associated with the user.
        """
        result = await db_session.execute(sqlalchemy.select(Grant).where(Grant.user_id == self.id, Grant.active == True))
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
    
    @staticmethod
    async def find(name: str, db_session):
        """
        Find a user by name.
        :param name: The name of the user to find.
        :return: User object or None if not found.
        """
        result = await db_session.execute(sqlalchemy.select(User).where(User.name == name))
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
        result = await db_session.execute(sqlalchemy.select(User).join(Email).where(Email.email == email))
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
        result = await db_session.execute(sqlalchemy.select(User).where(User.id == user_id))
        return result.scalars().first()
    
    @staticmethod
    async def full_user_json(user, db_session):
        user_obj = {
            'id': user.id,
            'name': user.name,
            'type': user.type,
            'emails': await asyncio.gather(*(e.to_dict() for e in user.emails)),
            'personal_name': user.personal_name,
            'family_names': user.family_names,
            'display_name': user.display_name,
            'active': user.active,
            'created_date': user.created_date.isoformat(),
            'modified_date': user.modified_date.isoformat(),
            'deleted': user.deleted,
            'grants': await asyncio.gather(*(grant.to_dict() for grant in user.grants)),
            'permissions': await user.get_permissions(db_session)
        }
        return user_obj
    
    @staticmethod
    async def get_all_json_by_account(account_id, db_sesion):
        logger.debug(f"Retrieving all users for account {account_id}")
        
        result = await db_sesion.execute(
            sqlalchemy.select(User)
            .where(User.active == True,
                User.deleted == False,
                User.id.in_(
                    sqlalchemy.select(Grant.user_id).where(
                        Grant.account_id == account_id,
                        Grant.active == True)))
            .options(
                sqlalchemy.orm.selectinload(User.emails),
                sqlalchemy.orm.selectinload(User.grants)
                    .selectinload(Grant.role)
                    .selectinload(Role.permissions),
                sqlalchemy.orm.selectinload(User.grants)
                    .selectinload(Grant.account),
            )
        )
        users = result.scalars().all()
        user_dicts = [await User.full_user_json(user, db_sesion) for user in users]
        return user_dicts
    
    @staticmethod
    async def get_json_user_by_id(user_id, db_session):
        result = await db_session.execute(
            sqlalchemy.select(User)
            .where(User.id == user_id)
            .options(
                sqlalchemy.orm.selectinload(User.emails),
                sqlalchemy.orm.with_loader_criteria(
                    Email,
                    lambda e: (e.active == sqlalchemy.true()) & (e.deleted == sqlalchemy.false())
                ),
                sqlalchemy.orm.selectinload(User.grants)
                    .selectinload(Grant.role)
                    .selectinload(Role.permissions),
                sqlalchemy.orm.selectinload(User.grants)
                    .selectinload(Grant.account),
            )
        )
        users = result.scalars().unique().all()
        if not users:
            return None
        user_dict = await User.full_user_json(users[0], db_session)
        return user_dict


class Grant(Base):
    __tablename__ = 'grant'
    id: Mapped[str] = mapped_column(
        sqlalchemy.String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4()), 
        unique=True
    )
    active: Mapped[bool] = mapped_column(default=True)
    granted_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(tz=datetime.timezone.utc))
    role_id: Mapped[str] = mapped_column(sqlalchemy.ForeignKey("role.id"))
    user_id: Mapped[str] = mapped_column(sqlalchemy.ForeignKey("user.id"))
    user: Mapped[User] = relationship('User', back_populates='grants', foreign_keys=[user_id])
    account_id: Mapped[str] = mapped_column(sqlalchemy.ForeignKey("account.id"), nullable=True)
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


class TokenEvent(Base):
    __tablename__ = 'token_event'
    """
    Events for which we need to generate, store, validate, expire a one-time-use token
    Supported types shown below as self.accepted_event_types
    """
    id: Mapped[str] = mapped_column(
        sqlalchemy.String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4()), 
        unique=True
    )
    event_type: Mapped[str] = mapped_column(sqlalchemy.String(255), nullable=False)
    event_key: Mapped[str] = mapped_column(sqlalchemy.String(255), unique=True, nullable=False) # the thing we're validating 
    created_by: Mapped[str] = mapped_column(sqlalchemy.ForeignKey("user.id"))
    created_for: Mapped[str] = mapped_column(sqlalchemy.ForeignKey("user.id"))
    token: Mapped[str] = mapped_column(sqlalchemy.String(255), unique=True, nullable=False)
    created_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now(tz=datetime.timezone.utc))
    expire_date: Mapped[datetime.datetime] = mapped_column(default=(datetime.datetime.now(tz=datetime.timezone.utc)+datetime.timedelta(hours=2)))
    validated: Mapped[bool] = mapped_column(default=False)

    # Not part of the SqlAlchemy table
    accpeted_event_types: ClassVar[list[str]] = ["email"]
    
    def __init__(self, 
                 type: str, 
                 key: str,
                 created_by: str, 
                 created_for: str = None,
                 hours_valid:int = 2):
        if type not in self.accpeted_event_types:
            raise ValueError(f"Invalid TokenEvent event `type` of {type}")
        self.event_type = type
        self.event_key = key
        self.created_by = created_by
        self.created_for = created_for if created_for else created_by
        self.token = secrets.token_urlsafe(32)
        self.created_date= datetime.datetime.now(tz=datetime.timezone.utc)
        self.expire_date = datetime.datetime.now(tz=datetime.timezone.utc)+datetime.timedelta(hours=hours_valid)
        self.validated = False

    def __repr__(self):
        return f"TokenEvent(id={self.id})"
    
    async def to_dict(self):
        return {
            "event_type": self.event_type,
            "event_key": self.event_key,
            "created_by": self.created_by,
            "created_for": self.created_for,
            "token": self.token,
            "expire_date": self.expire_date,
            "validated": self.validated
        }
    
    async def generate_url(self):
        return f"{cfg.CORS_ORIGIN}/{self.event_type}/validate/?token={self.token}"
    
    async def reset_expiration(self, requestor_id, hours_valid=2):
        """
        Similar to re-init, but cannot change type or targeted user
        """
        self.created_by = requestor_id
        self.created_date = datetime.datetime.now(tz=datetime.timezone.utc)
        self.expire_date = datetime.datetime.now(tz=datetime.timezone.utc)+datetime.timedelta(hours=hours_valid)
        self.token = secrets.token_urlsafe(32)
        self.validated = False
    
    async def resolve_email(self, db_session):
        """
        Use a standard method to resolve/commit the email to the database
        """
        target_user = await User.get(self.created_for, db_session)
        new_email = Email(email=self.event_key,
                          user_id=self.created_for,
                          user=target_user,
                          validated=True)
        db_session.add(new_email)
        db_session.commit()
        return self

    @staticmethod
    async def find(key: str, db_session):
        """
        Find an existing token even for which a key already exists.
        :param key: The key (i.e. email).
        :return: TokenEvent object
        """
        result = await db_session.execute(sqlalchemy.select(TokenEvent).where(TokenEvent.event_key == key))
        return result.scalars().first()

    @staticmethod
    async def accept_token(token: str, db_session):
        """
        Given a Token, validate and complete the transaction
        """
        result = await db_session.execute(sqlalchemy.select(TokenEvent).where(TokenEvent.token == token))
        te = result.scalars().first()

        if te and te.expire_date > datetime.datetime.now():
            match te.event_type:
                case "email":
                    await te.resolve_email(db_session)
                    await db_session.delete(te)
                    await db_session.commit()
                    return True, "Email added to the account"

                case _: 
                    raise ValueError(f"TokenEvent type of {te.event_type} was not found")
        else:
            return False, "The provided token was not found or the expiration date on the token has passed."
        