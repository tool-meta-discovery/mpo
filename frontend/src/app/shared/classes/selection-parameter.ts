import { FormControl, FormGroup } from '@angular/forms';
import { Exclude, Expose, Type } from 'class-transformer';
import { ParameterBase } from './parameter-base';
import { ParameterType } from './parameter-type';

export class SelectionParameter extends ParameterBase<string> {
  constructor(
    startValue: string,
    selectionSet: string[],
    name: string,
    description: string,
    controlType?: string,
    type?: string
  ) {
    super(startValue, name, description, controlType, type);
    this.selectionSet = selectionSet;
  }

  override controlType = 'dropdown';
  override type = ParameterType.selection;

  public override toFormGroup(): FormGroup {
    const fg = super.toFormGroup();
    fg.addControl('selectionSet', new FormControl(this.selectionSet));
    return fg;
  }

  @Exclude()
  isValid(): boolean {
    return this.startValue in this.selectionSet!;
  }
}
