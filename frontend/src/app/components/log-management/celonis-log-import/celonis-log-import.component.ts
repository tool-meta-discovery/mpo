import { Component, OnInit } from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  FormGroup,
  ValidationErrors,
  Validators,
} from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { CookieService } from 'ngx-cookie-service';
import { Subject } from 'rxjs';
import { CelonisImportService } from 'src/app/services/celonis-import.service';

@Component({
  selector: 'app-celonis-log-import',
  templateUrl: './celonis-log-import.component.html',
  styleUrls: ['./celonis-log-import.component.scss'],
})
export class CelonisLogImportComponent implements OnInit {
  public fetchingModels: boolean = false;
  public importingModel: boolean = false;
  public celonisCredentialsForm: FormGroup = this.fb.group({
    apiCredentials: this.fb.group({
      celonis_url: [
        '',
        [
          Validators.required,
          Validators.pattern(
            '(https?://)?([\\da-z.-]+)\\.([a-z.]{2,6})[/\\w .-]*/?'
          ),
        ],
      ],
      celonis_key: ['', [Validators.required, this.exactLengthValidator(108)]],
      is_user_key: [false],
    }),
    saveToCookies: [false],
  });

  public celonisModelSelectionForm: FormGroup = this.fb.group({
    model: ['', [Validators.required]],
  });

  public availableCelonisModelsSubject: Subject<string[]>;

  constructor(
    private fb: FormBuilder,
    private celonisImportService: CelonisImportService,
    private dialogRef: MatDialogRef<CelonisLogImportComponent>,
    private cookieService: CookieService
  ) {
    this.availableCelonisModelsSubject =
      this.celonisImportService.celonisModelsSubject;
  }

  ngOnInit(): void {
    const cookieCredentials = this.getCredentialsFromCookies();
    if (cookieCredentials) {
      console.log('Cookies found');
      console.log(cookieCredentials);
      this.celonisCredentialsForm.setValue({
        apiCredentials: cookieCredentials,
        saveToCookies: true,
      });
    }
    this.celonisCredentialsForm.valueChanges.subscribe((val) => {
      if (val.saveToCookies) {
        if (this.celonisCredentialsForm.valid)
          this.storeCredentialsInCookies(val.apiCredentials);
      } else {
        this.clearCookieCredentials();
      }
    });
  }

  onFetch() {
    this.fetchingModels = true;
    this.celonisImportService
      .fetchModels(this.celonisCredentialsForm.value.apiCredentials)
      .subscribe()
      .add(() => (this.fetchingModels = false));
  }

  onImport() {
    this.importingModel = true;
    this.celonisImportService
      .importModel(
        this.celonisCredentialsForm.value.apiCredentials,
        this.celonisModelSelectionForm.value.model
      )
      .subscribe(() => {
        this.importingModel = false;
        this.dialogRef.close();
      });
  }

  private getCredentialsFromCookies():
    | {
        celonis_url: string;
        celonis_key: string;
        is_user_key: boolean;
      }
    | undefined {
    const cookieCredentials = {
      celonis_url: this.cookieService.get('celonis_url'),
      celonis_key: this.cookieService.get('celonis_key'),
      is_user_key: this.cookieService.get('is_user_key') == 'true',
    };
    if (
      cookieCredentials.celonis_url == '' ||
      cookieCredentials.celonis_url == ''
    )
      return undefined;
    return cookieCredentials;
  }

  private storeCredentialsInCookies(apiCredentials: {
    celonis_url: string;
    celonis_key: string;
    is_user_key: boolean;
  }) {
    for (const [key, value] of Object.entries(apiCredentials)) {
      this.cookieService.set(key, value as string);
    }
  }

  private clearCookieCredentials(): void {
    this.cookieService.delete('celonis_url');
    this.cookieService.delete('celonis_key');
    this.cookieService.delete('is_user_key');
  }

  private exactLengthValidator(requiredLength: number) {
    return (control: AbstractControl): ValidationErrors | null => {
      const actualLength = control.value.length;
      return actualLength != requiredLength
        ? {
            exactLength: {
              requiredLength: requiredLength,
              actualLength: actualLength,
            },
          }
        : null;
    };
  }
}
