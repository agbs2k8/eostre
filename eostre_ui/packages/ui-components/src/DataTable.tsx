"use client";

import React, { useState, useCallback } from "react";
import { AgGridReact } from "ag-grid-react";
import {
  ModuleRegistry,
  AllCommunityModule,
  colorSchemeDark,
  ColDef,
  GridOptions,
  themeQuartz,
  GridReadyEvent,
  PaginationChangedEvent,
} from "ag-grid-community";

// Register all community modules (only once)
ModuleRegistry.registerModules([AllCommunityModule]);

// Constants for sizing
const DEFAULT_ROW_HEIGHT = 40; // px
const DEFAULT_HEADER_HEIGHT = 50; // px

export interface DataTableProps extends Partial<GridOptions> {
  columnDefs: ColDef[];
  rowData: any[];
  className?: string;
  /**
   * If true, the table height adjusts to fit visible rows + header.
   * If false, a fixed height (default 750px) is used.
   */
  autoHeight?: boolean;
  /**
   * Max number of rows to size for when autoHeight is enabled.
   * Defaults to paginationPageSize (or 15 if unset).
   */
  maxVisibleRows?: number;
  /**
   * Fixed height fallback (when autoHeight = false).
   */
  fixedHeight?: number;
  /**
   * Initial page size (default: 15).
   */
  paginationPageSize?: number;
  /**
   * Dropdown options for page size selector.
   */
  paginationPageSizeOptions?: number[];
  onRowClick?: (rowData: any) => void;
}

const myTheme = themeQuartz.withPart(colorSchemeDark);

export const DataTable: React.FC<DataTableProps> = ({
  columnDefs,
  rowData,
  className,
  autoHeight = false,
  maxVisibleRows,
  fixedHeight = 750,
  paginationPageSize = 15,
  paginationPageSizeOptions = [5, 10, 15, 20, 50, 100],
  onRowClick,
  ...gridOptions
}) => {
  const [gridApi, setGridApi] = useState<any>(null);
  const [currentPageSize, setCurrentPageSize] = useState(paginationPageSize);

  const onGridReady = useCallback((params: GridReadyEvent) => {
    setGridApi(params.api);
    setCurrentPageSize(params.api.paginationGetPageSize() || paginationPageSize);
  }, [paginationPageSize]);

  const onPaginationChanged = useCallback((event: PaginationChangedEvent) => {
    const newPageSize = event.api.paginationGetPageSize();
    setCurrentPageSize(newPageSize);
  }, []);

  // Use the smaller of: total rows, page size, or user-provided maxVisibleRows
  const effectivePageSize = maxVisibleRows
    ? Math.min(currentPageSize, maxVisibleRows)
    : currentPageSize;

  const visibleRowCount = Math.min(rowData.length, effectivePageSize);

  const computedHeight = autoHeight
    ? (visibleRowCount * DEFAULT_ROW_HEIGHT) + (DEFAULT_HEADER_HEIGHT * 2)
    : fixedHeight;

  return (
    <div
      className={className || ""}
      style={{ height: computedHeight, width: "100%" }}
    >
      <AgGridReact
        theme={myTheme}
        columnDefs={columnDefs}
        rowData={rowData}
        rowHeight={DEFAULT_ROW_HEIGHT}
        headerHeight={DEFAULT_HEADER_HEIGHT}
        pagination
        paginationPageSize={paginationPageSize}
        paginationPageSizeSelector={paginationPageSizeOptions}
        onGridReady={onGridReady}
        onPaginationChanged={onPaginationChanged}
        onRowClicked={(event) => {
          if (onRowClick) onRowClick(event.data);  // pass back the clicked row's data
        }}
        {...gridOptions}
      />
    </div>
  );
};
