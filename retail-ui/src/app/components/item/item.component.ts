import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-item',
  templateUrl: './item.component.html',
  styleUrls: ['./item.component.css']
})
export class ItemComponent implements OnInit {
  @Input() name = '';
  @Input() originalPrice = 0.0;
  @Input() price = 0.0;
  @Input() unit = '';
  @Input() imageUrl = '';
  @Input() cartButtonEnabled = true;

  @Output() itemSelected = new EventEmitter<boolean>();
  @Output() itemDisselected = new EventEmitter<boolean>();
  @Output() itemClicked = new EventEmitter();

  
  itemStyleToggle: boolean = true;
  constructor() { }

  ngOnInit(): void {
  }

  // expand(): void {
  //   if(this.itemStyleToggle) {
  //     this.itemStyle = 'item-expand';
  //   } else {
  //     this.itemStyle = 'item-contract'
  //   }
  //   this.itemStyleToggle = !this.itemStyleToggle;
  // }

  addToCart() {
    this.itemSelected.emit();
  }

  removeFromCart() {
    this.itemDisselected.emit();
  }

  itemNameClicked() {
    this.itemClicked.emit();
  }

}
