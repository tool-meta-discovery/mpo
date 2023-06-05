import { Component, Input, OnInit } from '@angular/core';
import { Iteration } from 'src/app/shared/interfaces/iteration';

@Component({
  selector: 'app-parameter-table',
  templateUrl: './parameter-table.component.html',
  styleUrls: ['./parameter-table.component.scss'],
})
export class ParameterTableComponent implements OnInit {
  @Input()
  public iteration?: Iteration;

  constructor() {}

  ngOnInit(): void {}
}
