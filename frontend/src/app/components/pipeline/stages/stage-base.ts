import { Component, ViewChild } from '@angular/core';
import { FormArray, FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { MatCheckboxChange } from '@angular/material/checkbox';
import { MatAccordion, MatExpansionPanel } from '@angular/material/expansion';
import { instanceToPlain, plainToInstance } from 'class-transformer';
import { BehaviorSubject, Subject } from 'rxjs';
import { StageServiceBase } from 'src/app/services/stage-data/stage-service-base';
import { ParameterBase } from 'src/app/shared/classes/parameter-base';
import { StageObject } from 'src/app/shared/classes/stage-object';

@Component({
  template: '',
})
export abstract class StageBase {
  public hideBackButton: boolean = false;
  public readonly stageName: string;
  public readonly loadingSubject: Subject<boolean> =
    new BehaviorSubject<boolean>(false);

  @ViewChild(MatAccordion) accordion?: MatAccordion;

  stageObjectsForm: FormGroup = new FormGroup({
    stageObjects: new FormArray([
      new FormGroup({
        selected: new FormControl([false]),
        parameters: new FormArray([]),
      }),
    ]),
  });

  get stageObjectsFormArray() {
    return this.stageObjectsForm.get('stageObjects') as FormArray;
  }

  parameterFormArray(stageObjectIndex: number) {
    return this.stageObjectsFormArray
      .at(stageObjectIndex)
      .get('parameters') as FormArray;
  }

  parameterForm(stageObjectIndex: number, parameterIndex: number) {
    return this.parameterFormArray(stageObjectIndex).at(
      parameterIndex
    ) as FormGroup;
  }

  originalStageObjects: StageObject[] = [];
  modifiedStageObjects: StageObject[] = [];

  constructor(private stageService: StageServiceBase, private fb: FormBuilder) {
    this.stageName = stageService.stageName;
    this.stageService
      .getStageObjects()
      .subscribe((stageObjects: StageObject[]) => {
        this.originalStageObjects = stageObjects.map((stageObject) =>
          plainToInstance(StageObject, instanceToPlain(stageObject))
        ); // Creating deep-copy

        this.modifiedStageObjects = stageObjects;
        this.stageObjectsFormArray.clear();
        stageObjects.forEach((stageObject: StageObject) => {
          this.stageObjectsFormArray.push(
            this.fb.group({
              selected: [false],
              parameters: stageObject.toParameterFormArray(),
            })
          );
        });
      });
    this.loadingSubject = this.stageService.loadingSubject;
  }

  selectAll() {
    this.stageObjectsFormArray.controls.forEach((control) => {
      control.patchValue({ selected: true });
    });
  }
  unselectAll() {
    if (this.accordion) this.accordion.closeAll();
    this.stageObjectsFormArray.controls.forEach((control) => {
      control.patchValue({ selected: false });
    });
  }

  onCheck(change: MatCheckboxChange, panel: MatExpansionPanel) {
    if (change.checked) {
      panel.open();
    } else {
      panel.close();
    }
  }

  onParameterUpdate(
    parameter: ParameterBase<any>,
    stageObjectIndex: number,
    parameterIndex: number
  ) {
    this.modifiedStageObjects[stageObjectIndex].parameters[parameterIndex] =
      parameter;
  }

  onSubmit() {
    const selectedList = this.stageObjectsFormArray.value.map(
      (val: { selected: boolean; parameters: any[] }) => val.selected
    );
    this.stageService
      .sendStageObjects(
        this.modifiedStageObjects.filter((_, index) => selectedList[index])
      )
      .subscribe();
  }
}
