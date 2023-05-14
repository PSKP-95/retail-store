import { HttpClient } from '@angular/common/http';
import { EventEmitter, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { User } from '../models/user.model';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  url = "/api/iam/"
  public loginEvent: EventEmitter<User>;
  public logoutEvent: EventEmitter<any>;

  constructor(private http: HttpClient) {
    this.loginEvent = new EventEmitter();
    this.logoutEvent = new EventEmitter();
  }

  getLoggedInUserProfile(): Observable<any> {
    return this.http.get<any>(`${this.url}`);
  }

  doLoginUsingUsernamePassword(value: any): Observable<any> {
    let formData = new FormData();
    formData.append("userid", value.email);
    formData.append("password", value.password);
    return this.http.post<any>(`${this.url}login`, formData);
  }

  doLogoutFromApp(): Observable<any> {
    return this.http.get<any>(`${this.url}logout`);
  }

  doSignupUsingPassword(value: any): Observable<User> {
    console.log(value);
    let user: User = new User();
    user.name = value.name;
    user.email = value.email;
    user.mobNum = value.mobNo;
    user.password = value.password;
    user.address = {
      "name": value.name,
      "pin": value.pin,
      "street": value.street,
      "village": value.village
    };

    // let formData = new FormData();
    // formData.append("email", value.email);
    // formData.append("name", value.name);
    // formData.append("address", value.address);
    // formData.append("mobNum", value.mobNo);
    // formData.append("password", value.password);
    return this.http.post<any>(`${this.url}signup`, user);
  }

  refreshJwtToken(): Observable<any> {
    return this.http.get(`${this.url}token`);
  }
}
