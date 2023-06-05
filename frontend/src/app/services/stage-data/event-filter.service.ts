import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { StageServiceBase } from './stage-service-base';

@Injectable({
  providedIn: 'root',
})
export class EventFilterService extends StageServiceBase {
  public baseRoute = '/event';
  public stageName = 'Event Filter';

  constructor(private http: HttpClient) {
    super(http);
  }
}
