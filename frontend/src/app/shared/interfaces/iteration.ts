import { Qualities } from './qualities';

export interface Iteration {
  bpmn_download_url: string;
  pnml_download_url: string;
  model: string;
  quality: Qualities;
  parameter: {
    [keys: string]: any;
  };
}
