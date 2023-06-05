import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import * as moment from 'moment';
import {
  BehaviorSubject,
  finalize,
  interval,
  map,
  mergeMap,
  Subject,
  Subscription,
  tap,
} from 'rxjs';
import { environment } from 'src/environments/environment';
import { Iteration } from '../shared/interfaces/iteration';
import { OptimizationStatus } from '../shared/misc/optimization-status';

@Injectable({
  providedIn: 'root',
})
export class OptimizationService {
  private optimizationStartDate: moment.Moment = moment();
  private timer: Subscription | undefined;

  public readonly optimizationObjectsSubject: Subject<Iteration[][]> =
    new BehaviorSubject<Iteration[][]>([]);

  public readonly optimizationStatusSubject: Subject<OptimizationStatus> =
    new BehaviorSubject<OptimizationStatus>(OptimizationStatus.NotStarted);

  public readonly optimizationTimeSubject: Subject<string> =
    new BehaviorSubject<string>('has not started yet.');

  public readonly fetchingResultsSubject: Subject<boolean> =
    new BehaviorSubject<boolean>(false);

  constructor(private http: HttpClient) {}

  public startOptimization(timeoutSeconds: number = 600) {
    this.optimizationStartDate = moment();
    this.optimizationTimeSubject.next(
      `started ${this.optimizationStartDate.fromNow()}.`
    );

    this.optimizationStatusSubject.next(OptimizationStatus.Running);

    this.timer = interval(60000).subscribe(() =>
      this.optimizationTimeSubject.next(
        `started ${this.optimizationStartDate.fromNow()}.`
      )
    );

    return this.http
      .post<string>(`${environment.backendUrl}/optimizer/set_timeout`, {
        seconds: timeoutSeconds,
      })
      .pipe(
        mergeMap(() => {
          return this.http.get<string>(
            `${environment.backendUrl}/optimizer/run_optimizer`
          );
        })
      );
  }

  public stopOptimization() {
    this.http
      .get<string>(`${environment.backendUrl}/optimizer/stop_optimizer`)
      .subscribe();
    this.optimizationStatusSubject.next(OptimizationStatus.Stopped);
    this.finishOptimization(true);
  }

  public getResults(updateTimer: boolean = true) {
    this.fetchingResultsSubject.next(true);
    this.http
      .get<{ histories: string[]; finished: boolean }>(
        `${environment.backendUrl}/optimizer/get_result`
      )
      .pipe(
        tap((res) => {
          if (res.finished) {
            this.optimizationStatusSubject.next(OptimizationStatus.Stopped);
            if (updateTimer) this.finishOptimization();
          }
        }),
        map((res) => {
          return res.histories.map((history) => JSON.parse(history));
        }),
        finalize(() => this.fetchingResultsSubject.next(false)) // Execute when the observable completes
      )
      .subscribe({
        next: (res) => this.optimizationObjectsSubject.next(res),
      });
  }

  private finishOptimization(forced: boolean = false) {
    this.timer?.unsubscribe();
    this.optimizationTimeSubject.next(
      `${
        forced ? 'stopped' : 'finished'
      } after ${this.optimizationStartDate.toNow(true)}.`
    );
  }
}
