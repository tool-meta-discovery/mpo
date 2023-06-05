import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { StageServiceBase } from './stage-service-base';

@Injectable({
  providedIn: 'root',
})
export class TraceFilterService extends StageServiceBase {
  public baseRoute = '/trace';
  public stageName = 'Trace Filter';

  constructor(private http: HttpClient) {
    super(http);
  }
}
