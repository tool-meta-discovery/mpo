import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { StageServiceBase } from './stage-service-base';

@Injectable({
  providedIn: 'root',
})
export class QualityMeasureService extends StageServiceBase {
  public baseRoute = '/quality';
  public stageName = 'Quality Measure';

  constructor(private http: HttpClient) {
    super(http);
  }
}
