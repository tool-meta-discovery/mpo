import { Component, OnInit } from '@angular/core';
import { Subject } from 'rxjs';
import { OptimizationService } from 'src/app/services/optimization.service';
import { Iteration } from 'src/app/shared/interfaces/iteration';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.scss'],
})
export class ResultComponent implements OnInit {
  public fetchingResultsSubject: Subject<boolean>;
  public optimizationObjectsSubject: Subject<Iteration[][]>;

  constructor(private optimizationService: OptimizationService) {
    this.optimizationObjectsSubject =
      this.optimizationService.optimizationObjectsSubject;
    this.fetchingResultsSubject =
      this.optimizationService.fetchingResultsSubject;
  }

  ngOnInit(): void {}
}
