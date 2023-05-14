import { Component, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { SpinnereventsService } from 'src/app/services/spinnerevents.service';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  isLogin: boolean = true;
  hide = true;
  hide1 = true;
  hide2 = true;
  login: FormGroup = this.formBuilder.group({});
  signup: FormGroup = this.formBuilder.group({});
  signUpFormPage: number = 1;

  constructor(private _snackBar: MatSnackBar, public dialogRef: MatDialogRef<LoginComponent>, public formBuilder: FormBuilder, private userService: UserService, private spinnerEvents: SpinnereventsService) { }

  ngOnInit(): void {
    this.login = this.formBuilder.group({
      email: new FormControl('', [Validators.required, Validators.email]),
      password: new FormControl('', [Validators.required, Validators.minLength(6)])
    });

    this.signup = this.formBuilder.group({
      email: new FormControl('', [Validators.required, Validators.email]),
      name: new FormControl('', [Validators.required]),
      mobNo: new FormControl('', [Validators.required, Validators.pattern("^[0-9]*$"), Validators.minLength(10), Validators.maxLength(10)]),
      password: new FormControl('', [Validators.required, Validators.minLength(6)]),
      repassword: new FormControl('', [Validators.required, Validators.minLength(6)]),
      street: new FormControl('', [Validators.required]),
      village: new FormControl('', [Validators.required]),
      pin: new FormControl('', [Validators.required, Validators.pattern("^[0-9]*$"), Validators.minLength(6), Validators.maxLength(6)]),
    });
  }

  dialogState(state: boolean): void {
    this.isLogin = state;
    this.signUpFormPage = 1;
  }

  doLogin() {
    this.spinnerEvents.spinnerEvent.emit(true);
    this.userService.doLoginUsingUsernamePassword(this.login.value).subscribe({
      next: (response) => {
        this.dialogRef.close();
        this.userService.loginEvent.emit(response);
        this.spinnerEvents.spinnerEvent.emit(false);
        this.showSnackBar("Welcome", "Ok");
      },
      error: (error) => {
        this.spinnerEvents.spinnerEvent.emit(false);
        console.log(error)
        this.showSnackBar("Login failed "+ error.error.detail, "Ok");
      }
    });
  }

  doSignup() {
    if(!this.signup.valid) {
      this.showSnackBar("Check filled form, Something wrong", "Ok");
      return;
    }
    this.spinnerEvents.spinnerEvent.emit(true);
    console.log(this.signup.value);
    this.userService.doSignupUsingPassword(this.signup.value).subscribe({
      next: (response) => {
        this.spinnerEvents.spinnerEvent.emit(false);
        this.dialogRef.close();
        this.showSnackBar("Account Created...", "Ok");
      },
      error: (error) => {
        this.spinnerEvents.spinnerEvent.emit(false);
        this.showSnackBar(error.error.detail, "Ok");
      }
    });
  }

  changePage(page: number) {
    if(page == 2) {
      this.signup.get('email')?.markAsTouched();
      this.signup.get('name')?.markAsTouched();
      this.signup.get('mobNo')?.markAsTouched();
      this.signup.get('password')?.markAsTouched();
      if(this.signup.get('email')?.valid && 
         this.signup.get('name')?.valid && 
         this.signup.get('mobNo')?.valid && 
         this.signup.get('password')?.valid) {

        this.signUpFormPage = page;
      }
    } else {
      this.signup.markAllAsTouched();
      this.signUpFormPage = page;
    }
  }

  checkPassword() {
    if(this.signup.value.password !== this.signup.value.repassword) {
      this.signup.get('repassword')?.setErrors({notSame: "Pass"});
    }
    console.log(this.signup.get('repassword')?.hasError(''))
  }

  showSnackBar(message: string, action: string): void {
    this._snackBar.open(message, action, {
      duration:  1500
    });
  }
}
