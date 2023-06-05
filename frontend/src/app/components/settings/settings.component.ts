import { Component, OnInit } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { SnackbarService } from 'src/app/services/snackbar.service';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss'],
})
export class SettingsComponent implements OnInit {
  constructor(
    private cookieService: CookieService,
    private snackbar: SnackbarService
  ) {}

  ngOnInit(): void {}

  onDeleteCookies() {
    this.cookieService.deleteAll();
    this.snackbar.notify('Cookies have been deleted.');
  }
}
