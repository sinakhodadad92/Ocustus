import { Component, OnInit, Inject } from '@angular/core';
import { JobService } from '../../services/job.service';
import { ActivatedRoute } from '@angular/router';
import { NgbCarousel } from '@ng-bootstrap/ng-bootstrap';
import { ViewChild } from '@angular/core';
import { Error, JobDetails } from 'src/app/models/job-details';

@Component({
  selector: 'app-job-results',
  templateUrl: './job-results.component.html',
  styleUrls: ['./job-results.component.css'],
})
export class JobResultsComponent implements OnInit {
  @ViewChild('carousel')
  carousel!: NgbCarousel;

  animal!: string;
  name!: string;

  public currentJob: JobDetails | undefined;
  public currentChunks: Error[][] | undefined;
  public imageArray: string[] = []; // string encodings of images shown for a job

  public constructor(
    private route: ActivatedRoute,
    private jobService: JobService
  ) {}

  /*
   * Takes the ID of the current job from the route and uses it to load job and images
   * */

  saveFP() {
    this.currentJob?.panels.forEach((pan) => {
      pan.errors.forEach((er) => {
        console.log(er.rework);
      });
    });
  }

  changed(errCompo: Error) {
    console.log(errCompo.designator);
    const reworkbody = { rework: errCompo.rework };
    this.jobService.putError(errCompo.id, reworkbody).subscribe(
      (resp) => {
        console.log(resp);
      },
      (error) => console.error(error.message)
    );
  }

  public ngOnInit(): void {
    const jobIdFromRoute = this.route.snapshot.paramMap.get('jobId');
    if (
      jobIdFromRoute != null &&
      this.containsOnlyNumbersAndLetters(jobIdFromRoute)
    ) {
      this.jobService.getJobDetails(jobIdFromRoute).subscribe(
        (job) => {
          this.currentJob = job;

          //          this.currentChunks = this.chunkArray(
          //          this.currentJob.panels[0].errors,
          //            10
          //          );
        },
        (error) => console.error(error.message)
      );
    } // otherwise no job is displayed
  }

  chunkArray(myArray: Error[], chunk_size: number) {
    var index = 0;
    var arrayLength = myArray.length;
    var tempArray = [];

    for (index = 0; index < arrayLength; index += chunk_size) {
      var myChunk = myArray.slice(index, index + chunk_size);
      // Do something if you want with the group
      tempArray.push(myChunk);
    }

    return tempArray;
  }

  nextStep() {
    this.carousel.next();
  }
  prevStep() {
    this.carousel.prev();
  }

  /*
   * Loads each image associated to a job via the image IDs
   * */

  /*
   * Takes a Blob of an image, converts it in a string and appends it to the imageArray
   * */
  private createImageFromBlob(image: Blob): void {
    const reader = new FileReader();
    reader.addEventListener(
      'load',
      () => {
        if (reader.result && typeof reader.result === 'string') {
          this.imageArray.push(reader.result);
        }
      },
      false
    );
    if (image) {
      reader.readAsDataURL(image);
    }
  }

  /*
   * Checking a string for containing nothing but numbers and letters. Used for checking jobID from route params
   * */
  private containsOnlyNumbersAndLetters(s: string): boolean {
    return /^[0-9a-zA-Z]*$/.test(s);
  }
}
