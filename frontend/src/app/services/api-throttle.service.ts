import { HttpEvent, HttpHandler, HttpRequest } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { finalize, Observable, switchMap, tap, timer } from 'rxjs';
import { environment } from 'src/environments/environment';
import { sessionUrl } from './http-interceptors/session.interceptor';

@Injectable({
  providedIn: 'root',
})
export class APIThrottleService {
  private ongoingReq: boolean = false;

  public intercept(
    req: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    if (req.url.startsWith(environment.backendUrl) && req.url != sessionUrl) {
      // if there is an ongoing request throw error otherwise pass to next interceptor
      return timer(0).pipe(
        tap((_) => {
          if (this.ongoingReq)
            throw { message: 'Pending Request', status: -100 };
          this.ongoingReq = true;
        }),
        switchMap(() =>
          next.handle(req).pipe(
            finalize(() => {
              this.ongoingReq = false;
            })
          )
        )
      );
    } else {
      return next.handle(req);
    }
  }
}
