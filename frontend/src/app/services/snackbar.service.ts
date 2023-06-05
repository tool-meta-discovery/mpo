import { Injectable, NgZone } from '@angular/core';
import { MatSnackBar, MatSnackBarConfig } from '@angular/material/snack-bar';

@Injectable({
  providedIn: 'root',
})
export class SnackbarService {
  constructor(private snackBar: MatSnackBar, private zone: NgZone) {}

  public notify(message: string) {
    const config = new MatSnackBarConfig();
    config.horizontalPosition = 'center';
    config.verticalPosition = 'top';
    config.panelClass = ['notify-snackbar'];
    config.duration = 5000;

    this.zone.run(() => {
      this.snackBar.open(message, 'Ok', config);
    });
  }

  public error(message: string) {
    const config = new MatSnackBarConfig();
    config.horizontalPosition = 'center';
    config.verticalPosition = 'top';
    config.panelClass = ['error-snackbar'];
    config.duration = 10000;

    this.zone.run(() => {
      this.snackBar.open(message, 'Dismiss', config);
    });
  }
}
