import {AfterViewInit, Component, ElementRef, Input, OnInit, ViewChild} from '@angular/core';
import {Error, Panel} from "../../models/job-details";

@Component({
  selector: 'panel-canvas-component',
  templateUrl: './panel-canvas.component.html',
  styleUrls: ['./panel-canvas.component.css']
})
export class PanelCanvasComponent implements OnInit, AfterViewInit {

  constructor() { }

  @ViewChild('canvas') public canvas: ElementRef | undefined;

  // default circle size
  private circleRadius = 15;
  private height = 0; // height is calculated based on width and the image proportions

  @Input() public panel: Panel | undefined;
  @Input() public width = 900;

  private cx: CanvasRenderingContext2D | null | undefined;
  private img = new Image();

  ngOnInit(): void {
    if(this.panel) {
      this.img.src = this.panel.cropped_panel_photo;
    }
  }

  public ngAfterViewInit() {
    const canvasEl: HTMLCanvasElement = this.canvas?.nativeElement;
    this.cx = canvasEl.getContext('2d');
    if (!this.cx) throw 'Cannot get context';

    if(this.img.complete) { //check if image was already loaded by the browser
      this.height = this.img.height * this.width / this.img.width; // reset height so that the image is scaled proportionally (width is fixed)
      // set height and width of the canvas to the width and height based on the image
      canvasEl.width = this.width;
      canvasEl.height = this.height;

      this.render();

    }else {
      this.img.onload = () => {
        this.height = this.img.height * this.width / this.img.width; // reset height so that the image is scaled proportionally (width is fixed)
        // set height and width of the canvas to the width and height based on the image
        canvasEl.width = this.width;
        canvasEl.height = this.height;

        this.render();
      }
    }
  }

  /**
   * Checks whether image was loaded and after that draws the image and marks the erros on the panel
   * */
  private render():void {
    if(this.cx){
      this.cx.drawImage(this.img, 0, 0, this.width, this.height);
      this.showErrors(this.panel?.errors);
    }
  }

  /**
   * Reads the errors given from the backend and marks those that have to be reworked
   * */
  private showErrors(errors: Error[] = []): void {
    let widthScaleFactor = this.width / this.img.width;
    let heightScaleFactor = this.height / this.img.height;

    // draw circles for all errors that have to be reworked
    for (let i = 0; i < errors.length; i++) {
      if (errors[i].rework) {
        this.drawCircleWithIdx(
          errors[i].coordinate_x * widthScaleFactor,
          errors[i].coordinate_y * heightScaleFactor,
          this.circleRadius,
          i+1);
      }
    }
  }

  /**
   * Draws a circle with a number in it indicating the number of the marked error
   * */
  private drawCircleWithIdx(x: number, y: number, radius: number, errorIdx: number, color: string = "#fff26b"): void {
    if(this.cx){
      this.cx.lineCap = 'round';
      this.cx.fillStyle = color;
      this.cx.strokeStyle = color;
      this.cx.lineWidth = 3;
      this.cx.beginPath();
      this.cx.arc(x, y, radius, 0, 2 * Math.PI);
      this.cx.stroke();
      this.cx.lineWidth = 1;
      this.cx.font = "bold " + radius + "px Arial";
      this.cx.textAlign = "center"
      this.cx.textBaseline = "middle";
      this.cx.fillText(errorIdx.toString(), x, y);
    }
  }


}
