import {
  Exclude,
  Expose,
  Transform,
  TransformationType,
  Type,
} from 'class-transformer';
import * as moment from 'moment';
import { Moment } from 'moment';
import { IntervallParameterBase } from './intervall-parameter-base';
import { ParameterType } from './parameter-type';

const format: string = 'YYYY-MM-DD HH:mm:ss.SSSSSS';
export class TimeParameter extends IntervallParameterBase<Moment> {
  override controlType = 'datetimepicker';
  override type = ParameterType.time;

  @Expose({ name: 'lower_bound' })
  @Transform(({ value, key, obj, type }) => {
    if (type == TransformationType.CLASS_TO_PLAIN) return value.format(format);
    if (type == TransformationType.PLAIN_TO_CLASS) return moment(value);
    else return value;
  })
  override minValue!: Moment;

  @Expose({ name: 'upper_bound' })
  @Transform(({ value, key, obj, type }) => {
    if (type == TransformationType.CLASS_TO_PLAIN) return value.format(format);
    if (type == TransformationType.PLAIN_TO_CLASS) return moment(value);
    else return value;
  })
  override maxValue!: Moment;

  @Expose({ name: 'start_value' })
  @Transform(({ value, key, obj, type }) => {
    if (type == TransformationType.CLASS_TO_PLAIN) return value.format(format);
    if (type == TransformationType.PLAIN_TO_CLASS) return moment(value);
    else return value;
  })
  override startValue!: Moment;

  // @Expose()
  // get lower_bound() {
  //   return this.minValue.format(this.format);
  // }

  // @Expose()
  // get upper_bound() {
  //   return this.minValue.format(this.format);
  // }

  // @Expose()
  // get start_value() {
  //   return this.minValue.format(this.format);
  // }
}
