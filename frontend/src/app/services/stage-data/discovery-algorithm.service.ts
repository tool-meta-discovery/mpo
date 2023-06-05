import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { StageServiceBase } from './stage-service-base';

@Injectable({
  providedIn: 'root',
})
export class DiscoveryAlgorithmService extends StageServiceBase {
  public baseRoute = '/algorithm';
  public stageName = 'Discovery Algorithm';

  constructor(private http: HttpClient) {
    super(http);
  }
}
