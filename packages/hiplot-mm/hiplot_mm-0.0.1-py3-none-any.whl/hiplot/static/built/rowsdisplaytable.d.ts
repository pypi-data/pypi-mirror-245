import React from "react";
import { Datapoint } from "./types";
import { HiPlotPluginData } from "./plugin";
import _ from "underscore";
interface RowsDisplayTableState {
}
export interface TableDisplayData {
    hide: Array<string>;
    order_by: Array<[string, string]>;
    order?: Array<string>;
}
interface TablePluginProps extends HiPlotPluginData, TableDisplayData {
}
export declare class RowsDisplayTable extends React.Component<TablePluginProps, RowsDisplayTableState> {
    table_ref: React.RefObject<HTMLTableElement>;
    table_container: React.RefObject<HTMLDivElement>;
    dt: any;
    ordered_cols: Array<string>;
    empty: boolean;
    setSelected_debounced: ((selected: Array<Datapoint>) => void) & _.Cancelable;
    static defaultProps: {
        hide: any[];
        order_by: string[][];
    };
    constructor(props: TablePluginProps);
    componentDidMount(): void;
    mountDt(): void;
    componentDidUpdate(prevProps: HiPlotPluginData): void;
    setSelectedToSearchResult(): void;
    setSelected(selected: Array<Datapoint>): void;
    render(): JSX.Element;
    destroyDt(): void;
    componentWillUnmount(): void;
}
export {};
