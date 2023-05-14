import { Component, OnInit } from '@angular/core';
import {MatSnackBar} from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { CartItem, Item } from 'src/app/models/item.model';
import { CartService } from 'src/app/services/cart.service';
import { ProductsService } from 'src/app/services/products.service';
import { SpinnereventsService } from 'src/app/services/spinnerevents.service';

@Component({
  selector: 'app-items',
  templateUrl: './items.component.html',
  styleUrls: ['./items.component.css']
})
export class ItemsComponent implements OnInit {
  items: Item[] = [];
  inCartItemIds: CartItem[] = [];
  constructor(private _snackBar: MatSnackBar, private productService: ProductsService, private router: Router, private cartService: CartService, private spinnerEvents: SpinnereventsService) {}

  ngOnInit(): void {
    this.spinnerEvents.spinnerEvent.emit(true);
    this.cartService.loadItemsInCart().subscribe({
      next: (response) => {
        this.inCartItemIds = response.items;
        console.log(response);
        
      },
      error: (error) => {
        console.log(error);
      }
    })

    this.productService.loadAllProducts().subscribe((response: any) => {
      this.items = response;
      this.spinnerEvents.spinnerEvent.emit(false);
    });
  }

  checkInCart(id: string): number {
    let index = 0;
    for(let cartItem of this.inCartItemIds) {
      if(cartItem.iid == id) {
        return index;
      }
      index++;
    }
    return -1;
  }

  changeLocalStorage() {
    localStorage.setItem("Cart", JSON.stringify(this.inCartItemIds));
  }

  addToCart(id: string, name: string): void {
    this.spinnerEvents.spinnerEvent.emit(true);
    this.cartService.changeItemInCart(id, 1).subscribe({
      next: (response) => {
        this.inCartItemIds = response.items;
        this.spinnerEvents.spinnerEvent.emit(false);
      },
      error: (error) => {
        console.log(error);
        this.spinnerEvents.spinnerEvent.emit(false);
      }
    });
    this.showSnackBar("Item added "+name, "Ok");
  }

  showSnackBar(message: string, action: string): void {
    this._snackBar.open(message, action, {
      duration:  1500
    });
  }

  removeFromCart(id: string, name: string): void {
    this.cartService.changeItemInCart(id, 0).subscribe({
      next: (response) => {
        this.inCartItemIds = response.items;
        this.spinnerEvents.spinnerEvent.emit(false);
      },
      error: (error) => {
        console.log(error);
        this.spinnerEvents.spinnerEvent.emit(false);
      }
    });
    this.showSnackBar("Item removed "+name, "Ok");
  }

  openProduct(id: string) {
    this.router.navigate([`/product/${id}`]);
  }
}
