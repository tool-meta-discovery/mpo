import { HttpClient } from '@angular/common/http';
import { instanceToPlain, plainToInstance } from 'class-transformer';
import {
  BehaviorSubject,
  finalize,
  map,
  mergeMap,
  Observable,
  Subject,
} from 'rxjs';
import { StageObject } from 'src/app/shared/classes/stage-object';
import { environment } from 'src/environments/environment';

export abstract class StageServiceBase {
  public abstract readonly stageName: string;
  public abstract baseRoute: string;
  public readonly loadingSubject: Subject<boolean> =
    new BehaviorSubject<boolean>(false);

  constructor(private _http: HttpClient) {}

  sendStageObjects(stageObjects: StageObject[]): Observable<string> {
    return this._http.post<string>(
      `${environment.backendUrl}${this.baseRoute}/set_parameter`,
      instanceToPlain(stageObjects)
    );
  }

  getStageObjects(): Observable<StageObject[]> {
    this.loadingSubject.next(true);
    return this._http
      .get<StageObject[]>(
        `${environment.backendUrl}${this.baseRoute}/get_parameter`
      )
      .pipe(
        map((stageObject: StageObject[]) =>
          stageObject.map((stageObject) => {
            return plainToInstance(StageObject, stageObject);
          })
        ),
        finalize(() => this.loadingSubject.next(false)) // Execute when the observable completes
      );
  }

  // Unused as it breaks some backend logic
  resetStageObjects(): Observable<StageObject[]> {
    this.loadingSubject.next(true);
    return this._http
      .post<string>(`${environment.backendUrl}${this.baseRoute}/reset`, {})
      .pipe(
        mergeMap((_) => this.getStageObjects()),
        finalize(() => this.loadingSubject.next(false)) // Execute when the observable completes
      );
  }
}
