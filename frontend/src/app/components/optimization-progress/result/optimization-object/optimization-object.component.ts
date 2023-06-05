import { Component, Input, OnInit, ViewEncapsulation } from '@angular/core';
import { Iteration } from 'src/app/shared/interfaces/iteration';

@Component({
  selector: 'app-optimization-object',
  templateUrl: './optimization-object.component.html',
  styleUrls: ['./optimization-object.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class OptimizationObjectComponent implements OnInit {
  @Input()
  public rank: number = 0;

  @Input()
  public optimizationObject: Iteration[] = [];

  constructor() {}

  ngOnInit(): void {}

  get bestIteration() {
    return this.optimizationObject.reduce((bestIteration, currIteration) => {
      return bestIteration.quality.overall > currIteration.quality.overall
        ? bestIteration
        : currIteration;
    });
  }

  get bestIterationIndex() {
    return this.optimizationObject.reduce(
      (bestIterationIndex, currIteration, currIterationIndex) => {
        return this.optimizationObject[bestIterationIndex].quality.overall >
          currIteration.quality.overall
          ? bestIterationIndex
          : currIterationIndex;
      },
      0
    );
  }

  get qualityMeasureCount() {
    return Object.keys(this.bestIteration.quality).length - 1; // minus 1 for overall key
  }
}
