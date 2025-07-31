import sqlalchemy
import sqlalchemy.orm
# Import from the project
import sys
sys.path.append('./src')
import config as cfg
sys.path.append('./src/models')
from models.models import (User,
                           Account,
                           Role,
                           Permission,
                           Grant,
                           Email,
                           Event,
                           Base)

if __name__ == "__main__":
    config_file = "./.env"
    with open(config_file, "r") as f:
        cfg_file = {x.split("=")[0].strip():x.split("=")[1].strip() for x in f.readlines()}
    engine = sqlalchemy.create_engine(cfg.DATABASE_URI, echo=True, pool_pre_ping=True)

    Base.metadata.create_all(engine)

    with sqlalchemy.orm.Session(engine) as session:
        # Create Primary Service account
        #sa_email = Email(email=f"{cfg_file['APP_ADMIN_USER']}@local.host")
        #session.add(sa_email)
        service_account = User(name="master_service_account",
                               display_name="Master Service Account",
                               password=cfg_file["APP_ADMIN_PASSWORD"],
                               email=f"{cfg_file['APP_ADMIN_USER']}@local.host",
                               type="service")
        session.add(service_account)
        session.flush()
        event1 = Event(
            user=service_account,
            type="system",
            description="Service account created",
            data={"account": service_account.__repr__()}
        )
        session.add(event1)
        
        # Create Admin Role & Permissions
        account_read_permission = Permission(name="account.read", display_name="Account Read", scope="read")
        account_write_permission = Permission(name="account.write", display_name="Account Write", scope="write")
        session.add_all([account_read_permission, account_write_permission])
        session.flush()
        account_admin_role = Role(name="account.admin", display_name="Account Admin",
                                  permissions=[account_read_permission, account_write_permission])
        session.add(account_admin_role)
        event2 = Event(
            user=service_account,
            type="system",
            description="Acount admin role created",
            data={"permissions": [account_read_permission.__repr__(), account_write_permission.__repr__()]}
        )
        session.add(event2)
        session.flush()
        
        # Create Demo Account
        demo_account = Account(name="demo",
                               display_name="Demo Account")
        session.add(demo_account)
        event3 = Event(
            user=service_account,
            type="system",
            description="Demo account created",
            data={"Account": demo_account.__repr__()}
        )
        session.add(event3)
        
        # Grant SA the admin role for the demo account
        sa_grant = Grant(user=service_account, account=demo_account, role=account_admin_role)
        session.add(sa_grant)
        event4 = Event(
            user=service_account,
            type="system",
            description="Service account granted admin role for demo account",
            data={"grant": sa_grant.__repr__()}
        )
        session.add(event4)
       
        # session.commit()
        print(f"users: {[x for x in session.scalars(sqlalchemy.select(User))]}")
        print(f"accounts: {[x for x in session.scalars(sqlalchemy.select(Account))]}")
        print(f"roles: {[x for x in session.scalars(sqlalchemy.select(Role))]}")
        print(f"permissions: {[x for x in session.scalars(sqlalchemy.select(Permission))]}")
        print(f"grants: {[x for x in session.scalars(sqlalchemy.select(Grant))]}")
        print(f"emails: {[x for x in session.scalars(sqlalchemy.select(Email))]}")
        print(f"events: {[x for x in session.scalars(sqlalchemy.select(Event))]}")
        session.commit()
        print("Database populated successfully.")
    print("Done.")

