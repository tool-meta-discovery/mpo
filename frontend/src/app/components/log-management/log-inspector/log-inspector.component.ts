import {
  AfterViewInit,
  Component,
  Inject,
  OnInit,
  ViewChild,
} from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import { EventLog } from 'src/app/shared/interfaces/event-log';

@Component({
  selector: 'app-log-inspector',
  templateUrl: './log-inspector.component.html',
  styleUrls: ['./log-inspector.component.scss'],
})
export class LogInspectorComponent implements OnInit, AfterViewInit {
  public columns: string[];
  public rows: object[];

  public dataSource: MatTableDataSource<any>;

  @ViewChild(MatPaginator) private paginator!: MatPaginator;

  constructor(@Inject(MAT_DIALOG_DATA) public logHead: EventLog['head']) {
    this.rows = logHead;
    this.columns = Object.keys(logHead[0]);
    this.dataSource = new MatTableDataSource<any>(this.rows);
  }

  ngOnInit(): void {}

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
  }
}
