import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Item } from 'src/app/models/item.model';
import { ProductsService } from 'src/app/services/products.service';

@Component({
  selector: 'app-cart-item',
  templateUrl: './cart-item.component.html',
  styleUrls: ['./cart-item.component.css']
})
export class CartItemComponent implements OnInit {
  @Input() iid: string = '';
  @Input() quantity: number = 0;
  item: Item = new Item();

  @Output() quantityChanged = new EventEmitter<number>();
  constructor(private productsService: ProductsService) { }

  ngOnInit(): void {
    this.productsService.loadProduct(this.iid).subscribe({
      next: (response: Item) => {
        console.log(response);
        this.item = response;
      },
      error: (error) => {
        console.log(error);
      }
    });
  }

  doMultiplication(a: number, b: number): number  {
    return a * b;
  }

  removeItemFromCart() {
    this.quantityChanged.emit(0);
  }

}
