import { IntervallParameterBase } from './intervall-parameter-base';
import { ParameterType } from './parameter-type';

export class NumericParameter extends IntervallParameterBase<number> {
  override controlType = 'number-textbox';
  override type = ParameterType.numeric;
}
