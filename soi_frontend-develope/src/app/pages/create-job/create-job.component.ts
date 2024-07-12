import {Component} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {JobService} from "../../services/job.service";
import {Router} from "@angular/router";
import { ImageUiData } from 'src/app/models/image-data';

@Component({
  selector: 'app-create-job',
  templateUrl: './create-job.component.html',
  styleUrls: ['./create-job.component.css']
})
export class CreateJobComponent {

  public jobForm: FormGroup = this.formBuilder.group({
    jobName: ['', [Validators.required, Validators.pattern('[a-zA-Z 0-9]*')]],
    images: ['', Validators.required],
    configurations: ['', Validators.required],
    csv: ['', Validators.required]
  });

  /*
  * Flag whether create job button was clicked for showing possible form validation errors
  * */
  public submitClicked: boolean = false;
  public images: Array<ImageUiData> = [];

  public constructor(
      private formBuilder: FormBuilder,
      private jobService: JobService,
      private router: Router
  ) { }

  /*
  * Creates a new job if all values are entered correctly. Executed on click of 'Create Job' button.
  * */
  public submitJob() {
    this.submitClicked = true;
    
    if (!this.jobForm.valid) {
      return;
    }
    let jobData = this.jobForm.value;
    this.jobService.addJob(jobData.jobName, jobData.images, jobData.configurations, jobData.csv).subscribe(
        next => this.router.navigate(['']),
        error => console.error(typeof error)
    )
  }

  public processCsv(inputCsv: any): void {

    const selectedFile: File = inputCsv.target.files[0];
    
    if (inputCsv.target.files){
      this.jobForm.get('csv')?.setValue(selectedFile);
    }
  }

  /*
  * Handles changes of the config file input by adding it to the jobForm.
  * */
  public processConfigFile(inputConfig: any): void {

    const selectedFile: File = inputConfig.target.files[0];
    
    if (inputConfig.target.files){
      this.jobForm.get('configurations')?.setValue(selectedFile);
    }
  }

  /*
  * Handles changes of the image files input by adding a list of images to the jobForm.
  * */
  public processImageFiles(inputImages: any): void {
    let panel: Array<Blob> = [];

      if (inputImages.target.files && inputImages.target.files[0]) {
          for (let i = 0; i < inputImages.target.files.length; i++) {

            const panelPhoto = inputImages.target.files[i]
            panel.push(panelPhoto);
            this.jobForm.get('images')?.patchValue(panel);

            const reader = new FileReader();
            const imageName: string = inputImages.target.files[i].name;
     
            reader.onload = (event:any) => {
              const imageData: ImageUiData = {image: event.target.result, imageName: imageName}
              this.images = [...this.images, imageData]
                }

              reader.readAsDataURL(inputImages.target.files[i]);
          }
      }

  }

}
