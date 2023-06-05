import { Component, Input, OnInit } from '@angular/core';
import { Iteration } from 'src/app/shared/interfaces/iteration';

@Component({
  selector: 'app-history',
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.scss'],
})
export class HistoryComponent implements OnInit {
  @Input()
  public optimizationObject: Iteration[] = [];

  constructor() {}

  ngOnInit(): void {}
}
