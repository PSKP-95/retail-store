import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CartComponent } from './components/cart/cart.component';
import { ItemsComponent } from './components/items/items.component'
import { ProductComponent } from './components/product/product.component';
import { ProfileComponent } from './components/profile/profile.component';
const routes: Routes = [
  {path: "", component: ItemsComponent},
  {path: "cart", component: CartComponent},
  {path: "profile", component: ProfileComponent},
  {path: "product/:id", component: ProductComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
