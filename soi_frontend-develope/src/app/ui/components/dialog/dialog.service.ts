import { DeleteConfirmationDialogComponent } from './delete-confirmation-dialog/delete-confirmation-dialog.component';
import { Injectable } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { DialogConfigurations } from './dialog-configurations';
import { ErrorDialogComponent } from './error-dialog/error-dialog.component';
import { ProgressDialogComponent } from './progress-dialog/progress-dialog.component';
import { SuccessDialogComponent } from './success-dialog/success-dialog.component';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DialogService {

  public defaultOptions: DialogConfigurations = {
    width: '700px',
    height: '215px',
    disableMouseClose: true,
    disableEscClose: true,
    okButton: 'OK',
    cancelButton: 'Cancel'
  };

  constructor(private readonly dialog: MatDialog) {
  }

  /**
   * Opens an error dialog.
   * @param {ErrorDialogComponent} options dialog options and content
   */
  public openErrorDialog(options: DialogConfigurations): void {
    options = {...this.defaultOptions, ...options};
     this.dialog.open(ErrorDialogComponent, {
      disableClose: options.disableMouseClose, autoFocus: true,
      width: options.width, data: options, height: options.height,
      panelClass: 'custom-dialog-container'
    }).afterClosed();
  }

  /**
   * Opens a success dialog.
   * @param {SuccessDialogComponent} options dialog options and content
   */
  public openSuccessDialog(options: DialogConfigurations): void {
    options = {...this.defaultOptions, ...options};
     this.dialog.open(SuccessDialogComponent, {
      disableClose: options.disableMouseClose, autoFocus: true,
      width: options.width, height: options.height, data: options,
      panelClass: 'custom-dialog-container'
    }).afterClosed();
  }

    /**
   * Opens an progress dialog.
   * @param {ProgressDialogComponent} options dialog options and content
   */
     public openProgressDialog(options: DialogConfigurations): void {
      options = {...this.defaultOptions, ...options};
       this.dialog.open(ProgressDialogComponent, {
        disableClose: options.disableMouseClose, autoFocus: true,
        width: options.width, data: options, height: options.height,
        panelClass: 'custom-dialog-container'
      }).afterClosed();
    }

        /**
   * Opens a  confirmation dialog.
   * @param {DeleteConfirmationDialogComponent} options dialog options and content
   */
         public openconfirmationDialog(name: string): Observable<Boolean> {
          this.defaultOptions.name = name;
           return this.dialog.open(DeleteConfirmationDialogComponent, {
            disableClose: this.defaultOptions.disableMouseClose, autoFocus: true,
            width: this.defaultOptions.width, data: this.defaultOptions, height: this.defaultOptions.height,
            panelClass: 'custom-dialog-container'
          }).afterClosed();
        }

}