import { HttpClient, HttpEvent } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { of } from 'rxjs';
import { delay, mergeMap } from 'rxjs/operators';
import { environment } from '../../../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class FileUploadService {
  private apiUrl = environment.depositApiUrl;
  private resourceUrl = 'api/processingrequests/';
  private n = 100;
  private a = new Array(this.n);
  private mockedObservable: Observable<number>;
  constructor(private http: HttpClient) {
    for (let i = 0; i < this.n; ++i) this.a[i] = i;
    this.mockedObservable = of(...this.a);
  }

  public upload(file: File): Observable<any> {
    return this.mockedObservable.pipe(
      mergeMap(value => of(value).pipe(delay(value * 3)))
    );
  }
  uploadFile(
    file: File,
    auto_extract_only: boolean = false
  ): Observable<HttpEvent<any>> {
    console.log('uploading to:', this.apiUrl);
    const formData = new FormData();
    formData.append('files', file, file.name);
    formData.append('auto_extract_only', String(auto_extract_only));
    return this.http.post(`${this.apiUrl}/${this.resourceUrl}`, formData, {
      reportProgress: true,
      observe: 'events',
    });
  }
}
