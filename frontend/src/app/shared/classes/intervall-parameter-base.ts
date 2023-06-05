import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { Exclude, Expose } from 'class-transformer';
import { ParameterBase } from './parameter-base';

export class IntervallParameterBase<T> extends ParameterBase<T> {
  constructor(
    startValue: T,
    minValue: T,
    maxValue: T,
    name: string,
    description: string,
    controlType?: string,
    type?: string
  ) {
    super(startValue, name, description, controlType, type);
    this.minValue = minValue;
    this.maxValue = maxValue;
  }

  public override toFormGroup(): FormGroup {
    const fg = super.toFormGroup();
    fg.addControl('minValue', new FormControl(this.minValue));
    fg.addControl('maxValue', new FormControl(this.maxValue));
    return fg;
  }

  @Exclude()
  isValid(): boolean {
    return (
      this.minValue! <= this.startValue && this.startValue <= this.maxValue!
    );
  }
}
