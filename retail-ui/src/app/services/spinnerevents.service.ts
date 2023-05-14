import { EventEmitter, Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class SpinnereventsService {
  public spinnerEvent: EventEmitter<boolean>;
  constructor() { 
    this.spinnerEvent = new EventEmitter();
  }
}
