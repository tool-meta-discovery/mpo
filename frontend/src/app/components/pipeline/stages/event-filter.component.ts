import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { EventFilterService } from 'src/app/services/stage-data/event-filter.service';
import { StageBase } from './stage-base';

@Component({
  selector: 'app-event-filter',
  templateUrl: './stage.html',
  styleUrls: ['./stage.scss'],
})
export class EventFilterComponent extends StageBase implements OnInit {
  constructor(
    private eventFilterService: EventFilterService,
    private formBuilder: FormBuilder
  ) {
    super(eventFilterService, formBuilder);
  }

  // has to be implemented in Childs, as Angular Lifecycle Methods do not work properply with inheritance
  ngOnInit(): void {}
}
