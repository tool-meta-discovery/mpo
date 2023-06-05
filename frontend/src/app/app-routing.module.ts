import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ColumnSelectionComponent } from './components/log-management/local-log-import/column-selection/column-selection.component';
import { OptimizationProgressComponent } from './components/optimization-progress/optimization-progress.component';
import { PipelineComponent } from './components/pipeline/pipeline.component';
import { WelcomeComponent } from './components/welcome/welcome.component';

const routes: Routes = [
  { path: '', component: WelcomeComponent },
  { path: 'parameter-selection', component: PipelineComponent },
  { path: 'results', component: OptimizationProgressComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
