import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpErrorResponse,
} from '@angular/common/http';
import { catchError, Observable, throwError } from 'rxjs';
import { MatSnackBar } from '@angular/material/snack-bar';
import { SnackbarService } from '../snackbar.service';

@Injectable()
export class ErrorHandlingInterceptor implements HttpInterceptor {
  private handleError(error: HttpErrorResponse) {
    let userMsg: string;
    if (error.status === 0) {
      // A client-side or network error occurred. Handle it accordingly.
      userMsg = `An error occurred, check the console for more informations`;
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong.
      userMsg = `Backend returned code ${
        error.status
      }, body was: ${JSON.stringify(error.error)}`;
    }
    console.error(error);
    this.snackbarService.error(userMsg);
    // Return an observable with a user-facing error message.
    return throwError(
      () => new Error('Something bad happened; please try again.')
    );
  }

  constructor(private snackbarService: SnackbarService) {}

  intercept(
    request: HttpRequest<unknown>,
    next: HttpHandler
  ): Observable<HttpEvent<unknown>> {
    return next.handle(request).pipe(
      // Map response body having result
      catchError((err) => this.handleError(err))
    );
  }
}
