import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { finalize, Subject } from 'rxjs';
import { EventLogService } from 'src/app/services/eventlog.service';
import { EventLog } from 'src/app/shared/interfaces/event-log';
import { CelonisLogImportComponent } from './celonis-log-import/celonis-log-import.component';
import { LocalLogImportComponent } from './local-log-import/local-log-import.component';
import { LogInspectorComponent } from './log-inspector/log-inspector.component';

@Component({
  selector: 'app-log-management',
  templateUrl: './log-management.component.html',
  styleUrls: ['./log-management.component.scss'],
})
export class LogManagementComponent implements OnInit {
  public eventLogsSubject: Subject<EventLog[]>;
  public loadingSubject: Subject<boolean>;
  public selectingEventLog: boolean = false;
  public selectedLog?: EventLog;
  public displayedColumns: string[] = [
    'name',
    'cases',
    'events',
    'date',
    'actions',
  ];

  constructor(
    private dialog: MatDialog,
    private eventLogService: EventLogService,
    private router: Router
  ) {
    this.loadingSubject = this.eventLogService.loadingLogsSubject;
    this.eventLogsSubject = this.eventLogService.eventLogsSubject;
  }

  ngOnInit(): void {}

  onLogClicked(log: EventLog) {
    this.selectedLog = log;
  }

  onLocalUploadClick() {
    this.dialog.open(LocalLogImportComponent, {
      disableClose: true,
    });
  }

  onCelonisImportClick() {
    this.dialog.open(CelonisLogImportComponent, {
      disableClose: true,
    });
  }

  onLogPreview(log: EventLog) {
    this.dialog.open(LogInspectorComponent, {
      data: log.head,
      maxHeight: '95%',
      maxWidth: '95%',
    });
  }

  onLogSelect() {
    if (this.selectedLog) {
      this.selectingEventLog = true;
      this.eventLogService
        .selectEventLog(this.selectedLog)
        .pipe(
          finalize(() => {
            this.selectingEventLog = false;
          })
        )
        .subscribe(() => this.router.navigateByUrl('/parameter-selection'));
    }
  }

  onLogDelete(log: EventLog) {
    if (this.selectedLog == log) this.selectedLog = undefined;
    this.eventLogService.deleteEventLog(log);
  }
}
