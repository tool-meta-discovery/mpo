import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { QualityMeasureService } from 'src/app/services/stage-data/quality-measure.service';
import { StageBase } from './stage-base';

@Component({
  selector: 'app-quality-measure',
  templateUrl: './stage.html',
  styleUrls: ['./stage.scss'],
})
export class QualityMeasureComponent extends StageBase implements OnInit {
  constructor(
    private qualityMeasureService: QualityMeasureService,
    private formBuilder: FormBuilder
  ) {
    super(qualityMeasureService, formBuilder);
  }

  // has to be implemented in Childs, as Angular Lifecycle Methods do not work properply with inheritance
  ngOnInit(): void {}
}
