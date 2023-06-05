import { HttpClient, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import * as moment from 'moment';
import {
  Observable,
  throwError,
  tap,
  map,
  BehaviorSubject,
  Subject,
  concatWith,
  ReplaySubject,
} from 'rxjs';
import { environment } from 'src/environments/environment';
import { EventLog } from '../shared/interfaces/event-log';
import { SnackbarService } from './snackbar.service';

@Injectable({
  providedIn: 'root',
})
export class EventLogService {
  private _eventLogsSubject: Subject<EventLog[]> = new BehaviorSubject<
    EventLog[]
  >([]);

  private _eventLogColumnsSubject: Subject<string[]> = new BehaviorSubject<
    string[]
  >([]);

  private _selectedEventLogSubject: Subject<EventLog> =
    new ReplaySubject<EventLog>();

  private _loadingLogsSubject: Subject<boolean> = new BehaviorSubject<boolean>(
    false
  );

  constructor(private http: HttpClient, private snackBar: SnackbarService) {
    this.reloadEventLogs();
  }

  public get eventLogColumnsSubject(): Subject<string[]> {
    return this._eventLogColumnsSubject;
  }

  public get eventLogsSubject(): Subject<EventLog[]> {
    return this._eventLogsSubject;
  }

  public get selectedEventLogSubject(): Subject<EventLog> {
    return this._selectedEventLogSubject;
  }

  public get loadingLogsSubject(): Subject<boolean> {
    return this._loadingLogsSubject;
  }

  public sendEventLog(
    eventLog: File,
    separator: string = ';'
  ): Observable<any> {
    const formData = new FormData();
    formData.append('file', eventLog);
    formData.append('separator', separator);

    const splittedName = eventLog.name.split('.');
    const fileType = splittedName[splittedName.length - 1];
    formData.append('file_type', fileType);

    return this.http
      .post<HttpResponse<string>>(
        `${environment.backendUrl}/import/upload_local_file`,
        formData,
        {
          reportProgress: true,
          observe: 'events',
        }
      )
      .pipe(
        concatWith(
          this.http
            .get<string[]>(`${environment.backendUrl}/import/get_column_names`)
            .pipe(
              tap(console.log),
              tap((val) => this._eventLogColumnsSubject.next(val))
            )
        )
      );
  }

  public sendSelectedColumns(selectedColumns: {
    activity: string;
    case: string;
    time: string;
  }): Observable<string> {
    if (!selectedColumns)
      return throwError(() => new Error('No columns have been set'));

    return this.http
      .post<string>(
        `${environment.backendUrl}/import/import_local_file`,
        selectedColumns
      )
      .pipe(tap(() => this.reloadEventLogs()));
  }

  public reloadEventLogs(): void {
    this._loadingLogsSubject.next(true);
    this.http
      .get<
        {
          name: EventLog['name'];
          cases: EventLog['cases'];
          events: EventLog['events'];
          date: string;
          head: string;
        }[]
      >(`${environment.backendUrl}/import/get_imported_data_sets`)
      .pipe(
        map((logs) => {
          return logs.map((log) => {
            return {
              ...log,
              date: moment(log.date),
              head: JSON.parse(log.head),
            };
          });
        })
      )
      .subscribe((val) => this._eventLogsSubject.next(val))
      .add(() => this._loadingLogsSubject.next(false));
  }

  public selectEventLog(eventLog: EventLog): Observable<string> {
    return this.http
      .post<string>(`${environment.backendUrl}/import/select_data`, {
        name: eventLog.name,
      })
      .pipe(
        tap(() => {
          this._selectedEventLogSubject.next(eventLog);
        })
      );
  }

  public deleteEventLog(eventLog: EventLog): void {
    this.http
      .post<string>(`${environment.backendUrl}/import/delete_data`, {
        name: eventLog.name,
      })
      .pipe(tap(() => this.reloadEventLogs()))
      .subscribe((res) => {
        if (res == 'data removed') {
          this.snackBar.notify(`${eventLog.name} has been removed.`);
        }
      });
  }
}
