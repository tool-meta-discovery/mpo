import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'app-model-dialog',
  templateUrl: './model-dialog.component.html',
  styleUrls: ['./model-dialog.component.scss'],
})
export class ModelDialogComponent implements OnInit {
  constructor(@Inject(MAT_DIALOG_DATA) public data: { model: string }) {}

  ngOnInit(): void {}
}
