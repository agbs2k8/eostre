"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@utils/authProvider";
import { apiClient } from "@utils/apiClient";
import { DataTable } from "@ui-components/DataTable";
import { Button } from "@ui-components/Button";
import { Drawer } from "@ui-components/Drawer";
import { ProtectedRoute } from "@utils/ProtectedRoute";
import ReactJson from "react-json-view";
import { useThemeContext } from "@/packages/utils/src";

export default function LocationsPage() {
  return (
    <ProtectedRoute>
      <Locations />
    </ProtectedRoute>
  );
}

function Locations() {
  const { accessToken } = useAuth();
  const [rowData, setRowData] = useState<TableRow[]>([]);
  const [isAddOpen, setAddOpen] = useState(false);
  const [selectedRow, setSelectedRow] = useState<any | null>(null);
  const {isDark, setIsDark} = useThemeContext();


  interface ApiLocation {
    _id: string;
    _name: string;
    display_name: string;
    account_id: string;
    created_by: string;
    created_date: string;
    modified_date: string;
    deleted: boolean;
    active: boolean;
    geo_point?: {
      type: string;
      coordinates: [number, number, number?];
    };
    address?: {
      countryRegion?: { name };
      addressLine?: string;
      adminDistricts?: { name: string; shortName: string }[];
      formattedAddress?: string;
      locality?: string;
      postalCode?: string;
      streetName?: string;
      streetNumber?: string;
    };
  }

  interface TableRow {
    name: string;
    createdBy: string;
    createdDate: string;
    modifiedDate: string;
    geoPoint: string;
    address: string;
  }

  const columnDefs = [
    { field: "name", sortable: true, filter: true, flex: 1, resizable: true },
    { field: "createdBy", sortable: true, filter: true, width: 150, resizable: true },
    { field: "createdDate", sortable: true, filter: true, flex: 1, resizable: true },
    { field: "modifiedDate", sortable: true, filter: true, flex: 1, resizable: true },
    { field: "geoPoint", sortable: false, filter: true, width: 250, resizable: true },
    { field: "address", sortable: true, filter: true, flex: 1, resizable: true },
  ];

  useEffect(() => {
    apiClient<{ data: ApiLocation[] }>("/locationserv/location", accessToken)
      .then(res => {
        const tableRows: TableRow[] = res.data.map(item => ({
          id: item._id,
          name: item.display_name,
          createdBy: item.created_by,
          createdDate: item.created_date,
          modifiedDate: item.modified_date,
          geoPoint: item.geo_point?.coordinates?.join(", ") || "",
          address: item.address?.formattedAddress || "",
          fullObject: item,
        }));
        setRowData(tableRows);
      })
      .catch(err => console.error("Fetch failed", err));
  }, []);

  return (
    <>
        <div className="font-sans min-h-screen p-8 sm:p-20 bg-brand-light text-brand-dark dark:bg-brand-dark dark:text-brand-light">
          <main className="flex flex-col gap-8 w-full">
            {/* Header with title and +Add button */}
            <div className="w-full flex items-center justify-between mb-6">
              <h1 className="text-2xl font-bold text-brand-primary dark:text-accent-cyan">
                Locations
              </h1>
              <Button
                onClick={() => setAddOpen(true)}
                aria-label="Open add location drawer"
              >
                + Add
              </Button>
            </div>

            {/* DataTable */}
            <DataTable 
              columnDefs={columnDefs} 
              rowData={rowData} 
              autoHeight={true}
              paginationPageSize={10}
              onRowClick={(row) => setSelectedRow(row)}
            />
          </main>
        </div>
        {/* Drawer for viewing location details */}
        <Drawer
         isOpen={!!selectedRow} 
            onClose={() => setSelectedRow(null)}
            title="Edit Location"
            side="right"
            variant="form"
        >
          {selectedRow ? (
            <div className="p-4">
              <h2 className="text-lg font-bold">{selectedRow.name}</h2>
              <ReactJson
                src={selectedRow.fullObject}
                name={false}
                collapsed={2}
                enableClipboard={true}
                displayDataTypes={false} 
                indentWidth={2}
                iconStyle={"triangle"}
                theme={isDark ? "railscasts" : "rjv-default"}
              />
            </div>
          ) : null}
        </Drawer>


        {/* Drawer for adding locations */}
        <Drawer
          isOpen={isAddOpen}
          onClose={() => setAddOpen(false)}
          title="Add Location"
          side="right"
          variant="form"
        >
          {/* Example form inside drawer */}
          <form className="flex flex-col gap-4">
            <label className="flex flex-col">
              Name
              <input className="mt-1 p-2 border rounded bg-brand-light dark:bg-brand-dark dark:text-brand-light" />
            </label>
            <label className="flex flex-col">
              Address
              <input className="mt-1 p-2 border rounded bg-brand-light dark:bg-brand-dark dark:text-brand-light" />
            </label>
            <div className="flex justify-end gap-2 mt-4">
              <Button onClick={() => setAddOpen(false)}>Cancel</Button>
              <Button type="submit">Save</Button>
            </div>
          </form>
        </Drawer>
    </>
  );
}
