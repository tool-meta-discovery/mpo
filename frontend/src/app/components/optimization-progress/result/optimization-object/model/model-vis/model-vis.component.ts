import {
  AfterViewInit,
  Component,
  ElementRef,
  Input,
  OnInit,
  ViewChild,
} from '@angular/core';
import { BaseType } from 'd3';
import { Graphviz, graphviz } from 'd3-graphviz';

@Component({
  selector: 'app-model-vis',
  templateUrl: './model-vis.component.html',
  styleUrls: ['./model-vis.component.scss'],
})
export class ModelVisComponent implements OnInit, AfterViewInit {
  public loading: boolean = true;
  public graphvizId: string = `model-${Math.random().toString().slice(2, 5)}`;

  @Input()
  public model: string = '';

  @ViewChild('modelView')
  public modelView?: ElementRef;

  private width: number = 500;
  private height: number = 250;

  private graph?: Graphviz<BaseType, any, BaseType, any>;

  constructor() {}

  ngOnInit(): void {}

  ngAfterViewInit(): void {
    if (this.modelView) {
      this.height = this.modelView.nativeElement.offsetHeight;
      this.width = this.modelView.nativeElement.offsetWidth;
    }

    this.graph = graphviz(`#${this.graphvizId}`)
      .width(this.width)
      .height(this.height)
      .fit(true)
      .renderDot(this.model, () => (this.loading = false));
  }

  public resetZoom() {
    this.graph?.resetZoom();
  }
}
