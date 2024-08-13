import { Component, ChangeDetectorRef } from '@angular/core';


@Component({
  selector: 'app-dental-quote',
  templateUrl: './dental-quote.component.html',
  styleUrl: './dental-quote.component.scss',
})
export class DentalQuoteComponent {
  renderFileDetails = false;
  extractionError: string = '';
  waitForTyping: boolean = false;
  isChecked: boolean = false;

  constructor(

    private changeDetectorRef: ChangeDetectorRef
  ) {}

  autoExtractionCheckBox() {
    return this.isChecked;
  }

  onUploadDone(uploadedDocUUID: string) {
    //send request
  }

  
}
