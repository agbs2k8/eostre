"use client";
import { ProtectedRoute } from "@utils/ProtectedRoute";
import { useEffect, useState } from "react";
import { apiClient } from "@utils/apiClient";
import { useUser } from "@utils/userProvider";
import { useAuth } from "@utils/authProvider";
import { Button } from "@ui-components/Button";
import { DataTable } from "@ui-components/DataTable";
import { Drawer } from "@ui-components/Drawer";


export default function AccountPage() {
  return (
    <ProtectedRoute>
      <AccountForm />
    </ProtectedRoute>
  );
}

function AccountForm() {
  const { accessToken, user } = useAuth();
  const { userProfile, loading } = useUser();
  const currentAccountId = Number(user?.account_id);
  const accountName =
    userProfile?.grants.find(
      (grant) => grant.account_id === currentAccountId
    )?.account_display_name ?? null;
  const [rowData, setRowData] = useState<UsersTableRow[]>([]);
  const [selectedRow, setSelectedRow] = useState<any | null>(null);


  interface ApiGrant {
    account_display_name: string;
    account_id: string;
    account_name: string;
    active: boolean;
    granted_date: string;
    id: number;
    revoke_date?: string;
    role_id: number;
    role_name: string;
    user_id: number
  }

  interface ApiAccountUsers {
    created_date: string;
    email: string;
    grants: ApiGrant[];
    id: number;
    modified_date: string;
    name: string;
    type: string;
  }

  interface UsersTableRow {
    name: string;
    email: string;
    modifiedDate: string;
    type: string;
    roles: number;
  }

  const columnDefs = [
    { field: "name", sortable: true, filter: true, flex: 1, resizable: true },
    { field: "email", sortable: true, filter: true, flex: 1, resizable: true },
    { field: "modifiedDate", sortable: true, filter: true, flex: 1, resizable: true },
    { field: "type", sortable: false, filter: true, flex: 1, resizable: true },
    { field: "roles", sortable: true, filter: true, flex: 1, resizable: true },
  ]

  useEffect(() => {
    if (!accessToken) return; // wait until accessToken exists

    const fetchUsers = async () => {
      try {
        console.log("Fetching users with token:", accessToken);
        const res = await apiClient<ApiAccountUsers[]>("/api/v1/account/user", accessToken);
        const tableRows: UsersTableRow[] = res.map(item => ({
          name: item.name,
          email: item.email,
          modifiedDate: item.modified_date,
          type: item.type,
          roles: item.grants.length
        }));
        setRowData(tableRows);
      } catch (err) {
        console.error("Fetch failed", err);
      }
    };
    fetchUsers();
  }, [accessToken]);
  return (
    <>
      <div className="font-sans min-h-screen p-8 sm:p-20 bg-brand-light text-brand-dark dark:bg-brand-dark dark:text-brand-light">
        <main className="flex flex-col gap-8 w-full">
          {/* Header with title and +Add button */}
          <div className="w-full flex items-center justify-between mb-6">
            <h1 className="text-2xl font-bold text-brand-primary dark:text-accent-cyan">
              {accountName}
            </h1>
            <Button
              onClick={() => true}
              aria-label="Open add location drawer"
            >
              Change
            </Button>
          </div>

          {/* DataTable */}
          <DataTable
            columnDefs={columnDefs}
            rowData={rowData}
            autoHeight={true}
            paginationPageSize={5}
            onRowClick={(row) => setSelectedRow(row)}
          />
          <Drawer 
            isOpen={!!selectedRow} 
            onClose={() => setSelectedRow(null)}
            title="Edit User"
            side="right"
            variant="form"
          >
            {selectedRow ? (
              <div className="p-4">
                <h2 className="text-lg font-bold">{selectedRow.name}</h2>
                <p>Email: {selectedRow.email}</p>
                <p>Type: {selectedRow.type}</p>
                {/* Or drop in a <UserEditForm row={selectedRow} /> here */}
              </div>
            ) : null}
          </Drawer>
        </main>
      </div>
    </>
  );
}