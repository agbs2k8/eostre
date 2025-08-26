"use client";

import React from "react";
import { AgGridReact } from "ag-grid-react";
import { ModuleRegistry, AllCommunityModule, colorSchemeDark } from "ag-grid-community";
import { ColDef, GridOptions, themeQuartz } from "ag-grid-community";
import {Theme} from "ag-grid-community"

// Register all community modules (only once)
ModuleRegistry.registerModules([AllCommunityModule]);

export interface DataTableProps extends Partial<GridOptions> {
  columnDefs: ColDef[];
  rowData: any[];
  className?: string;
}

const myTheme = themeQuartz.withPart(colorSchemeDark)

export const DataTable: React.FC<DataTableProps> = ({
  columnDefs,
  rowData,
  className,
  ...gridOptions
}) => {
  return (
    <div className={className || ""} style={{ height: 750, width:"100%"}}>
      <AgGridReact
        theme={myTheme}
        columnDefs={columnDefs}
        rowData={rowData}
        pagination
        paginationPageSize={15}
        {...gridOptions}
      />
    </div>
  );
};