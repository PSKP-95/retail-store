import { Component, OnInit } from '@angular/core';
import { CartItem } from 'src/app/models/item.model';
import { CartService } from 'src/app/services/cart.service';
import { SpinnereventsService } from 'src/app/services/spinnerevents.service';

@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.css']
})
export class CartComponent implements OnInit {
  inCartItemIds: CartItem[] = [];
  constructor(private cartService: CartService, private spinnerEvents: SpinnereventsService) { }

  ngOnInit(): void {
    this.spinnerEvents.spinnerEvent.emit(true);
    this.cartService.loadItemsInCart().subscribe({
      next: (response) => {
        this.inCartItemIds = response.items;
        console.log(response);
        this.spinnerEvents.spinnerEvent.emit(false);
      },
      error: (error) => {
        console.log(error);
        this.spinnerEvents.spinnerEvent.emit(false);
      }
    })
  }

  sendNewQuantity(iid: string, event: number) {
    this.spinnerEvents.spinnerEvent.emit(true);
    this.cartService.changeItemInCart(iid, 0).subscribe({
      next: (response) => {
        this.inCartItemIds = response.items;
        this.spinnerEvents.spinnerEvent.emit(false);
      },
      error: (error) => {
        console.log(error);
        this.spinnerEvents.spinnerEvent.emit(false);
      }
    });
  }
}
