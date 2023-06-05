/* "Barrel" of Http Interceptors */
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { APIThrottleRetryInterceptor } from './api-throttle-retry.interceptor';
import { APIThrottleInterceptor } from './api-throttle.interceptor';
import { ErrorHandlingInterceptor } from './error-handling.interceptor';
import { FlaskResponseInterceptor } from './flask-response.interceptor';
import { SessionInterceptor } from './session.interceptor';

/** Http interceptor providers in outside-in order */
export const HttpInterceptorProviders = [
  {
    provide: HTTP_INTERCEPTORS,
    useClass: APIThrottleRetryInterceptor,
    multi: true,
  },
  {
    provide: HTTP_INTERCEPTORS,
    useClass: APIThrottleInterceptor,
    multi: true,
  },
  {
    provide: HTTP_INTERCEPTORS,
    useClass: ErrorHandlingInterceptor,
    multi: true,
  },
  {
    provide: HTTP_INTERCEPTORS,
    useClass: FlaskResponseInterceptor,
    multi: true,
  },
  { provide: HTTP_INTERCEPTORS, useClass: SessionInterceptor, multi: true },
];
