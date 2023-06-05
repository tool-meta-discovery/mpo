import { IntervallParameterBase } from './intervall-parameter-base';
import { ParameterType } from './parameter-type';

export class IntegralParameter extends IntervallParameterBase<number> {
  override controlType = 'number-textbox';
  override type = ParameterType.integral;
}
