import { FormArray, FormControl, FormGroup } from '@angular/forms';
import { Type } from 'class-transformer';
import 'reflect-metadata';
import { IntegralParameter } from './integral-parameter';
import { NumericParameter } from './numeric-parameter';
import { ParameterBase } from './parameter-base';
import { ParameterType } from './parameter-type';
import { SelectionParameter } from './selection-parameter';
import { TimeParameter } from './time-parameter';

export class StageObject {
  public name!: string;
  public description!: string;
  @Type(() => ParameterBase, {
    discriminator: {
      property: 'type',
      subTypes: [
        { value: IntegralParameter, name: ParameterType.integral },
        { value: NumericParameter, name: ParameterType.numeric },
        { value: TimeParameter, name: ParameterType.time },
        { value: SelectionParameter, name: ParameterType.selection },
      ],
    },
  })
  public parameters!: ParameterBase<any>[];

  public toParameterFormArray(): FormArray {
    return new FormArray(
      this.parameters.map((param) => param.toFormGroup())
    ) as FormArray;
  }
}
