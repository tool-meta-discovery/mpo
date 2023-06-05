import * as moment from 'moment';
import { Component, OnInit } from '@angular/core';
import { EventFilterService } from 'src/app/services/stage-data/event-filter.service';
import { TraceFilterService } from 'src/app/services/stage-data/trace-filter.service';
import {
  finalize,
  forkJoin,
  interval,
  mergeMap,
  Subject,
  Subscription,
} from 'rxjs';
import { DiscoveryAlgorithmService } from 'src/app/services/stage-data/discovery-algorithm.service';
import { QualityMeasureService } from 'src/app/services/stage-data/quality-measure.service';
import { StageServiceBase } from 'src/app/services/stage-data/stage-service-base';
import { OptimizationService } from 'src/app/services/optimization.service';

import { EventLogService } from 'src/app/services/eventlog.service';
import { EventLog } from 'src/app/shared/interfaces/event-log';
import { Router } from '@angular/router';

@Component({
  selector: 'app-selection',
  templateUrl: './pipeline.component.html',
  styleUrls: ['./pipeline.component.scss'],
})
export class PipelineComponent implements OnInit {
  public selectedEventLogSubject: Subject<EventLog>;
  public optimizationLimitMinutes: number = 10;

  public loading: boolean = false;

  constructor(
    private optimizationService: OptimizationService,
    private eventLogService: EventLogService,
    private router: Router
  ) {
    this.selectedEventLogSubject = this.eventLogService.selectedEventLogSubject;
  }

  ngOnInit(): void {}

  public onStart(): void {
    this.loading = true;
    this.optimizationService
      .startOptimization(this.optimizationLimitMinutes * 60)
      .pipe(
        finalize(() => {
          this.loading = false;
        })
      )
      .subscribe(() => {
        this.router.navigateByUrl('/results');
      });
  }
}
