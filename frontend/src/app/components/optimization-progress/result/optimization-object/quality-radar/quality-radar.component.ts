import {
  AfterViewInit,
  Component,
  ElementRef,
  Input,
  OnInit,
  ViewChild,
} from '@angular/core';
import { Qualities } from 'src/app/shared/interfaces/qualities';
import Chart from 'chart.js/auto';
import { TooltipItem } from 'chart.js';
import { colors } from 'src/app/shared/misc/colors';

@Component({
  selector: 'app-quality-radar',
  templateUrl: './quality-radar.component.html',
  styleUrls: ['./quality-radar.component.scss'],
})
export class QualityRadarComponent implements OnInit, AfterViewInit {
  @Input()
  public qualities?: Qualities;

  @ViewChild('qualityRadar')
  private radarChartRef?: ElementRef;

  constructor() {}

  ngOnInit(): void {}

  ngAfterViewInit(): void {
    if (this.qualities) {
      const datasets = [
        {
          label: 'Best Iteration',
          data: Object.entries(this.qualities)
            .filter(([qm, value]) => qm != 'overall')
            .map(([qm, value]) => value),
          borderColor: colors.primary(1),
          backgroundColor: colors.primary(0.3),
        },
        {
          label: 'Overall',
          data: Array(Object.keys(this.qualities).length - 1).fill(
            this.qualities.overall
          ),
        },
      ];

      const data = {
        labels: Object.keys(this.qualities)
          .filter((qm) => qm != 'overall')
          .map((label) => label.split(',')),
        datasets: datasets,
      };

      const options = {
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          },
          tooltip: {
            callbacks: {
              title: function (context: TooltipItem<any>[]) {
                return 'Best Iteration';
              },
              label: function (context: TooltipItem<any>) {
                const prefix =
                  context.dataset.label == 'Overall'
                    ? 'Quality Measure Average'
                    : context.label;
                return `${prefix}: ${context.formattedValue}`;
              },
            },
          },
        },
        elements: {
          line: {
            borderWidth: 3,
          },
        },
        scales: {
          r: {
            min: 0,
            max: 1,
            ticks: { stepSize: 0.2 },
          },
        },
      };

      new Chart(this.radarChartRef!.nativeElement, {
        type: 'radar',
        data: data,
        options: options,
      });
    }
  }
}
