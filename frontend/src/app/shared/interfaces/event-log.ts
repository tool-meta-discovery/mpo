import { Moment } from 'moment';

export interface EventLog {
  name: string;
  cases: number;
  events: number;
  date: Moment;
  head: object[];
}
