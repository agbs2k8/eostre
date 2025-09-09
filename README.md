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
2. Forward location (if deleted, optiona re-direct to other objectId)
3. FIND endpoint


# UI Plan
- Layout & Navigation
- Design 
- Locations
  - Create Location Modal
  - Edit Loction Modal
  - Delete Location menu-option w/ warning pop-up
  - Deleted locations tab/table (AgGrid)
  - Restore deleted location