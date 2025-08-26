"use client";

import { useEffect, useState } from "react";
import { apiClient } from "utils";
import { DataTable } from "ui-components";
import { themeQuartz } from "ag-grid-community"


export default function Home() {
  const [rowData, setRowData] = useState<TableRow[]>([]);

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
      countryRegion?: { name: string };
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
    { field: "createdBy", sortable: true, filter: true, width:150, resizable: true },
    { field: "createdDate", sortable: true, filter: true, flex: 1, resizable: true },
    { field: "modifiedDate", sortable: true, filter: true, flex: 1, resizable: true },
    { field: "geoPoint", sortable: false, filter: true, width:250, resizable: true },
    { field: "address", sortable: true, filter: true, flex: 1 , resizable: true},
  ];


  useEffect(() => {
    apiClient<{ data: ApiLocation[] }>("/api/locationserv/locations")
      .then(res => {
        const tableRows: TableRow[] = res.data.map(item => ({
          name: item.display_name,
          createdBy: item.created_by,
          createdDate: item.created_date,
          modifiedDate: item.modified_date,
          geoPoint: item.geo_point?.coordinates?.join(", ") || "",
          address: item.address?.formattedAddress || ""
        }));

        setRowData(tableRows);
      })
      .catch(err => console.error("Fetch failed", err));
  }, []);

  return (
    <div className="font-sans grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start w-full">
        <h1 className="text-2xl mb-4">Locations</h1>
        <DataTable columnDefs={columnDefs} rowData={rowData} />
        <ol className="font-mono list-inside list-decimal text-sm/6 text-center sm:text-left">
          <li className="mb-2 tracking-[-.01em]">
            Get started by editing{" "}
            <code className="bg-black/[.05] dark:bg-white/[.06] font-mono font-semibold px-1 py-0.5 rounded">
              location/src/app/page.tsx
            </code>
            .
          </li>
          <li className="tracking-[-.01em]">
            Save and see your changes instantly.
          </li>
        </ol>

        <div className="flex gap-4 items-center flex-col sm:flex-row">

        </div>
      </main>

    </div>
  );
}
