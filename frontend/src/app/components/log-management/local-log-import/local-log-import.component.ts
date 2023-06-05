import { Component, OnInit, ViewChild } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { ColumnSelectionComponent } from './column-selection/column-selection.component';

@Component({
  selector: 'app-local-log-import',
  templateUrl: './local-log-import.component.html',
  styleUrls: ['./local-log-import.component.scss'],
})
export class LocalLogImportComponent implements OnInit {
  @ViewChild('columnSelection')
  columnSelection: ColumnSelectionComponent | undefined;
  public loading: boolean = false;

  constructor(private dialogRef: MatDialogRef<LocalLogImportComponent>) {}

  ngOnInit(): void {}

  public onImport() {
    this.loading = true;
    this.columnSelection?.onSubmit().subscribe(() => {
      this.loading = false;
      this.dialogRef.close();
    });
  }
}
