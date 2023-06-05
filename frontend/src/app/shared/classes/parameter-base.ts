import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { Exclude, Expose, Type } from 'class-transformer';

export class ParameterBase<T> {
  @Expose({ name: 'start_value' })
  startValue: T;
  name: string;
  description: string;
  @Exclude()
  controlType?: string;
  type?: string;
  @Expose({ name: 'lower_bound' })
  minValue?: T;
  @Expose({ name: 'upper_bound' })
  maxValue?: T;
  @Expose({ name: 'selection_set' })
  @Type(() => String)
  selectionSet?: string[];

  constructor(
    startValue: T,
    name: string,
    description: string,
    controlType?: string,
    type?: string
  ) {
    this.startValue = startValue;
    this.name = name;
    this.description = description;
    this.controlType = controlType;
    this.type = type;
  }

  public toFormGroup(): FormGroup {
    const fb = new FormBuilder();
    return fb.group({
      startValue: [this.startValue],
    });
  }
}
