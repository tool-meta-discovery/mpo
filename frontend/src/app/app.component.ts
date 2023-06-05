import { Component } from '@angular/core';
import { wasmFolder } from '@hpcc-js/wasm';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  title = 'meta-parameter-optimizer';

  constructor() {
    wasmFolder('assets/@hpcc-js/wasm/dist/');
  }
}
