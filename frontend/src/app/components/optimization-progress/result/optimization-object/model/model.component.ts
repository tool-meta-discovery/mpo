import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { environment } from 'src/environments/environment';
import { ModelDialogComponent } from './model-dialog/model-dialog.component';
import { ModelVisComponent } from './model-vis/model-vis.component';

@Component({
  selector: 'app-model',
  templateUrl: './model.component.html',
  styleUrls: ['./model.component.scss'],
})
export class ModelComponent implements OnInit {
  @Input()
  public model: string = '';
  @Input()
  public pnmlDownloadUrl: string = '';
  @Input()
  public bpmnDownloadUrl: string = '';
  @ViewChild(ModelVisComponent)
  public modelVisComponent?: ModelVisComponent;

  constructor(private dialog: MatDialog) {}

  ngOnInit(): void {}

  onPnmlDownload() {
    window.open(`${environment.backendUrl}/${this.pnmlDownloadUrl}`, '_blank');
  }
  onBpmnDownload() {
    window.open(`${environment.backendUrl}/${this.bpmnDownloadUrl}`, '_blank');
  }
  onFullscreen() {
    this.dialog.open(ModelDialogComponent, {
      data: { model: this.model },
      width: '95%',
      height: '95%',
    });
  }
  onZoomReset() {
    this.modelVisComponent?.resetZoom();
  }
}
