import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpEventType,
} from '@angular/common/http';
import { map, Observable } from 'rxjs';

@Injectable()
export class FlaskResponseInterceptor implements HttpInterceptor {
  constructor() {}

  intercept(
    request: HttpRequest<unknown>,
    next: HttpHandler
  ): Observable<HttpEvent<unknown>> {
    return next.handle(request).pipe(
      // Map response body having result
      map((val) => {
        if (val.type == HttpEventType.Response)
          if (val.body.result) {
            // Convert to json if result string is a stringified json
            try {
              return val.clone({
                body: JSON.parse(val.body.result),
              });
            } catch (error) {
              return val.clone({
                body: val.body.result,
              });
            }
          }
        return val;
      })
    );
  }
}
