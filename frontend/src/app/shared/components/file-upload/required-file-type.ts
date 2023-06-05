import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';

export function requiredFileType(type: string): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const file = control.value;
    if (file) {
      const splitFileName = file.name.split('.');
      const extension =
        '.' + splitFileName[splitFileName.length - 1].toLowerCase();
      if (
        !type
          .split(',')
          .map((type) => type.toLowerCase())
          .includes(extension.toLowerCase())
      ) {
        return {
          requiredFileType: true,
        };
      }

      return null;
    }

    return null;
  };
}
