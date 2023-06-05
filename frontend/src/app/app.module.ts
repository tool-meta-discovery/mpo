// Angular Imports
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { FlexLayoutModule } from '@angular/flex-layout';

// All Angular Material related import grouped in separated module
import { MaterialModule } from './shared/modules/material.module';
import { IconModule } from './shared/modules/icon.module';
import { AppRoutingModule } from './app-routing.module';

// Services
import { HttpInterceptorProviders } from './services/http-interceptors';

// Components
import { AppComponent } from './app.component';
import { WelcomeComponent } from './components/welcome/welcome.component';
import { TopBarComponent } from './components/top-bar/top-bar.component';
import { PipelineComponent } from './components/pipeline/pipeline.component';
import { TraceFilterComponent } from './components/pipeline/stages/trace-filter.component';
import { EventFilterComponent } from './components/pipeline/stages/event-filter.component';
import { DiscoveryAlgorithmComponent } from './components/pipeline/stages/discovery-algorithm.component';
import { QualityMeasureComponent } from './components/pipeline/stages/quality-measure.component';
import { ColumnSelectionComponent } from './components/log-management/local-log-import/column-selection/column-selection.component';
import { LogManagementComponent } from './components/log-management/log-management.component';
import { CelonisLogImportComponent } from './components/log-management/celonis-log-import/celonis-log-import.component';
import { LocalLogImportComponent } from './components/log-management/local-log-import/local-log-import.component';
import { LogUploadComponent } from './components/log-management/local-log-import/log-upload/log-upload.component';
import { FileUploadComponent } from './shared/components/file-upload/file-upload.component';
import { LogInspectorComponent } from './components/log-management/log-inspector/log-inspector.component';
import { ResultComponent } from './components/optimization-progress/result/result.component';
import { OptimizationObjectComponent } from './components/optimization-progress/result/optimization-object/optimization-object.component';
import { HistoryComponent } from './components/optimization-progress/result/optimization-object/history/history.component';
import { ModelComponent } from './components/optimization-progress/result/optimization-object/model/model.component';
import { QualityRadarComponent } from './components/optimization-progress/result/optimization-object/quality-radar/quality-radar.component';
import { QualityChartComponent } from './components/optimization-progress/result/optimization-object/history/quality-chart/quality-chart.component';
import { ModelVisComponent } from './components/optimization-progress/result/optimization-object/model/model-vis/model-vis.component';
import { ModelDialogComponent } from './components/optimization-progress/result/optimization-object/model/model-dialog/model-dialog.component';
import { ParameterTableComponent } from './components/optimization-progress/result/optimization-object/parameter-table/parameter-table.component';
import { OptimizationProgressComponent } from './components/optimization-progress/optimization-progress.component';
import { SettingsComponent } from './components/settings/settings.component';
import { DynamicFormParameterComponent } from './components/pipeline/stages/dynamic-form-parameter/dynamic-form-parameter.component';
import { MAT_DATE_LOCALE } from '@angular/material/core';
import { STEPPER_GLOBAL_OPTIONS } from '@angular/cdk/stepper';
@NgModule({
  declarations: [
    AppComponent,
    WelcomeComponent,
    TopBarComponent,
    PipelineComponent,
    TraceFilterComponent,
    EventFilterComponent,
    DiscoveryAlgorithmComponent,
    QualityMeasureComponent,
    ColumnSelectionComponent,
    LogManagementComponent,
    CelonisLogImportComponent,
    LocalLogImportComponent,
    LogUploadComponent,
    FileUploadComponent,
    LogInspectorComponent,
    ResultComponent,
    OptimizationObjectComponent,
    HistoryComponent,
    ModelComponent,
    QualityRadarComponent,
    QualityChartComponent,
    ModelVisComponent,
    ModelDialogComponent,
    ParameterTableComponent,
    OptimizationProgressComponent,
    SettingsComponent,
    DynamicFormParameterComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    HttpClientModule,
    ReactiveFormsModule,
    FormsModule,
    MaterialModule,
    IconModule,
    FlexLayoutModule,
  ],
  providers: [
    HttpInterceptorProviders,
    { provide: MAT_DATE_LOCALE, useValue: 'de-DE' },
    {
      provide: STEPPER_GLOBAL_OPTIONS,
      useValue: { showError: true },
    },
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
