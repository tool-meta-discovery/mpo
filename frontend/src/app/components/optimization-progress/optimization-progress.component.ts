import { Component, OnInit } from '@angular/core';
import { interval, Subject, Subscription } from 'rxjs';
import { OptimizationService } from 'src/app/services/optimization.service';
import { OptimizationStatus } from 'src/app/shared/misc/optimization-status';

@Component({
  selector: 'app-optimization-progress',
  templateUrl: './optimization-progress.component.html',
  styleUrls: ['./optimization-progress.component.scss'],
})
export class OptimizationProgressComponent implements OnInit {
  public autoload: boolean = false;
  private autoloadSubscription?: Subscription;

  public readonly optimizationStatus = OptimizationStatus;

  public optimizationTimeSubject: Subject<string>;
  public optimizationStatusSubject: Subject<OptimizationStatus>;
  public fetchingResultsSubject: Subject<boolean>;

  constructor(private optimizationService: OptimizationService) {
    this.optimizationTimeSubject =
      this.optimizationService.optimizationTimeSubject;
    this.optimizationStatusSubject =
      this.optimizationService.optimizationStatusSubject;
    this.fetchingResultsSubject =
      this.optimizationService.fetchingResultsSubject;
    this.optimizationStatusSubject.subscribe((status) => {
      if (status != OptimizationStatus.Running) {
        this.stopAutoloading();
      }
    });
  }

  ngOnInit(): void {}

  public onFetchResults() {
    let updateTimer = true;
    this.optimizationStatusSubject.subscribe((status) => {
      updateTimer = status == this.optimizationStatus.Running;
    });
    this.stopAutoloading();
    this.optimizationService.getResults(updateTimer);
  }

  public onAutoloadChange() {
    if (this.autoload)
      this.autoloadSubscription = interval(60000).subscribe(() =>
        this.optimizationService.getResults()
      );
    else this.stopAutoloading();
  }

  private stopAutoloading() {
    this.autoload = false;
    this.autoloadSubscription?.unsubscribe();
  }

  public onStop(): void {
    this.stopAutoloading();
    this.optimizationService.stopOptimization();
    this.optimizationService.getResults(false);
  }
}
