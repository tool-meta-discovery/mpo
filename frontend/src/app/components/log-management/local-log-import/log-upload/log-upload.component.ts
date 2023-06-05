import { Component, Input, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatStepper } from '@angular/material/stepper';
import { EventLogService } from 'src/app/services/eventlog.service';
import { requiredFileType } from 'src/app/shared/components/file-upload/required-file-type';

@Component({
  selector: 'app-log-upload',
  templateUrl: './log-upload.component.html',
  styleUrls: ['./log-upload.component.scss'],
})
export class LogUploadComponent implements OnInit {
  @Input()
  public stepper: MatStepper | undefined;
  public acceptedFileType: string = '.xes,.csv';
  public loading: boolean = false;
  public readonly uploadForm: FormGroup = this.fb.group({
    file: ['', [Validators.required, requiredFileType(this.acceptedFileType)]],
    separator: [
      ';',
      [Validators.required, Validators.maxLength(1), Validators.minLength(1)],
    ],
  });

  constructor(
    private eventLogService: EventLogService,
    private fb: FormBuilder
  ) {}

  ngOnInit(): void {
    this.uploadForm.valueChanges.subscribe(() => {
      if (this.stepper) {
        this.stepper!.selected!.completed = false;
      }
    });
  }

  onSubmit() {
    if (this.uploadForm.dirty) {
      this.uploadForm.disable();
      this.uploadForm.markAsPristine();
      this.loading = true;
      this.eventLogService
        .sendEventLog(
          this.uploadForm.value.file,
          this.uploadForm.value.separator
        )
        .subscribe({
          complete: () => {
            this.loading = false;
            if (this.stepper) {
              this.stepper!.selected!.completed = true;
              this.stepper.next();
            }
            this.uploadForm.enable();
          },
        });
    } else {
      if (this.stepper) {
        this.stepper!.selected!.completed = true;
        this.stepper.next();
      }
    }
  }
}
