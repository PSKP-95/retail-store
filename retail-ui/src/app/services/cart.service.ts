import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Cart, CartItem, Item } from '../models/item.model';

@Injectable({
  providedIn: 'root'
})
export class CartService {
  itemUrl = "/api/item/"
  cartUrl = "/api/cartorder/cart"

  constructor(private http: HttpClient) { }

  loadCartProducts(id: string): Observable<Item[]> {
    return this.http.get<any>(`${this.itemUrl}/${id}`);
  }

  loadItemsInCart(): Observable<Cart> {
    return this.http.get<any>(`${this.cartUrl}`);
  }

  changeItemInCart(iid: string, qty: number): Observable<Cart> {
    let cartItem = new CartItem();
    cartItem.iid = iid;
    cartItem.qty = qty;
    return this.http.put<any>(`${this.cartUrl}`, cartItem);
  }
}
