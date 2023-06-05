import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { APIThrottleService } from '../api-throttle.service';

@Injectable()
export class APIThrottleInterceptor implements HttpInterceptor {
  constructor(private apiThrottleService: APIThrottleService) {}

  intercept(
    request: HttpRequest<unknown>,
    next: HttpHandler
  ): Observable<HttpEvent<unknown>> {
    return this.apiThrottleService.intercept(request, next);
  }
}
