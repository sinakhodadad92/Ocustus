import { DialogService } from './../../ui/components/dialog/dialog.service';
import { Component, OnInit } from '@angular/core';
import { JobService } from '../../services/job.service';
import { JobDetails } from 'src/app/models/job-details';
import { Router } from '@angular/router';

@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  styleUrls: ['./index.component.css'],
})
export class IndexComponent implements OnInit {
  jobs: JobDetails[] = [];

  deleteClicked: Boolean = false;

  constructor(private jobService: JobService,
              private dialogService: DialogService,
              private router: Router) {}

  getIcon(state: string): string {
    let icon = 'feedback';
    switch (state) {
      case 'PROCESSING':
        icon = 'loop';
        break;
      case 'COMPLETED':
        icon = 'done_outline';
        break;
      default:
        icon = 'feedback';
    }
    
    return icon;
  }

  public getIconMessage(iconString: string) : string {
    let icon = '';
    
    switch (iconString) {
      case 'PROCESSING':
        icon = 'The job is in process';
        break;
      case 'COMPLETED':
        icon = 'job processing complete';
        break;
      default:
        icon = 'The job creation has failed';
    }
   
    return icon;
  }

  ngOnInit(): void {
    this.loadJobs();
  }

  loadJobs(): void {
    this.jobService.getJobs().subscribe((jobs) => (this.jobs = jobs));
  }

  reload() {
    this.ngOnInit();
  }

  public listItemClicked(jobStatus: string, id: number): void{

    if (!this.deleteClicked)
    {

      if (jobStatus === 'COMPLETED') {
        this.router.navigate(['/jobresult', id]);
      }
      else if (jobStatus === 'PROCESSING') {
        this.dialogService.openProgressDialog({
          title: 'Pending: Job Creation In Progress',
          content: 'Please click on the refresh status button for updated progress'
        })
      }
      else if (jobStatus === 'FAILED') {
        this.dialogService.openErrorDialog({
          title: 'Error: Job Creation Failed',
          content: 'The data provided for the Job was not in the correct format'
        })
      }

    }

  }
  
  public deleteJob(id: number, name: string): void {
    this.deleteClicked = true;

    this.dialogService.openconfirmationDialog(name).subscribe((isDelete) => {

      if (isDelete) {
        this.jobService.deleteJob(id.toString()).subscribe(() => {
          this.jobs = this.jobs.filter(job => job.id != id)
          this.dialogService.openSuccessDialog({
            title: 'Success: Delete',
            content: 'The the job has been successfully deleted'
    
          })
          this.deleteClicked = false;
        })
      }
      else {
        this.deleteClicked = false;
      }
    });
  }

}
