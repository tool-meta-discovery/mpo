import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpClient,
  HttpErrorResponse,
} from '@angular/common/http';
import { catchError, mergeMap, Observable, of, throwError } from 'rxjs';
import { environment } from 'src/environments/environment';

export const sessionUrl =
  environment.backendUrl + '/configuration/start_session';
@Injectable()
export class SessionInterceptor implements HttpInterceptor {
  constructor(private http: HttpClient) {}

  intercept(
    req: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    if (!req.url.startsWith(environment.backendUrl)) {
      return next.handle(req);
    }
    const sessionReq = req.clone({
      withCredentials: true,
    });
    return next.handle(sessionReq).pipe(
      catchError((error: HttpErrorResponse) => {
        // If the error is 401 then try to start_session
        // Otherwise rethrow the error.
        if (error.status === 401) {
          return this.http.get(sessionUrl).pipe(
            mergeMap((_) => {
              return next.handle(sessionReq);
            })
          );
        }
        return throwError(() => error);
      })
    );
  }
}
