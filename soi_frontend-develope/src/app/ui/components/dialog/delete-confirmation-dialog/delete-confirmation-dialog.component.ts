import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { DialogConfigurations } from '../dialog-configurations';

@Component({
  selector: 'app-delete-confirmation-dialog',
  templateUrl: './delete-confirmation-dialog.component.html',
  styleUrls: ['./delete-confirmation-dialog.component.css']
})
export class DeleteConfirmationDialogComponent{

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: DialogConfigurations,
    private readonly dialogRef: MatDialogRef<DeleteConfirmationDialogComponent>) {}

  
  public onClose(isDelete: boolean): void {
    this.dialogRef.close(isDelete);
  }
}
