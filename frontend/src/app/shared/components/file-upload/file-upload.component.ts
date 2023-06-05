import { Component, ElementRef, HostListener, Input } from '@angular/core';
import { ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';

@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.scss'],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: FileUploadComponent,
      multi: true,
    },
  ],
})
export class FileUploadComponent implements ControlValueAccessor {
  @Input()
  public acceptedType: string = '';
  private onChange: Function | undefined;
  public file: File | null = null;
  public disabled: boolean = false;

  @HostListener('change', ['$event.target.files']) emitFiles(event: FileList) {
    const file = event && event.item(0);
    if (this.onChange) this.onChange(file);
    this.file = file;
  }

  constructor(private host: ElementRef<HTMLInputElement>) {}

  writeValue(_value: null): void {
    // clear file input
    this.host.nativeElement.value = '';
    this.file = null;
  }
  registerOnChange(fn: Function): void {
    this.onChange = fn;
  }
  registerOnTouched(_fn: Function): void {}

  setDisabledState(isDisabled: boolean) {
    this.disabled = isDisabled;
  }
}
