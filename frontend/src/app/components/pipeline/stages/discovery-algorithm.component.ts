import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { DiscoveryAlgorithmService } from 'src/app/services/stage-data/discovery-algorithm.service';
import { StageBase } from './stage-base';

@Component({
  selector: 'app-discovery-algorithm',
  templateUrl: './stage.html',
  styleUrls: ['./stage.scss'],
})
export class DiscoveryAlgorithmComponent extends StageBase implements OnInit {
  constructor(
    private discoveryAlgorithmService: DiscoveryAlgorithmService,
    private formBuilder: FormBuilder
  ) {
    super(discoveryAlgorithmService, formBuilder);
  }

  // has to be implemented in Childs, as Angular Lifecycle Methods do not work properply with inheritance
  ngOnInit(): void {}
}
