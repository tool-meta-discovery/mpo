import {
  AfterViewInit,
  Component,
  ElementRef,
  Input,
  OnInit,
  ViewChild,
} from '@angular/core';
import { colors } from 'src/app/shared/misc/colors';
import { Iteration } from 'src/app/shared/interfaces/iteration';
import Chart from 'chart.js/auto';

@Component({
  selector: 'app-quality-chart',
  templateUrl: './quality-chart.component.html',
  styleUrls: ['./quality-chart.component.scss'],
})
export class QualityChartComponent implements OnInit, AfterViewInit {
  @Input()
  public optimizationObject: Iteration[] = [];

  @ViewChild('qualityChart')
  private lineChartRef?: ElementRef;

  constructor() {}

  ngOnInit(): void {}

  ngAfterViewInit(): void {
    const datasets = Object.keys(this.optimizationObject[0].quality)
      .filter((qm) => qm != 'overall')
      .map((qm, index) => {
        return {
          label: qm,
          data: this.optimizationObject.map((o) => o.quality[qm]),
          borderColor: colors.palette[index + 1],
        };
      });
    datasets.push({
      label: 'Overall',
      data: this.optimizationObject.map((o) => o.quality.overall),
      borderColor: colors.palette[0],
    });

    const data = {
      labels: [...Array(this.optimizationObject.length).keys()].map(
        (index) => index + 1
      ),
      datasets: datasets,
    };

    new Chart(this.lineChartRef!.nativeElement, {
      type: 'line',
      data: data,
      options: {
        maintainAspectRatio: false,
        responsive: true,
      },
    });
  }
}
