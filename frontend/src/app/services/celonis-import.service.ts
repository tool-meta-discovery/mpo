import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, Subject, tap } from 'rxjs';
import { environment } from 'src/environments/environment';
import { EventLogService } from './eventlog.service';

@Injectable({
  providedIn: 'root',
})
export class CelonisImportService {
  private _celonisModelsSubject: Subject<string[]> = new Subject<string[]>();

  get celonisModelsSubject(): Subject<string[]> {
    return this._celonisModelsSubject;
  }

  constructor(
    private http: HttpClient,
    private eventLogService: EventLogService
  ) {}

  public fetchModels(apiCred: {
    celonis_url: string;
    celonis_key: string;
    is_user_key: boolean;
  }): Observable<string[]> {
    return this.http
      .post<string[]>(
        `${environment.backendUrl}/import/get_available_data_models`,
        apiCred
      )

      .pipe(tap((res) => this._celonisModelsSubject.next(res)));
  }

  public importModel(
    apiCred: {
      celonis_url: string;
      celonis_key: string;
      is_user_key: boolean;
    },
    model: string
  ): Observable<string> {
    console.log({ ...apiCred });
    return this.http
      .post<string>(`${environment.backendUrl}/import/import_data_model`, {
        ...apiCred,
        name: model,
      })
      .pipe(tap(() => this.eventLogService.reloadEventLogs()));
  }
}
