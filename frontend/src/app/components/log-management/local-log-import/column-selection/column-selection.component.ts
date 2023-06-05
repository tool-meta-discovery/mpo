import {
  Component,
  Input,
  OnChanges,
  OnInit,
  SimpleChanges,
} from '@angular/core';
import { AbstractControl, ValidationErrors, Validators } from '@angular/forms';
import { EventLogService } from 'src/app/services/eventlog.service';
import { FormBuilder } from '@angular/forms';
import { filter, Observable, Subject, throwError } from 'rxjs';
import { Router } from '@angular/router';

@Component({
  selector: 'app-column-selection',
  templateUrl: './column-selection.component.html',
  styleUrls: ['./column-selection.component.scss'],
})
export class ColumnSelectionComponent implements OnInit, OnChanges {
  @Input('loading')
  public loading: boolean = false;
  public eventLogColumnsSubject: Subject<string[]>;
  public readonly columnSelectionForm = this.fb.group(
    {
      case: ['', Validators.required],
      time: ['', Validators.required],
      activity: ['', Validators.required],
    },
    { validators: [this.exclusiveSelectionValidator] }
  );

  get notLoading() {
    return !this.loading;
  }

  constructor(
    private eventLogService: EventLogService,
    private fb: FormBuilder
  ) {
    this.eventLogColumnsSubject = this.eventLogService.eventLogColumnsSubject;
    this.eventLogColumnsSubject.subscribe(console.log);
  }

  ngOnInit(): void {}

  ngOnChanges(changes: SimpleChanges): void {
    if (this.loading) this.columnSelectionForm.disable();
    else this.columnSelectionForm.enable();
  }

  public onSubmit(): Observable<string> {
    if (this.columnSelectionForm.valid) {
      return this.eventLogService.sendSelectedColumns(
        this.columnSelectionForm.value
      );
    } else return throwError(() => new Error('Column Selection is invalid.'));
  }

  private exclusiveSelectionValidator(
    control: AbstractControl
  ): ValidationErrors | null {
    if (
      control.value.case == '' ||
      control.value.activity == '' ||
      control.value.time == ''
    )
      return null;
    if (
      control.value.case != control.value.activity &&
      control.value.activity != control.value.time &&
      control.value.case != control.value.time
    )
      return null;
    else return { exclusiveSelection: true };
  }
}
