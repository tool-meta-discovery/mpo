import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { TraceFilterService } from 'src/app/services/stage-data/trace-filter.service';
import { StageBase } from './stage-base';

@Component({
  selector: 'app-trace-filter',
  templateUrl: './stage.html',
  styleUrls: ['./stage.scss'],
})
export class TraceFilterComponent extends StageBase implements OnInit {
  public override hideBackButton: boolean = true;

  constructor(
    private traceFilterService: TraceFilterService,
    private formBuilder: FormBuilder
  ) {
    super(traceFilterService, formBuilder);
  }

  // has to be implemented in Childs, as Angular Lifecycle Methods do not work properply with inheritance
  ngOnInit(): void {}
}
