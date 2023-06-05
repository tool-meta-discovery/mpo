import { Injectable } from '@angular/core';
import { FormControl, Validators, FormGroup } from '@angular/forms';
import { ParameterBase } from '../shared/classes/parameter-base';

@Injectable({
  providedIn: 'root',
})
export class ParameterControlServiceService {
  constructor() {}
  toFormGroup(parameters: ParameterBase<any>[]) {
    const group: any = {};

    //TODO RIGHT NOW
    parameters.forEach((parameter) => {
      switch (obj.type) {
        case 'integral':
          group[parameter.name] = new FormControl(
            parameter.startValue || '',
            Validators.required
          );
          break;
        case 'numeric':
          group[parameter.name] = new FormControl(
            parameter.startValue || '',
            Validators.required
          );
          break;
        case 'datetime':
          group[parameter.name] = new FormControl(
            parameter.startValue || '',
            Validators.required
          );
          break;
        case 'selection':
          group[parameter.name] = new FormControl(
            parameter.startValue || '',
            Validators.required
          );
          break;
        default:
          group[parameter.name] = new FormControl(
            parameter.startValue || '',
            Validators.required
          );
      }
    });
    return new FormGroup(group);
  }
}
