import { Component, HostListener, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { DialogConfigurations } from '../dialog-configurations';

@Component({
  selector: 'tnpa-error-dialog',
  templateUrl: './error-dialog.component.html',
  styleUrls: ['./error-dialog.component.css']
})
export class ErrorDialogComponent {

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: DialogConfigurations,
    private readonly dialogRef: MatDialogRef<ErrorDialogComponent>) {}

  /**
   * Handles the enter key for accept action of dialog.
   */
  @HostListener('document:keydown.enter', ['$event'])
  public onEnter(): void {
    this.dialogRef.close();
  }

}