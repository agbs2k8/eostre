# eostre
Multi-tenant web-app 

# TODO - AdminServer: 
1. Fix tests
2. Finish account CRUD 
3. Add ability to add new user to an account
4. Single-source of truth for RBAC/ABAC
  - Permissions per endpoint/resource
  - editable
  - reload on edit
5. Tags for ABAC

# TODO - LocationServ
1. Add tests
2. Load Capitols (US, CA, Global) to populate the database
3. Forward location (if deleted, optiona re-direct to other objectId)
4. FIND endpoint

# TODO - TagService
1. Create / Read / Update / Delete
2. 

# UI Plan
- Login handler
- Locations
  - List locations AgGrid Table + Menu 
  - Create Location Modal
  - Edit Loction Modal
  - Delete Location menu-option w/ warning pop-up
  - Deleted locations tab/table (AgGrid)
  - Restore deleted location
  - Forward deleted location