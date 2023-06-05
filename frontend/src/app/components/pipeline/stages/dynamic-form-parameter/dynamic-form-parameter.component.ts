import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { instanceToPlain, plainToInstance } from 'class-transformer';
import { IntegralParameter } from 'src/app/shared/classes/integral-parameter';
import { NumericParameter } from 'src/app/shared/classes/numeric-parameter';
import { ParameterBase } from 'src/app/shared/classes/parameter-base';
import { ParameterType } from 'src/app/shared/classes/parameter-type';
import { SelectionParameter } from 'src/app/shared/classes/selection-parameter';
import { TimeParameter } from 'src/app/shared/classes/time-parameter';

@Component({
  selector: 'app-dynamic-form-parameter',
  templateUrl: './dynamic-form-parameter.component.html',
  styleUrls: ['./dynamic-form-parameter.component.scss'],
})
export class DynamicFormParameterComponent implements OnInit {
  @Input() parameter!: ParameterBase<any>;
  @Input() form!: FormGroup;
  @Output() parameterUpdate = new EventEmitter<ParameterBase<any>>();

  public maximalSelectionSet?: string[];

  get isValid() {
    return true;
    // return this.form.controls[this.parameter.name].valid;
  }

  constructor() {}

  ngOnInit(): void {
    switch (this.parameter.type) {
      case ParameterType.integral:
        break;
      case ParameterType.numeric:
        break;
      case ParameterType.time:
        break;
      case ParameterType.selection:
        this.maximalSelectionSet = this.parameter.selectionSet;
        break;
    }

    this.form.valueChanges.subscribe((change) => {
      const newValues = instanceToPlain(this.parameter);
      switch (this.parameter.type) {
        case ParameterType.integral:
        case ParameterType.numeric:
          newValues['lower_bound'] = change.minValue;
          newValues['upper_bound'] = change.maxValue;
          newValues['start_value'] = change.startValue;
          break;
        case ParameterType.time:
          newValues['lower_bound'] = change.minValue;
          newValues['upper_bound'] = change.maxValue;
          newValues['start_value'] = change.startValue;
          newValues['lower_bound'].startOf('day');
          newValues['upper_bound'].startOf('day');
          newValues['start_value'].endOf('day');
          newValues['lower_bound'] = newValues['lower_bound'].format();
          newValues['upper_bound'] = newValues['upper_bound'].format();
          newValues['start_value'] = newValues['start_value'].format();
          break;
        case ParameterType.selection:
          newValues['start_value'] = change.startValue;
          newValues['selection_set'] = change.selectionSet;
          break;
        default:
          break;
      }

      switch (this.parameter.type) {
        case ParameterType.integral:
          this.parameterUpdate.emit(
            plainToInstance(IntegralParameter, newValues)
          );
          break;
        case ParameterType.numeric:
          this.parameterUpdate.emit(
            plainToInstance(NumericParameter, newValues)
          );
          break;
        case ParameterType.time:
          this.parameterUpdate.emit(plainToInstance(TimeParameter, newValues));
          break;
        case ParameterType.selection:
          this.parameterUpdate.emit(
            plainToInstance(SelectionParameter, newValues)
          );
          break;
        default:
          break;
      }
    });
  }
}
