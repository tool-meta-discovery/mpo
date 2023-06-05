import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
} from '@angular/common/http';
import { Observable, retry, timer } from 'rxjs';
@Injectable()
export class APIThrottleRetryInterceptor implements HttpInterceptor {
  constructor() {}

  intercept(
    request: HttpRequest<unknown>,
    next: HttpHandler
  ): Observable<HttpEvent<unknown>> {
    return next.handle(request).pipe(
      retry({
        count: 120,
        delay: (error: any, retryCount: number) => {
          if (error.status == -100) return timer(1000);
          throw error;
        },
      })
    );
  }
}
