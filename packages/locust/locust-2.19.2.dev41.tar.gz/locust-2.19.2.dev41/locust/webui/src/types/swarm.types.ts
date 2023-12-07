import {
  ICharts,
  ISwarmError,
  ISwarmStat,
  IResponseTime,
  ISwarmRatios,
  ISwarmException,
} from 'types/ui.types';

export interface IExtraOptionParameter {
  choices: string[] | null;
  defaultValue: string | boolean | null;
  helpText: string | null;
  isSecret: boolean;
}

export interface IExtraOptions {
  [key: string]: IExtraOptionParameter;
}

export type History = Omit<ICharts, 'markers'>;

export interface IReport {
  locustfile: string;
  showDownloadLink: boolean;
  startTime: string;
  endTime: string;
  host: string;
  charts: ICharts;
  requestsStatistics: ISwarmStat[];
  failuresStatistics: ISwarmError[];
  responseTimeStatistics: IResponseTime[];
  exceptionsStatistics: ISwarmException[];
  tasks: ISwarmRatios;
}

export interface IReportTemplateArgs extends IReport {
  history: ICharts[];
  is_report?: boolean;
  percentile1: number;
  percentile2: number;
}
