import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { JobService } from '../../services/job.service';
import { JobDetails, Panel } from '../../models/job-details';
import { Location } from '@angular/common';

@Component({
  selector: 'app-job-report',
  templateUrl: './job-report.component.html',
  styleUrls: ['./job-report.component.css'],
})
export class JobReportComponent implements OnInit {
  public currentJob: JobDetails | undefined;

  /*
   * Contains all panels that are labelled to be reworked.
   * */
  public errorPanels: Panel[] | undefined = [];

  constructor(
    private route: ActivatedRoute,
    private jobService: JobService,
    private _location: Location
  ) {}

  backClicked() {
    this._location.back();
  }

  ngOnInit(): void {
    const jobIdFromRoute = this.route.snapshot.paramMap.get('jobId');
    if (
      jobIdFromRoute != null &&
      this.containsOnlyNumbersAndLetters(jobIdFromRoute)
    ) {
      this.jobService.getJobDetails(jobIdFromRoute).subscribe(
        (job) => {
          this.currentJob = job;

          // Add panel numbering
          this.currentJob.panels.forEach(
            (panel, index) => (panel.panel_number = index + 1)
          );

          // Filter for panels that have to be reworked
          this.errorPanels = this.currentJob.panels.filter(
            // get all panels
            (panel) =>
              panel.errors.some(
                // that have at least one board analysis
                (err) => err.rework
              )
          ); // which has to be reworked

          // For each panel, remove errors that do not need to be reworked
          for (let panel of this.errorPanels) {
            panel.errors = panel.errors.filter((err) => err.rework); // keep only errors to be reworked
          }
        },
        (error) => console.error(error.message)
      );
    } // otherwise no job is displayed
  }

  /*
   * Checking a string for containing nothing but numbers and letters. Used for checking jobID from route params.
   * */
  private containsOnlyNumbersAndLetters(s: string): boolean {
    return /^[0-9a-zA-Z]*$/.test(s);
  }

  /*
  * Prints the report page equal to CTRL-P.
  * */
  printReport() : void {
    window.print();
    
      
  
  }
  
}
