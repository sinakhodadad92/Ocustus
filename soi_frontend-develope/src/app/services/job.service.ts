import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { JobDetails } from '../models/job-details';

@Injectable({
  providedIn: 'root',
})
export class JobService {
  private baseURL = 'http://127.0.0.1:8000';
  private jobsURL = this.baseURL + '/api/jobs';
  private createJobUrl = this.baseURL + '/api/createjob';
  private jobDetailURL = this.baseURL + '/api/job_detail';
  private jobImageUrl = this.baseURL + '/job_images';
  private errorUpdateUrl = this.baseURL + '/api/error_update';
  private jobDetailUrl = this.baseURL + '/api/job_detail';
  private jobDeleteUrl = this.baseURL + '/api/job_delete'

  httpOptionJSON = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
  };

  constructor(private http: HttpClient) {}

  /*
   * Gets all existing jobs
   * @return {Observable<Job>} an observable of all existing jobs
   * */
  getJobs(): Observable<JobDetails[]> {
    return this.http.get<JobDetails[]>(this.jobsURL, this.httpOptionJSON);
  }

  putError(compId: number, body: any): Observable<Object> {
    console.log(compId, body);
    console.log(this.errorUpdateUrl + '/' + compId);
    return this.http.put<any>(
      this.errorUpdateUrl + '/' + compId,
      body,
      this.httpOptionJSON
    );
  }

  /*
   * Gets the details of a specific job
   * @param {string} jobId ID of the job to get the details from
   * @return {Observable<Job>} an observable of all existing jobs
   * */
  getJobDetails(jobId: string): Observable<JobDetails> {
    return this.http.get<JobDetails>(
      this.jobDetailUrl + '/' + jobId,
      this.httpOptionJSON
    );
  }

  /*
   * Gets an image from a job
   * @param {string} imageId ID of the image
   * @return {Observable<Blob>} an observable of the image
   * */
  getJobImageById(imageId: string): Observable<Blob> {
    return this.http.get(this.jobImageUrl + '/' + imageId, {
      responseType: 'blob',
    });
  }

  /*
   * Creates a new job
   * @param {string} jobName name of the job
   * @param {Blob[]} images image files
   * @param {Blob} config config.json file
   * */
  public addJob(
    jobName: string,
    images: Array<Blob>,
    config: Blob,
    csv: Blob
  ): Observable<Object> {
    const formData = new FormData();

    for (let i = 0; i < images.length; i++) {
      formData.append('panels[' + i + ']panel_photo', images[i]);
    }
    formData.append('name', jobName);
    formData.append('config', config);
    formData.append('position', csv);

    return this.http.post<Object>(this.createJobUrl, formData);
  }

  public deleteJob(id: string): Observable<object> {
    const deleteUrl = this.jobDeleteUrl + '/' + id;

    return this.http.delete(deleteUrl);
  }


}
