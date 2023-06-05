import { NgModule } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { MaterialModule } from './material.module';
import { MatIconRegistry } from '@angular/material/icon';
@NgModule({
  imports: [MaterialModule],
})
export class IconModule {
  private path: string = '../../assets/images';
  constructor(
    private domSanitizer: DomSanitizer,
    public matIconRegistry: MatIconRegistry
  ) {
    this.matIconRegistry.addSvgIcon(
      'celonis',
      this.setPath(`${this.path}/celonis.svg`)
    );
  }
  private setPath(url: string): SafeResourceUrl {
    return this.domSanitizer.bypassSecurityTrustResourceUrl(url);
  }
}
