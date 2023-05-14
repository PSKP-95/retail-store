import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Item } from '../models/item.model';

@Injectable({
  providedIn: 'root'
})
export class ProductsService {

  url = "/api/item/"

  constructor(private http: HttpClient) { }

  loadAllProducts(): Observable<Item[]> {
    return this.http.get<any>(`${this.url}`);
  }

  loadProduct(id: string): Observable<Item> {
    return this.http.get<any>(`${this.url}${id}`)
  }
}
